from pydantic import BaseModel, Field, model_validator, field_validator, ConfigDict

class Affiliation(BaseModel):
    '''
    A model representing a Scopus affiliation entry.
    '''
    name: str = Field('', alias='affilname')
    city: str = Field('', alias='affiliation-city')
    country: str = Field('', alias='affiliation-country')

    @field_validator('name', 'city', 'country', mode='before')
    def _none_to_empty(cls, v) -> str:
        return '' if v is None else v

    model_config = ConfigDict(
        populate_by_name=True,
        extra='ignore'
    )

class Article(BaseModel):
    '''
    A model representing a Scopus article entry.
    '''
    title: str = Field(..., alias='dc:title')
    publication_name: str = Field('', alias='prism:publicationName')
    creator: str = Field('', alias='dc:creator')
    affiliations: list[Affiliation] = Field(default_factory=list, alias='affiliation')
    scopus_link: str = ''

    @model_validator(mode='before')
    def _check_and_extract(cls, data: dict) -> dict:
        if 'dc:title' not in data:
            raise ValueError(f'Invalid response: {data}')
        links: list[dict] = data.get('link', [])
        data['scopus_link'] = next(
            (link.get('@href') for link in links if link.get('@ref') == 'scopus'),
            ''
        )
        return data

    model_config = ConfigDict(
        populate_by_name=True,
        extra='ignore'
    )
