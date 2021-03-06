import logging
import traceback

from flask_restplus import Api
from biolink import settings
from sqlalchemy.orm.exc import NoResultFound

log = logging.getLogger(__name__)

api = Api(version='0.1.1', title='Gene Ontology API',
          license='BSD3',
          contact='laurent.albou@lbl.gov',
          description='Gene Ontology API based on the BioLink Model, an integration layer for linked biological objects.\n\n __Source:__ https://github.com/geneontology/biolink-api')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404
