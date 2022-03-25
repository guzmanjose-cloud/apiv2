import base64, frontmatter, markdown
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser
from django.template.loader import get_template
from breathecode.admissions.models import Academy, Cohort
from breathecode.events.models import Event
from django.db.models import Q
from breathecode.assessment.models import Assessment

__all__ = ['AssetTechnology', 'Asset', 'AssetAlias']


class AssetTechnology(models.Model):
    slug = models.SlugField(max_length=200, unique=True)
    title = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title


PUBLIC = 'PUBLIC'
UNLISTED = 'UNLISTED'
PRIVATE = 'PRIVATE'
VISIBILITY = (
    (PUBLIC, 'Public'),
    (UNLISTED, 'Unlisted'),
    (PRIVATE, 'Private'),
)

PROJECT = 'PROJECT'
EXERCISE = 'EXERCISE'
LESSON = 'LESSON'
QUIZ = 'QUIZ'
VIDEO = 'VIDEO'
TYPE = (
    (PROJECT, 'Project'),
    (EXERCISE, 'Exercise'),
    (QUIZ, 'Quiz'),
    (LESSON, 'Lesson'),
    (VIDEO, 'Video'),
)

BEGINNER = 'BEGINNER'
EASY = 'EASY'
DIFFICULTY = (
    (BEGINNER, 'Beginner'),
    (EASY, 'Easy'),
)

DRAFT = 'DRAFT'
UNNASIGNED = 'UNNASIGNED'
OK = 'OK'
ASSET_STATUS = (
    (UNNASIGNED, 'Unnasigned'),
    (DRAFT, 'Draft'),
    (OK, 'Ok'),
)

ASSET_SYNC_STATUS = (
    ('PENDING', 'Pending'),
    ('ERROR', 'Error'),
    ('OK', 'Ok'),
    ('WARNING', 'Warning'),
)


