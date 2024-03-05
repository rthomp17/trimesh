try:
    from . import generic as g
except BaseException:
    import generic as g


class BooleanTest(g.unittest.TestCase):

    def setUp(self):
        self.a = g.get_mesh('ballA.off')
        self.b = g.get_mesh('ballB.off')
        self.truth = g.data['boolean']

    def is_zero(self, value):
        return abs(value) < .001

    def test_boolean(self):
        a, b = self.a, self.b

        engines = [('blender', g.trimesh.interfaces.blender.exists),
                   ('scad', g.trimesh.interfaces.scad.exists)]

        for engine, exists in engines:
            # if we have all_dep set it means we should fail if
            # engine is not installed so don't continue
            if not exists:
                g.log.warning('skipping boolean engine %s', engine)
                continue

            g.log.info('Testing boolean ops with engine %s', engine)
            ab = a.difference(b, engine=engine)
            assert ab.is_volume
            assert self.is_zero(
                ab.volume - self.truth['difference'])

            assert g.np.allclose(
                ab.bounds[0],
                a.bounds[0])

            ba = b.difference(a, engine=engine)
            assert ba.is_volume
            assert self.is_zero(
                ba.volume - self.truth['difference'])

            assert g.np.allclose(
                ba.bounds[1],
                b.bounds[1])

            i = a.intersection(b, engine=engine)
            assert i.is_volume
            assert self.is_zero(
                i.volume - self.truth['intersection'])

            u = a.union(b, engine=engine)
            assert u.is_volume
            assert self.is_zero(u.volume - self.truth['union'])

            g.log.info('booleans succeeded with %s', engine)

    def test_multiple(self):
        """
        Make sure boolean operations work on multiple meshes.
        """
        engines = [
            ('blender', g.trimesh.interfaces.blender.exists),
            ('scad', g.trimesh.interfaces.scad.exists)]
        for _engine, exists in engines:
            if not exists:
                continue
            a = g.trimesh.primitives.Sphere(center=[0, 0, 0])
            b = g.trimesh.primitives.Sphere(center=[0, 0, .75])
            c = g.trimesh.primitives.Sphere(center=[0, 0, 1.5])

            r = g.trimesh.boolean.union([a, b, c])

            assert r.is_volume
            assert r.body_count == 1
            assert g.np.isclose(r.volume,
                                8.617306056726884)

    def test_empty(self):
        engines = [
            ('blender', g.trimesh.interfaces.blender.exists),
            ('scad', g.trimesh.interfaces.scad.exists)]
        for engine, exists in engines:
            if not exists:
                continue

            a = g.trimesh.primitives.Sphere(center=[0, 0, 0])
            b = g.trimesh.primitives.Sphere(center=[5, 0, 0])

            i = a.intersection(b, engine=engine)

            assert i.is_empty


if __name__ == '__main__':
    g.trimesh.util.attach_to_log()
    g.unittest.main()
