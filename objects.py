from typing import List, Dict, Optional


class Time:
    __slots__ = ["time", "iso8601"]

    def __init__(self, time: int, iso8601: str):
        self.time: int = time
        self.iso8601: str = iso8601


class Name:
    __slots__ = [
        "de_DE",
        "en_GB",
        "en_US",
        "es_ES",
        "es_MX",
        "fr_CA",
        "fr_FR",
        "it_IT",
        "ja_JP",
        "nl_NL",
        "ru_RU",
        "zh_CN",
        "zh_TW",
    ]

    def __init__(
        self,
        de_DE: str,
        en_GB: str,
        en_US: str,
        es_ES: str,
        es_MX: str,
        fr_CA: str,
        fr_FR: str,
        it_IT: str,
        ja_JP: str,
        nl_NL: str,
        ru_RU: str,
        zh_CN: str,
        zh_TW: str,
    ):
        self.de_DE: str = de_DE
        self.en_GB: str = en_GB
        self.en_US: str = en_US
        self.es_ES: str = es_ES
        self.es_MX: str = es_MX
        self.fr_CA: str = fr_CA
        self.fr_FR: str = fr_FR
        self.it_IT: str = it_IT
        self.ja_JP: str = ja_JP
        self.nl_NL: str = nl_NL
        self.ru_RU: str = ru_RU
        self.zh_CN: str = zh_CN
        self.zh_TW: str = zh_TW


class Freshness:
    __slots__ = ["freshness", "title"]

    def __init__(self, freshness: float, title: Dict[str, str]):
        self.freshness: float = freshness
        self.title: Name = Name(**title)


class Gender:
    __slots__ = ["key", "iso5218", "name"]

    def __init__(self, key: str, iso5218: int, name: Dict[str, str]):
        self.key: str = key
        self.iso5218: int = iso5218
        self.name: Name = Name(**name)


class Map:
    __slots__ = ["key", "splatnet", "name", "short_name", "area", "release_at"]

    def __init__(
        self,
        key: str,
        splatnet: int,
        name: Dict[str, str],
        short_name: Dict[str, str],
        area: int,
        release_at: dict,
    ):
        self.key = key
        self.splatnet: int = splatnet
        self.name: Name = Name(**name)
        self.short_name: Name = Name(**short_name)
        self.area: int = area
        self.release_at: Time = Time(**release_at)


class KeyAndName:
    __slots__ = ["key", "name"]

    def __init__(self, key: str, name: Dict[str, str]):
        self.key: str = key
        self.name: Name = Name(**name)


class Rank:
    __slots__ = ["key", "zone", "name"]

    def __init__(self, key: str, zone: dict, name: Dict[str, str]):
        self.key: str = key
        self.zone: KeyAndName = KeyAndName(**zone)
        self.name: Name = Name(**name)


class Weapon_Type:
    __slots__ = ["key", "name", "category"]

    def __init__(self, key: str, name: Dict[str, str], category: dict):
        self.key = key
        self.name: Name = Name(**name)
        self.category: KeyAndName = KeyAndName(**category)


class Weapon:
    __slots__ = [
        "key",
        "splatnet",
        "type",
        "name",
        "sub",
        "special",
        "reskin_of",
        "main_ref",
        "main_power_up",
    ]

    def __init__(
        self,
        key: str,
        splatnet: int,
        type: dict,
        name: Dict[str, str],
        sub: dict,
        special: dict,
        reskin_of: str,
        main_ref: str,
        main_power_up: dict,
    ):
        self.key: str = key
        self.splatnet: int = splatnet
        self.type: Weapon_Type = Weapon_Type(**type)
        self.name: Name = Name(**name)
        self.sub: KeyAndName = KeyAndName(**sub)
        self.special: KeyAndName = KeyAndName(**special)
        self.reskin_of: str = reskin_of
        self.main_ref: str = main_ref
        self.main_power_up: KeyAndName = KeyAndName(**main_power_up)


