from app import db
from datetime import datetime
import json


class Import(db.Model):
    """Imports of basic data done.

    source: '<file FILENAME>', '<uri URI>', 'api'
    """

    id = db.Column(db.Integer, primary_key=True)
    imported_at = db.Column(db.DateTime(), nullable=False)
    source = db.Column(db.String(512), nullable=False)
    raw = db.Column(db.Text())

    def __init__(self, source, raw):
        """Init Import."""
        self.source = source
        self.raw = raw
        self.imported_at = datetime.now()

    def __repr__(self):
        """Repr."""
        return '<Import {}>'.format(self.id)


class Doi(db.Model):
    """Doi model.

    Defines the publication data type with it's methods for useage of the Flask
    ORM.

    date comes as YYYY-MM-DD
    """

    doi = db.Column(db.String(64), primary_key=True, nullable=False)
    pmc_id = db.Column(db.String(256))
    pm_id = db.Column(db.String(256))
    import_id = db.Column(db.Integer, db.ForeignKey('import.id'), nullable=False)
    date_published = db.Column(db.DateTime())
    url_doi_new = db.Column(db.Boolean, nullable=False)
    url_doi_old = db.Column(db.Boolean, nullable=False)
    url_doi_lp = db.Column(db.Boolean, nullable=False)
    url_pm = db.Column(db.Boolean, nullable=False)
    url_pmc = db.Column(db.Boolean, nullable=False)
    url_unpaywall = db.Column(db.Boolean, nullable=False)
    is_valid = db.Column(db.Boolean)

    def __init__(self, doi, date_published, import_id, pmc_id=False, pm_id=False, url_doi_new=False, url_doi_old=False, url_doi_lp=False, url_pm=False, url_pmc=False, url_unpaywall=False, is_valid=False):
        """Init Doi."""
        self.doi = doi
        self.date_published = date_published
        self.import_id = import_id
        self.pmc_id = pmc_id
        self.pm_id = pm_id
        self.url_doi_new = url_doi_new
        self.url_doi_old = url_doi_old
        self.url_doi_lp = url_doi_lp
        self.url_pm = url_pm
        self.url_pmc = url_pmc
        self.url_unpaywall = url_unpaywall
        self.is_valid = is_valid

    def __repr__(self):
        """Repr."""
        return '<DOI {}>'.format(self.doi)


class Url(db.Model):
    """Url model.

    url_type:   'ojs', 'doi_new', 'doi_old', 'doi_landingpage',
                'unpaywall', 'pm', 'pmc'
    """

    url = db.Column(db.String(512), primary_key=True)
    doi = db.Column(db.String(64), db.ForeignKey('doi.doi'), nullable=False)
    url_type = db.Column(db.String(32))
    date_added = db.Column(db.DateTime(), nullable=False)

    def __init__(self, url, doi, url_type, date_added=None):
        """Init Url."""
        self.url = url
        self.doi = doi
        self.url_type = url_type
        if date_added:
            self.date_added = date_added
        else:
            self.date_added = datetime.now()

    def __repr__(self):
        """Repr."""
        return '<URL {}>'.format(self.url)


class APIRequest(db.Model):
    """NCBIRequest model."""

    id = db.Column(db.Integer, primary_key=True)
    doi = db.Column(db.String(64), db.ForeignKey('doi.doi'), nullable=False)
    request_url = db.Column(db.String(512))
    request_type = db.Column(db.String(32))
    response_content = db.Column(db.Text())
    response_status = db.Column(db.String(32))

    def __init__(self, doi, request_url, request_type, response_content, response_status):
        """Init APIRequest."""
        self.doi = doi
        self.request_url = request_url
        self.request_type = request_type
        self.response_content = response_content
        self.response_status = response_status

    def __repr__(self):
        """Repr."""
        return '<API Request "{}">'.format(self.request_type)


class FBRequest(db.Model):
    """FBRequest model."""

    id = db.Column(db.Integer, primary_key=True)
    url_url = db.Column(db.String(512), db.ForeignKey('url.url'),
                        nullable=False)
    response = db.Column(db.Text())
    reactions = db.Column(db.Integer)
    shares = db.Column(db.Integer)
    comments = db.Column(db.Integer)
    plugin_comments = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime())

    def __init__(self, url, response):
        """Init FBRequest."""
        self.url_url = url
        self.response = json.dumps(response)
        self.reactions = response['engagement']['reaction_count'],
        self.shares = response['engagement']['share_count'],
        self.comments = response['engagement']['comment_count'],
        self.plugin_comments = response['engagement']['comment_plugin_count']
        self.timestamp = datetime.now()

    def __repr__(self):
        """Repr."""
        return '<Facebook Request {}>'.format(self.request)