class Asset(models.Model):
    def __init__(self, *args, **kwargs):
        super(Asset, self).__init__(*args, **kwargs)
        self.__old_slug = self.slug

    slug = models.SlugField(max_length=200, unique=True)
    title = models.CharField(max_length=200, blank=True)
    lang = models.CharField(max_length=2, blank=True, null=True, default=None, help_text='E.g: en, es, it')

    all_translations = models.ManyToManyField('self', blank=True)
    technologies = models.ManyToManyField(AssetTechnology)

    url = models.URLField()
    solution_url = models.URLField(null=True, blank=True, default=None)
    preview = models.URLField(null=True, blank=True, default=None)
    description = models.TextField(null=True, blank=True, default=None)
    readme_url = models.URLField(null=True,
                                 blank=True,
                                 default=None,
                                 help_text='This will be used to synch from github')
    intro_video_url = models.URLField(null=True, blank=True, default=None)
    solution_video_url = models.URLField(null=True, blank=True, default=None)
    readme = models.TextField(null=True, blank=True, default=None)

    config = models.JSONField(null=True, blank=True, default=None)

    external = models.BooleanField(
        default=False,
        help_text=
        'External assets will open in a new window, they are not built using breathecode or learnpack tecnology'
    )

    interactive = models.BooleanField(default=False)
    with_solutions = models.BooleanField(default=False)
    with_video = models.BooleanField(default=False)
    graded = models.BooleanField(default=False)
    gitpod = models.BooleanField(default=False)
    duration = models.IntegerField(null=True, blank=True, default=None, help_text='In hours')

    difficulty = models.CharField(max_length=20, choices=DIFFICULTY, default=None, null=True, blank=True)
    visibility = models.CharField(max_length=20, choices=VISIBILITY, default=PUBLIC)
    asset_type = models.CharField(max_length=20, choices=TYPE)

    status = models.CharField(max_length=20,
                              choices=ASSET_STATUS,
                              default=DRAFT,
                              help_text='Related to the publishing of the asset')
    sync_status = models.CharField(max_length=20,
                                   choices=ASSET_SYNC_STATUS,
                                   default=None,
                                   null=True,
                                   blank=True,
                                   help_text='Internal state automatically set by the system based on sync')
    test_status = models.CharField(max_length=20,
                                   choices=ASSET_SYNC_STATUS,
                                   default=None,
                                   null=True,
                                   blank=True,
                                   help_text='Internal state automatically set by the system based on test')
    last_synch_at = models.DateTimeField(null=True, blank=True, default=None)
    last_test_at = models.DateTimeField(null=True, blank=True, default=None)
    status_text = models.TextField(null=True,
                                   default=None,
                                   blank=True,
                                   help_text='Used by the sych status to provide feedback')

    authors_username = models.CharField(max_length=80,
                                        null=True,
                                        default=None,
                                        blank=True,
                                        help_text='Github usernames separated by comma')
    assessment = models.ForeignKey(Assessment,
                                   on_delete=models.SET_NULL,
                                   default=None,
                                   blank=True,
                                   null=True,
                                   help_text='Connection with the assessment breathecode app')
    author = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               default=None,
                               blank=True,
                               null=True,
                               help_text='Who wrote the lesson, not necessarily the owner')
    owner = models.ForeignKey(User,
                              on_delete=models.SET_NULL,
                              related_name='owned_lessons',
                              default=None,
                              blank=True,
                              null=True,
                              help_text='The owner has the github premissions to update the lesson')

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return f'{self.slug}'

    def save(self, *args, **kwargs):

        # only validate this on creation
        if self.pk is None or self.__old_slug != self.slug:
            alias = AssetAlias.objects.filter(slug=self.slug).first()
            if alias is not None:
                raise Exception('Slug is already taken by alias')
            super().save(*args, **kwargs)
            AssetAlias.objects.create(slug=self.slug, asset=self)

        else:
            super().save(*args, **kwargs)

    def get_readme(self, parse=False, raw=False):
        if self.readme is None:
            AssetErrorLog(slug=AssetErrorLog.EMPTY_README,
                          path=self.slug,
                          asset_type=self.asset_type,
                          status_text='Readme file was not found').save()
            self.set_readme(
                get_template('default_readme.md').render({
                    'title': self.title,
                    'lang': self.lang,
                    'asset_type': self.asset_type,
                }))

        if raw:
            return self.readme

        readme = {
            'raw': self.readme,
            'decoded': base64.b64decode(self.readme.encode('utf-8')).decode('utf-8')
        }
        if parse:
            _data = frontmatter.loads(readme['decoded'])
            readme['frontmatter'] = _data.metadata
            readme['html'] = markdown.markdown(_data.content, extensions=['markdown.extensions.fenced_code'])
        return readme

    def set_readme(self, content):
        self.readme = str(base64.b64encode(content.encode('utf-8')).decode('utf-8'))
        return self

    @staticmethod
    def get_by_slug(asset_slug, request=None, asset_type=None):
        user = None
        if request is not None and not isinstance(request.user, AnonymousUser):
            user = request.user

        alias = AssetAlias.objects.filter(Q(slug=asset_slug) | Q(asset__slug=asset_slug)).first()
        if alias is None:
            AssetErrorLog(slug=AssetErrorLog.SLUG_NOT_FOUND,
                          path=asset_slug,
                          asset_type=asset_type,
                          user=user).save()
            return None
        elif asset_type is not None and alias.asset.asset_type.lower() == asset_type.lower():
            AssetErrorLog(slug=AssetErrorLog.DIFFERENT_TYPE,
                          path=asset_slug,
                          asset_type=asset_type,
                          user=user).save()
        else:
            return alias.asset


class AssetAlias(models.Model):
    slug = models.SlugField(max_length=200, primary_key=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.slug


ERROR = 'ERROR'
FIXED = 'FIXED'
IGNORED = 'IGNORED'
ERROR_STATUS = (
    (ERROR, 'Error'),
    (FIXED, 'Fixed'),
    (IGNORED, 'Ignored'),
)


class AssetErrorLog(models.Model):
    SLUG_NOT_FOUND = 'slug-not-found'
    DIFFERENT_TYPE = 'different-type'
    EMPTY_README = 'empty-readme'
    INVALID_URL = 'invalid-url'

    asset_type = models.CharField(max_length=20, choices=TYPE, default=None, null=True, blank=True)
    slug = models.SlugField(max_length=200)
    status = models.CharField(max_length=20, choices=ERROR_STATUS, default=ERROR)
    path = models.CharField(max_length=200)
    status_text = models.TextField(
        null=True,
        blank=True,
        default=None,
        help_text='Status details, it may be set automatically if enough error information')
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             default=None,
                             null=True,
                             help_text='The user how asked for the asset and got the error')
    asset = models.ForeignKey(
        Asset,
        on_delete=models.SET_NULL,
        default=None,
        null=True,
        help_text=
        'Assign an asset to this error and you will be able to create an alias for it from the django admin bulk actions "create alias"'
    )

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'Error {self.status} with {self.slug}'