class Ranked_Rank:
    __slots__ = ["rank_peak", "rank_current", "x_power_peak", "x_power_current"]

    def __init__(
        self, rank_peak: str, rank_current: str, x_power_peak, x_power_current
    ):
        self.rank_peak = rank_peak
        self.rank_current = rank_current
        self.x_power_peak = x_power_peak
        self.x_power_current = x_power_current


class User_Stats_V2_Gachi_Rules:
    __slots__ = ["area", "yagura", "hoko", "asari"]

    def __init__(self, area: dict, yagura: dict, hoko: dict, asari: dict):
        self.arena: Ranked_Rank = Ranked_Rank(**area)
        self.yagura: Ranked_Rank = Ranked_Rank(**yagura)
        self.hoko: Ranked_Rank = Ranked_Rank(**hoko)
        self.asari: Ranked_Rank = Ranked_Rank(**asari)


class User_Stats_V2_Gachi:
    __slots__ = [
        "battles",
        "win_pct",
        "kill_ratio",
        "kill_total",
        "kill_avg",
        "kill_per_min",
        "death_total",
        "death_avg",
        "death_per_min",
        "rules",
    ]

    def __init__(
        self,
        battles: int,
        win_pct: float,
        kill_ratio: float,
        kill_total: int,
        kill_avg: float,
        kill_per_min: float,
        death_total: int,
        death_avg: float,
        death_per_min: float,
        rules: dict,
    ):
        self.battles: int = battles
        self.win_pct: float = win_pct
        self.kill_ratio: float = kill_ratio
        self.kill_total: int = kill_total
        self.kill_avg: float = kill_avg
        self.kill_per_min: float = kill_per_min
        self.death_total: int = death_total
        self.death_avg: float = death_avg
        self.death_per_min: float = death_per_min
        self.rules: User_Stats_V2_Gachi_Rules = User_Stats_V2_Gachi_Rules(**rules)


class User_Stats_V2_Nawabari:
    __slots__ = [
        "battles",
        "win_pct",
        "kill_ratio",
        "kill_total",
        "kill_avg",
        "kill_per_min",
        "death_total",
        "death_avg",
        "death_per_min",
        "total_inked",
        "max_inked",
        "avg_inked",
    ]

    def __init__(
        self,
        battles: int,
        win_pct: float,
        kill_ratio: float,
        kill_total: float,
        kill_avg: float,
        kill_per_min: float,
        death_total: int,
        death_avg: float,
        death_per_min: float,
        total_inked: int,
        max_inked: int,
        avg_inked: float,
    ):
        self.battles: int = battles
        self.win_pct: float = win_pct
        self.kill_ratio: float = kill_ratio
        self.kill_total: float = kill_total
        self.kill_avg: float = kill_avg
        self.kill_per_min: float = kill_per_min
        self.death_total: int = death_total
        self.death_avg: float = death_avg
        self.death_per_min: float = death_per_min
        self.total_inked: int = total_inked
        self.max_inked: int = max_inked
        self.avg_inked: float = avg_inked


class User_Stats_V2_Entire:
    __slots__ = [
        "battles",
        "win_pct",
        "kill_ratio",
        "kill_total",
        "kill_avg",
        "kill_per_min",
        "death_total",
        "death_avg",
        "death_per_min",
    ]

    def __init__(
        self,
        battles: int,
        win_pct: float,
        kill_ratio: float,
        kill_total: int,
        kill_avg: float,
        kill_per_min: float,
        death_total: int,
        death_avg: float,
        death_per_min: float,
    ):
        self.battles: int = battles
        self.win_pct: float = win_pct
        self.kill_ratio: float = kill_ratio
        self.kill_total: int = kill_total
        self.kill_avg: float = kill_avg
        self.kill_per_min: float = kill_per_min
        self.death_total: int = death_total
        self.death_avg: float = death_avg
        self.death_per_min: float = death_per_min


