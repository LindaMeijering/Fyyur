from datetime import datetime
from enum import Enum

from flask_wtf import FlaskForm
from wtforms import (BooleanField, DateTimeField, SelectField,
                     SelectMultipleField, StringField)
from wtforms.validators import URL, AnyOf, DataRequired, Optional, Regexp


class GenreEnum(str, Enum):
    ALTERNATIVE = 'Alternative'
    BLUES = 'Blues'
    CLASSICAL = 'Classical'
    COUNTRY = 'Country'
    ELECTRONIC = 'Electronic'
    FOLK = 'Folk'
    FUNK = 'Funk'
    HIP_HOP = 'Hip-Hop'
    HEAVY_METAL = 'Heavy Metal'
    INSTRUMENTAL = 'Instrumental'
    JAZZ = 'Jazz'
    MUSICAL_THEATRE = 'Musical Theatre'
    POP = 'Pop'
    PUNK = 'Punk'
    RNB = 'R&B'
    REGGAE = 'Reggae'
    ROCK = 'Rock n Roll'
    SOUL = 'Soul'
    OTHER = 'Other'

    @classmethod
    def choices(cls):
        return [(genre.value, genre.value) for genre in cls]


class StateEnum(str, Enum):
    AL = 'AL'
    AK = 'AK'
    AZ = 'AZ'
    AR = 'AR'
    CA = 'CA'
    CO = 'CO'
    CT = 'CT'
    DE = 'DE'
    DC = 'DC'
    FL = 'FL'
    GA = 'GA'
    HI = 'HI'
    ID = 'ID'
    IL = 'IL'
    IN = 'IN'
    IA = 'IA'
    KS = 'KS'
    KY = 'KY'
    LA = 'LA'
    ME = 'ME'
    MT = 'MT'
    NE = 'NE'
    NV = 'NV'
    NH = 'NH'
    NJ = 'NJ'
    NM = 'NM'
    NY = 'NY'
    NC = 'NC'
    ND = 'ND'
    OH = 'OH'
    OK = 'OK'
    OR = 'OR'
    MD = 'MD'
    MA = 'MA'
    MI = 'MI'
    MN = 'MN'
    MS = 'MS'
    MO = 'MO'
    PA = 'PA'
    RI = 'RI'
    SC = 'SC'
    SD = 'SD'
    TN = 'TN'
    TX = 'TX'
    UT = 'UT'
    VT = 'VT'
    VA = 'VA'
    WA = 'WA'
    WV = 'WV'
    WI = 'WI'
    WY = 'WY'

    @classmethod
    def choices(cls):
        return [(state.value, state.value) for state in cls]

    @classmethod
    def values(cls):
        return [state.value for state in cls]

class ShowForm(FlaskForm):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state',
        validators=[
            DataRequired(),
            AnyOf(StateEnum.values(), message='Please select a valid state')
        ],
        choices=StateEnum.choices(),
        coerce=str
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone', validators=[
            DataRequired(),
            Regexp(
                r'^[\d\-\(\) ]+$',
                message='Phone number should only contain digits, spaces, parentheses and hyphens'
            ),
            Regexp(
                r'^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$',
                message='Phone number must be in format XXX-XXX-XXXX or (XXX) XXX-XXXX'
            )
        ]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres',
        validators=[DataRequired()],
        choices=GenreEnum.choices(),
        coerce=str
    )

    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website_link = StringField(
        'Website Link',
        validators=[Optional(), URL(message='Invalid URL.')]
    )

    seeking_talent = BooleanField(
        'seeking_talent', default=False, false_values=('false', False, '', None))

    seeking_description = StringField(
        'seeking_description'
    )



class ArtistForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state',
        validators=[
            DataRequired(),
            AnyOf(StateEnum.values(), message='Please select a valid state')
        ],
        choices=StateEnum.choices(),
        coerce=str
    )
    phone = StringField(
        'phone', validators=[
            DataRequired(),
            Regexp(
                r'^[\d\-\(\) ]+$',
                message='Phone number should only contain digits, spaces, parentheses and hyphens'
            ),
            Regexp(
                r'^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$',
                message='Phone number must be in format XXX-XXX-XXXX or (XXX) XXX-XXXX'
            )
        ]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres',
        validators=[DataRequired()],
        choices=GenreEnum.choices(),
        coerce=str
    )

    facebook_link = StringField(
        'facebook_link', validators=[URL()]
     )

    website_link = StringField(
        'Website Link',
        validators=[Optional(), URL(message='Invalid URL.')]
    )

    seeking_venue = BooleanField( 'seeking_venue' )

    seeking_description = StringField(
            'seeking_description'
     )

