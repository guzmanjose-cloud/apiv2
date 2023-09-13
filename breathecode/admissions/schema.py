import graphene
from graphql import GraphQLError
from graphql.type.definition import GraphQLResolveInfo
from graphene_django import DjangoObjectType
import graphene_django_optimizer as gql_optimizer

from breathecode.admissions import models
from breathecode.admissions.actions import haversine
from django.db.models import FloatField, Q, Value
from django.utils import timezone


class CohortTimeSlot(DjangoObjectType):

    class Meta:
        model = models.CohortTimeSlot
        fields = '__all__'


class City(DjangoObjectType):

    class Meta:
        model = models.City
        fields = '__all__'


class Country(DjangoObjectType):

    class Meta:
        model = models.Country
        fields = '__all__'

    city = graphene.Field(City)


class Academy(DjangoObjectType):

    class Meta:
        model = models.Academy
        fields = '__all__'

    country = graphene.Field(Country)
    city = graphene.Field(City)


class Syllabus(DjangoObjectType):

    class Meta:
        model = models.Syllabus
        fields = '__all__'


class SyllabusVersion(DjangoObjectType):

    class Meta:
        model = models.SyllabusVersion
        fields = '__all__'

    syllabus = graphene.Field(Syllabus)


class SyllabusSchedule(DjangoObjectType):

    class Meta:
        model = models.SyllabusSchedule
        fields = '__all__'

    syllabus = graphene.Field(Syllabus)


class Cohort(DjangoObjectType):

    class Meta:
        model = models.Cohort
        fields = '__all__'

    academy = graphene.Field(Academy)
    syllabus_version = graphene.Field(SyllabusVersion)
    schedule = graphene.Field(SyllabusSchedule)
    distance = graphene.Float()

    timeslots = graphene.List(CohortTimeSlot)

    def resolve_timeslots(self, info, first=10):
        return gql_optimizer.query(self.cohorttimeslot_set.all()[0:first], info)

    def resolve_distance(self, info):
        if not self.latitude or not self.longitude or not self.academy.latitude or not self.academy.longitude:
            return None

        return haversine(self.longitude, self.latitude, self.academy.longitude, self.academy.latitude)


class Admissions(graphene.ObjectType):
    hello = graphene.String(default_value='Hi!')
    cohorts = graphene.List(Cohort,
                            page=graphene.Int(),
                            limit=graphene.Int(),
                            plan=graphene.String(),
                            coordinates=graphene.String())

    def resolve_cohorts(self, info: GraphQLResolveInfo, page=1, limit=10, **kwargs):
        items = models.Cohort.objects.all()
        start = (page - 1) * limit
        end = start + limit

        items = items.annotate(longitude=Value(None, output_field=FloatField()),
                               latitude=Value(None, output_field=FloatField()))

        upcoming = kwargs.get('upcoming', None)
        if upcoming == 'true':
            now = timezone.now()
            items = items.filter(Q(kickoff_date__gte=now) | Q(never_ends=True))

        never_ends = kwargs.get('never_ends', None)
        if never_ends == 'false':
            items = items.filter(never_ends=False)

        academy = kwargs.get('academy', None)
        if academy is not None:
            items = items.filter(academy__slug__in=academy.split(','))

        location = kwargs.get('location', None)
        if location is not None:
            items = items.filter(academy__slug__in=location.split(','))

        ids = kwargs.get('id', None)
        if ids is not None:
            items = items.filter(id__in=ids.split(','))

        slugs = kwargs.get('slug', None)
        if slugs is not None:
            items = items.filter(slug__in=slugs.split(','))

        stage = kwargs.get('stage')
        if stage:
            items = items.filter(stage__in=stage.upper().split(','))
        else:
            items = items.exclude(stage='DELETED')

        if coordinates := kwargs.get('coordinates', ''):
            try:
                latitude, longitude = coordinates.split(',')
                latitude = float(latitude)
                longitude = float(longitude)
            except:
                raise GraphQLError('Bad coordinates, the format is latitude,longitude',
                                   slug='bad-coordinates')

            if latitude > 90 or latitude < -90:
                raise GraphQLError('Bad latitude', slug='bad-latitude')

            if longitude > 180 or longitude < -180:
                raise GraphQLError('Bad longitude', slug='bad-longitude')

            items = items.annotate(longitude=Value(longitude, FloatField()),
                                   latitude=Value(latitude, FloatField()))

        saas = kwargs.get('saas', '').lower()
        if saas == 'true':
            items = items.filter(academy__available_as_saas=True)

        elif saas == 'false':
            items = items.filter(academy__available_as_saas=False)

        syllabus_slug = kwargs.get('syllabus_slug', '')
        if syllabus_slug:
            items = items.filter(syllabus_version__syllabus__slug=syllabus_slug)

        plan = kwargs.get('plan', '')
        if plan == 'true':
            items = items.filter(academy__main_currency__isnull=False, cohortset__isnull=False).distinct()

        elif plan == 'false':
            items = items.filter().exclude(cohortset__isnull=True).distinct()

        elif plan:
            kwargs = {}

            if isinstance(plan, int) or plan.isnumeric():
                kwargs['cohortset__plan__id'] = plan
            else:
                kwargs['cohortset__plan__slug'] = plan

            items = items.filter(**kwargs).distinct()

        return gql_optimizer.query(items[start:end], info)