class User_Stats_V2:
    __slots__ = ["updated_at", "entire", "nawabari", "gachi"]

    def __init__(self, updated_at: dict, entire: dict, nawabari: dict, gachi: dict):
        self.updated_at: Time = Time(**updated_at)
        self.entire: User_Stats_V2_Entire = User_Stats_V2_Entire(**entire)
        self.nawabari: User_Stats_V2_Nawabari = User_Stats_V2_Nawabari(**nawabari)
        self.gachi: User_Stats_V2_Gachi = User_Stats_V2_Gachi(**gachi)


class User_Stats:
    __slots__ = ["v1", "v2"]

    def __init__(self, v1, v2: dict):
        self.v1 = v1
        self.v2: User_Stats_V2 = User_Stats_V2(**v2)


class User_Profile:
    __slots__ = [
        "nnid",
        "friend_code",
        "twitter",
        "ikanakama",
        "ikanakama2",
        "environment",
    ]

    def __init__(
        self,
        nnid: str,
        friend_code: str,
        twitter: str,
        ikanakama: str,
        ikanakama2: str,
        environment: str,
    ):
        self.nnid: str = nnid
        self.friend_code: str = friend_code
        self.twitter: str = twitter
        self.ikanakama: str = ikanakama
        self.ikanakama2: str = ikanakama2
        self.environment: str = environment


class User:
    __slots__ = [
        "id",
        "name",
        "screen_name",
        "url",
        "join_at",
        "profile",
        "stat",
        "stats",
    ]

    def __init__(
        self,
        id: int,
        name: str,
        screen_name: str,
        url: str,
        join_at: dict,
        profile: dict,
        stat,
        stats: dict,
    ):
        self.id: int = id
        self.name: str = name
        self.screen_name: str = screen_name
        self.url: str = url
        self.join_at: Time = Time(**join_at)
        self.profile: User_Profile = User_Profile(**profile)
        self.stat = stat
        self.stats = stats


class Brand:
    __slots__ = ["key", "name", "strength", "weakness"]

    def __init__(
        self,
        key: str,
        name: Dict[str, str],
        strength: Optional[dict],
        weakness: Optional[dict],
    ):
        self.key: str = key
        self.name: Name = Name(**name)
        if strength is not None:
            self.strength: Optional[KeyAndName] = KeyAndName(**strength)
        else:
            self.strength = None
        if weakness is not None:
            self.weakness: Optional[KeyAndName] = KeyAndName(**weakness)
        else:
            self.weakness = None


class Gears_Gear_Gear:
    __slots__ = ["key", "type", "brand", "name", "primary_ability", "splatnet"]

    def __init__(
        self,
        key: str,
        type: dict,
        brand: dict,
        name: Dict[str, str],
        primary_ability: Optional[dict],
        splatnet: int,
    ):
        self.key: str = key
        self.type: KeyAndName = KeyAndName(**type)
        self.brand: Brand = Brand(**brand)
        self.name: Name = Name(**name)
        if primary_ability is not None:
            self.primary_ability: Optional[KeyAndName] = KeyAndName(**primary_ability)
        else:
            self.primary_ability = None
        self.splatnet: int = splatnet


class Gears_Gear:
    __slots__ = ["gear", "primary_ability", "secondary_abilities"]

    def __init__(
        self,
        gear: Optional[dict],
        primary_ability: Optional[dict],
        secondary_abilities: Optional[List[dict]],
    ):
        if gear is not None:
            self.gear: Optional[Gears_Gear_Gear] = Gears_Gear_Gear(**gear)
        else:
            self.gear = None
        if primary_ability is not None:
            self.primary_ability: Optional[KeyAndName] = KeyAndName(**primary_ability)
        else:
            self.primary_ability = None
        self.secondary_abilities: Optional[List[KeyAndName]] = []
        if secondary_abilities is not None:
            for ability in secondary_abilities:
                if ability is not None:
                    self.secondary_abilities.append(KeyAndName(**ability))
        else:
            self.secondary_abilities = None


