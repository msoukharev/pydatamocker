import pydatamocker.generators.datetime as datetime
import pydatamocker.generators.numeric as numeric
import pydatamocker.generators.dataset as dataset
import pydatamocker.generators.enum as enum
from pydatamocker.types import ColumnGenerator, FieldParams
from pydatamocker.util.switch import switch


def get_generator(params: FieldParams) -> ColumnGenerator:
    type_ = params['type']
    return switch(type_,
        {
            'dataset': dataset.create,
            'integer': numeric.from_numeric,
            'float': numeric.from_numeric,
            'datetime': datetime.create,
            'enum': enum.create
        }
    )(params)
