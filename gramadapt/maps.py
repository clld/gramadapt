from clld.web.maps import Map, Layer


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


def includeme(config):
    config.register_map('languages', LanguagesMap)