class Gears:
    __slots__ = ["headgear", "clothing", "shoes"]

    def __init__(
        self, headgear: Optional[dict], clothing: Optional[dict], shoes: Optional[dict]
    ):
        if headgear is not None:
            self.headgear: Optional[Gears_Gear] = Gears_Gear(**headgear)
        else:
            self.headgear = None
        if clothing is not None:
            self.clothing: Optional[Gears_Gear] = Gears_Gear(**clothing)
        else:
            self.clothing = None
        if shoes is not None:
            self.shoes: Optional[Gears_Gear] = Gears_Gear(**shoes)
        else:
            self.shoes = None


class Player:
    __slots__ = [
        "team",
        "is_me",
        "weapon",
        "level",
        "rank",
        "star_rank",
        "rank_in_team",
        "kill",
        "death",
        "kill_or_assist",
        "special",
        "my_kill",
        "point",
        "name",
        "species",
        "gender",
        "fest_title",
        "splatnet_id",
        "top_500",
        "icon",
    ]

    def __init__(
        self,
        team: str,
        is_me: bool,
        weapon: Optional[dict],
        level: int,
        rank: Optional[dict],
        star_rank: int,
        rank_in_team: Optional[int],
        kill: int,
        death: int,
        kill_or_assist: int,
        special: int,
        my_kill,
        point: int,
        name: str,
        species: Optional[dict],
        gender: Optional[dict],
        fest_title,
        splatnet_id: str,
        top_500: Optional[bool],
        icon: str,
    ):
        self.team: str = team
        self.is_me: bool = is_me
        if weapon is not None:
            self.weapon: Optional[Weapon] = Weapon(**weapon)
        else:
            self.weapon = None
        self.level: int = level
        if rank is not None:
            self.rank: Optional[Rank] = Rank(**rank)
        else:
            self.rank = None
        self.star_rank: int = star_rank
        self.rank_in_team: Optional[int] = rank_in_team
        self.kill: int = kill
        self.death: int = death
        self.kill_or_assist: int = kill_or_assist
        self.special: int = special
        self.my_kill = my_kill
        self.point: int = point
        self.name: str = name
        if species is not None:
            self.species: Optional[KeyAndName] = KeyAndName(**species)
        else:
            self.species = None
        if gender is not None:
            self.gender: Optional[Gender] = Gender(**gender)
        else:
            self.gender = None
        self.fest_title = fest_title
        self.splatnet_id: str = splatnet_id
        self.top_500: Optional[bool] = top_500
        self.icon: str = icon


class Agent:
    __slots__ = [
        "name",
        "version",
        "game_version",
        "game_version_date",
        "custom",
        "variables",
    ]

    def __init__(
        self,
        name: str,
        version: str,
        game_version,
        game_version_date,
        custom,
        variables: Dict[str, str],
    ):
        self.name: str = name
        self.version: str = version
        self.game_version = game_version
        self.game_version_date = game_version_date
        self.custom = custom
        if variables is not None:
            self.variables: Optional[dict] = variables
        else:
            self.variables = None


