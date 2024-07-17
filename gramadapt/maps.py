from clld.web.maps import Map, Layer
from clld.web.adapters.geojson import GeoJson


class LanguagesMap(Map):
    def get_layers(self):
        """Generate the list of layers.

        :return: list or generator of :py:class:`clld.web.maps.Layer` instances.
        """
        route_params = {'ext': 'geojson'}
        route_name = 'languages_alt'
        yield Layer(
            getattr(self.ctx, 'id', 'id'),
            '%s' % self.ctx,
            self.req.route_url(route_name, **route_params))


class ContactsetGeoJson(GeoJson):
    def feature_iterator(self, ctx, req):
        return [ctx.focus_language, ctx.neighbor_language]


class ContactsetMap(Map):
    def get_layers(self):
        yield Layer(
            self.ctx.id,
            self.ctx.name,
            ContactsetGeoJson(self.ctx).render(self.ctx, self.req, dump=False))

    def get_options(self):
        return {'show_labels': True, 'max_zoom': 12}


def includeme(config):
    config.register_map('languages', LanguagesMap)
    config.register_map('contribution', ContactsetMap)
