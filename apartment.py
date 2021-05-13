from scipy.interpolate import interp1d


class Apartment:
    def __init__(self, hallways, floors, flats, lifts_per_hallway, lift_power):
        self._hallways = hallways
        self._flats = flats
        self._floors = floors
        self._lifts = lifts_per_hallway * hallways
        self._lift_power = lift_power
        self._k_s_l: float = 0.
        self._p_kv_ud: float = 0.
        self._k_y = 0.9
        self._p_p_kv: float = 0.
        self._p_pl: float = 0.
        self._p_p_zh_zd: float = 0.
        self.compute()

    def compute(self):
        self._get_p_kv_ud()
        self._get_p_p_kv()

        self._get_k_s_l()

        self._get_p_rl()
        self._get_p_p_zh_zd()

    def _get_k_s_l(self):
        x = [2, 3, 4, 5, 6, 10, 20, 25]
        y_up_to = [0.8, 0.8, 0.7, 0.7, 0.65, 0.5, 0.4, 0.35]
        y_above = [0.9, 0.9, 0.8, 0.8, 0.75, 0.6, 0.5, 0.4]
        if 1 <= self._floors < 12:
            f = interp1d(x, y_up_to, kind='linear')
        elif self._floors >= 12:
            f = interp1d(x, y_above, kind='linear')
        self._k_s_l = (f(self._floors)).item()

    def _get_p_kv_ud(self):
        x = [100, 200, 400]
        y = [0.85, 1.36, 1.27]
        f = interp1d(x, y, kind='linear')
        self._p_kv_ud = (f(self._flats)).item()

    def _get_p_p_kv(self):
        self._p_p_kv = self._p_kv_ud * self._flats

    def _get_p_rl(self):
        self._p_pl = self._k_s_l * self._lifts * self._lift_power

    def _get_p_p_zh_zd(self):
        self._p_p_zh_zd = self._p_p_kv + self._k_y * self._p_pl

    @property
    def k_s_l(self):
        return self.k_s_l

    @property
    def p_kv_ud(self):
        return self._p_kv_ud

    @property
    def p_p_kv(self):
        return self._p_p_kv

    @property
    def p_pl(self):
        return self._p_pl

    @property
    def p_p_zh_zd(self):
        return self._p_p_zh_zd