class Battle:
    __slots__ = [
        "id",
        "splatnet_number",
        "url",
        "user",
        "lobby",
        "mode",
        "rule",
        "map",
        "weapon",
        "freshness",
        "rank",
        "rank_exp",
        "rank_after",
        "rank_exp_after",
        "x_power",
        "x_power_after",
        "estimate_x_power",
        "level",
        "level_after",
        "star_rank",
        "result",
        "knock_out",
        "rank_in_team",
        "kill",
        "death",
        "kill_or_assist",
        "special",
        "kill_ratio",
        "kill_rate",
        "max_kill_combo",
        "max_kill_streak",
        "death_reasons",
        "my_point",
        "estimate_gachi_power",
        "league_point",
        "my_team_estimate_league_point",
        "his_team_estimate_league_point",
        "my_team_point",
        "his_team_point",
        "my_team_percent",
        "his_team_percent",
        "my_team_count",
        "his_team_count",
        "my_team_id",
        "his_team_id",
        "species",
        "gender",
        "fest_title",
        "fest_exp",
        "fest_title_after",
        "fest_exp_after",
        "fest_power",
        "my_team_estimate_fest_power",
        "his_team_my_team_estimate_fest_power",
        "my_team_fest_theme",
        "his_team_fest_theme",
        "my_team_nickname",
        "his_team_nickname",
        "clout",
        "total_clout",
        "total_clout_after",
        "my_team_win_streak",
        "his_team_win_streak",
        "synergy_bonus",
        "special_battle",
        "image_judge",
        "image_result",
        "image_gear",
        "gears",
        "period",
        "period_range",
        "players",
        "events",
        "splatnet_json",
        "agent",
        "automated",
        "environment",
        "link_url",
        "note",
        "game_version",
        "nawabari_bonus",
        "start_at",
        "end_at",
        "register_at",
    ]

    def __init__(
        self,
        id: int,
        splatnet_number: int,
        url: str,
        user: dict,
        lobby: Optional[dict],
        mode: Optional[dict],
        rule: Optional[dict],
        map: Optional[dict],
        weapon: Optional[dict],
        freshness: Optional[dict],
        rank: Optional[dict],
        rank_exp,
        rank_after: Optional[dict],
        rank_exp_after,
        x_power,
        x_power_after,
        estimate_x_power,
        level: int,
        level_after: int,
        star_rank: int,
        result: str,
        knock_out: bool,
        rank_in_team: Optional[int],
        kill: int,
        death: int,
        kill_or_assist: int,
        special: int,
        kill_ratio: float,
        kill_rate: float,
        max_kill_combo,
        max_kill_streak,
        death_reasons: list,
        my_point: int,
        estimate_gachi_power: Optional[int],
        league_point,
        my_team_estimate_league_point,
        his_team_estimate_league_point,
        my_team_point,
        his_team_point,
        my_team_percent: Optional[str],
        his_team_percent: Optional[str],
        my_team_count: Optional[int],
        his_team_count: Optional[int],
        my_team_id,
        his_team_id,
        species: Optional[dict],
        gender: Optional[dict],
        fest_title: Optional[dict],
        fest_exp: Optional[int],
        fest_title_after: Optional[dict],
        fest_exp_after: Optional[int],
        fest_power: Optional[str],
        my_team_estimate_fest_power: Optional[int],
        his_team_my_team_estimate_fest_power: Optional[int],
        my_team_fest_theme: Optional[str],
        his_team_fest_theme: Optional[str],
        my_team_nickname,
        his_team_nickname,
        clout: Optional[int],
        total_clout: Optional[int],
        total_clout_after: Optional[int],
        my_team_win_streak: Optional[int],
        his_team_win_streak: Optional[int],
        synergy_bonus: Optional[float],
        special_battle,
        image_judge,
        image_result: str,
        image_gear: Optional[str],
        gears: dict,
        period: int,
        period_range: str,
        players: Optional[List[dict]],
        events,
        splatnet_json,
        agent: dict,
        automated: bool,
        environment,
        link_url: Optional[str],
        note,
        game_version: str,
        nawabari_bonus: Optional[int],
        start_at: Optional[dict],
        end_at: Optional[dict],
        register_at: dict,
    ):
        self.id: int = id
        self.splatnet_number: int = splatnet_number
        self.url: str = url
        self.user: User = User(**user)
        if lobby is not None:
            self.lobby: Optional[KeyAndName] = KeyAndName(**lobby)
        else:
            self.lobby = None
        if mode is not None:
            self.mode: Optional[KeyAndName] = KeyAndName(**mode)
        else:
            self.mode = None
        if rule is not None:
            self.rule: Optional[KeyAndName] = KeyAndName(**rule)
        else:
            self.rule = None
        if map is not None:
            self.map: Optional[Map] = Map(**map)
        else:
            self.map = None
        if weapon is not None:
            self.weapon: Optional[Weapon] = Weapon(**weapon)
        else:
            self.weapon = None
        if freshness is not None:
            self.freshness: Optional[Freshness] = Freshness(**freshness)
        else:
            self.freshness = None
        if rank is not None:
            self.rank: Optional[Rank] = Rank(**rank)
        else:
            self.rank = None
        self.rank_exp = rank_exp
        if rank_after is not None:
            self.rank_after: Optional[Rank] = Rank(**rank_after)
        else:
            self.rank_after = None
        self.rank_exp_after = rank_exp_after
        self.x_power = x_power
        self.x_power_after = x_power_after
        self.estimate_x_power = estimate_x_power
        self.level: int = level
        self.level_after: int = level_after
        self.star_rank: int = star_rank
        self.result: str = result
        self.knock_out: bool = knock_out
        self.rank_in_team: Optional[int] = rank_in_team
        self.kill: int = kill
        self.death: int = death
        self.kill_or_assist: int = kill_or_assist
        self.special: int = special
        self.kill_ratio: float = kill_ratio
        self.kill_rate: float = kill_rate
        self.max_kill_combo = max_kill_combo
        self.max_kill_streak = max_kill_streak
        self.death_reasons = death_reasons
        self.my_point: int = my_point
        self.estimate_gachi_power: Optional[int] = estimate_gachi_power
        self.league_point = league_point
        self.my_team_estimate_league_point = my_team_estimate_league_point
        self.his_team_estimate_league_point = his_team_estimate_league_point
        self.my_team_point = my_team_point
        self.his_team_point = his_team_point
        self.my_team_percent: Optional[str] = my_team_percent
        self.his_team_percent: Optional[str] = his_team_percent
        self.my_team_count: Optional[int] = my_team_count
        self.his_team_count: Optional[int] = his_team_count
        self.my_team_id = my_team_id
        self.his_team_id = his_team_id
        if species is not None:
            self.species: Optional[KeyAndName] = KeyAndName(**species)
        else:
            self.species = None
        if gender is not None:
            self.gender: Optional[Gender] = Gender(**gender)
        else:
            self.gender = None
        if fest_title is not None:
            self.fest_title: Optional[KeyAndName] = KeyAndName(**fest_title)
        else:
            self.fest_title = None
        self.fest_exp: Optional[int] = fest_exp
        if fest_title_after is not None:
            self.fest_title_after: Optional[KeyAndName] = KeyAndName(**fest_title_after)
        else:
            self.fest_title_after = None
        self.fest_exp_after: Optional[int] = fest_exp_after
        self.fest_power: Optional[str] = fest_power
        self.my_team_estimate_fest_power: Optional[int] = my_team_estimate_fest_power
        self.his_team_my_team_estimate_fest_power: Optional[
            int
        ] = his_team_my_team_estimate_fest_power
        self.my_team_fest_theme: Optional["str"] = my_team_fest_theme
        self.his_team_fest_theme: Optional["str"] = his_team_fest_theme
        self.my_team_nickname = my_team_nickname
        self.his_team_nickname = his_team_nickname
        self.clout: Optional[int] = clout
        self.total_clout: Optional[int] = total_clout
        self.total_clout_after: Optional[int] = total_clout_after
        self.my_team_win_streak: Optional[int] = my_team_win_streak
        self.his_team_win_streak: Optional[int] = his_team_win_streak
        self.synergy_bonus: Optional[float] = synergy_bonus
        self.special_battle = special_battle
        self.image_judge = image_judge
        self.image_result: str = image_result
        self.image_gear: Optional[str] = image_gear
        self.gears: Gears = Gears(**gears)
        self.period: int = period
        self.period_range: str = period_range
        self.players: Optional[List[Player]] = []
        if players is not None:
            for player in players:
                self.players.append(Player(**player))
        else:
            self.players = None
        self.events = events
        self.splatnet_json = splatnet_json
        self.agent: Agent = Agent(**agent)
        self.automated: bool = automated
        self.environment = environment
        self.link_url: Optional[str] = link_url
        self.note = note
        self.game_version: str = game_version
        self.nawabari_bonus: Optional[int] = nawabari_bonus
        if start_at is not None:
            self.start_at: Optional[Time] = Time(**start_at)
        else:
            self.start_at = None
        if end_at is not None:
            self.end_at: Optional[Time] = Time(**end_at)
        else:
            self.end_at = None
        self.register_at: Time = Time(**register_at)
