# Strategy: Use the inspected Pipe-16 HybridOpening controller. Reassign idle workers during the first three days to plant, water and harvest one temporary wheat crop, then restore the planned pasture and deliver the wheat. Preserve the public Metav4 production and market controller. This is attributed reuse, and its stronger public source still needs live confirmation. Disable optional environment-dependent external library loading so the archive is self-contained.
# Local packaging modifications, 2026-09-20. Original attribution retained.
# Kaggriculture submission v9/3: public V39 (Apache-2.0, notices below) plus the v9 layers
# RACEPX gate, RACE (reservation from step 192, horizon 40 / margin 12), COURIER, CARROT and HERD
# appended at the end of this file.
# EXP-173 isolate opening market sequence inspired by yhay81/shop-router-0911-simple (Apache-2.0).
# Kaggriculture EXP-167 candidate. Not submitted automatically.
# Attribution: thomastschinkel, yhay81, destbreso, aurax7, tetsutani,
# prvsiyan and Dmitrii Gluzdov. Apache-2.0 derivations; notices retained below.
# Kaggriculture v31 / EXP-157, Ahmed Berat Ozer, September 9 2026.
# Selected mechanism: crop_public_order. New independent confirmation is required.
# Public V221B/V224C production/timing lineage: prvsiyan, Apache-2.0.
# Original economics and integration; retained upstream licenses follow.
# Kaggriculture v28 / EXP-154, Ahmed Berat Ozer, September 9 2026.
# Changes: aurax7 day-end storage guard; Dmitrii Gluzdov physical terminal rescue
# adapted to v27, with 64 deterministic simulations. Apache-2.0.
# New action tapes and ordered shop-pair map: yhay81/shop-router-0909, Apache-2.0.
# Kaggriculture v25, EXP-149: Shop0908 production, sale lead, terminal cargo rescue.
# Runtime chassis: Apache-2.0; thomastschinkel, yhay81, tetsutani.
# Routing and public action data: yhay81/shop-router-0908, frozen September 8, 2026.
# 
#                                  Apache License
#                            Version 2.0, January 2004
#                         http://www.apache.org/licenses/
# 
#    TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION
# 
#    1. Definitions.
# 
#       "License" shall mean the terms and conditions for use, reproduction,
#       and distribution as defined by Sections 1 through 9 of this document.
# 
#       "Licensor" shall mean the copyright owner or entity authorized by
#       the copyright owner that is granting the License.
# 
#       "Legal Entity" shall mean the union of the acting entity and all
#       other entities that control, are controlled by, or are under common
#       control with that entity. For the purposes of this definition,
#       "control" means (i) the power, direct or indirect, to cause the
#       direction or management of such entity, whether by contract or
#       otherwise, or (ii) ownership of fifty percent (50%) or more of the
#       outstanding shares, or (iii) beneficial ownership of such entity.
# 
#       "You" (or "Your") shall mean an individual or Legal Entity
#       exercising permissions granted by this License.
# 
#       "Source" form shall mean the preferred form for making modifications,
#       including but not limited to software source code, documentation
#       source, and configuration files.
# 
#       "Object" form shall mean any form resulting from mechanical
#       transformation or translation of a Source form, including but
#       not limited to compiled object code, generated documentation,
#       and conversions to other media types.
# 
#       "Work" shall mean the work of authorship, whether in Source or
#       Object form, made available under the License, as indicated by a
#       copyright notice that is included in or attached to the work
#       (an example is provided in the Appendix below).
# 
#       "Derivative Works" shall mean any work, whether in Source or Object
#       form, that is based on (or derived from) the Work and for which the
#       editorial revisions, annotations, elaborations, or other modifications
#       represent, as a whole, an original work of authorship. For the purposes
#       of this License, Derivative Works shall not include works that remain
#       separable from, or merely link (or bind by name) to the interfaces of,
#       the Work and Derivative Works thereof.
# 
#       "Contribution" shall mean any work of authorship, including
#       the original version of the Work and any modifications or additions
#       to that Work or Derivative Works thereof, that is intentionally
#       submitted to Licensor for inclusion in the Work by the copyright owner
#       or by an individual or Legal Entity authorized to submit on behalf of
#       the copyright owner. For the purposes of this definition, "submitted"
#       means any form of electronic, verbal, or written communication sent
#       to the Licensor or its representatives, including but not limited to
#       communication on electronic mailing lists, source code control systems,
#       and issue tracking systems that are managed by, or on behalf of, the
#       Licensor for the purpose of discussing and improving the Work, but
#       excluding communication that is conspicuously marked or otherwise
#       designated in writing by the copyright owner as "Not a Contribution."
# 
#       "Contributor" shall mean Licensor and any individual or Legal Entity
#       on behalf of whom a Contribution has been received by Licensor and
#       subsequently incorporated within the Work.
# 
#    2. Grant of Copyright License. Subject to the terms and conditions of
#       this License, each Contributor hereby grants to You a perpetual,
#       worldwide, non-exclusive, no-charge, royalty-free, irrevocable
#       copyright license to reproduce, prepare Derivative Works of,
#       publicly display, publicly perform, sublicense, and distribute the
#       Work and such Derivative Works in Source or Object form.
# 
#    3. Grant of Patent License. Subject to the terms and conditions of
#       this License, each Contributor hereby grants to You a perpetual,
#       worldwide, non-exclusive, no-charge, royalty-free, irrevocable
#       (except as stated in this section) patent license to make, have made,
#       use, offer to sell, sell, import, and otherwise transfer the Work,
#       where such license applies only to those patent claims licensable
#       by such Contributor that are necessarily infringed by their
#       Contribution(s) alone or by combination of their Contribution(s)
#       with the Work to which such Contribution(s) was submitted. If You
#       institute patent litigation against any entity (including a
#       cross-claim or counterclaim in a lawsuit) alleging that the Work
#       or a Contribution incorporated within the Work constitutes direct
#       or contributory patent infringement, then any patent licenses
#       granted to You under this License for that Work shall terminate
#       as of the date such litigation is filed.
# 
#    4. Redistribution. You may reproduce and distribute copies of the
#       Work or Derivative Works thereof in any medium, with or without
#       modifications, and in Source or Object form, provided that You
#       meet the following conditions:
# 
#       (a) You must give any other recipients of the Work or
#           Derivative Works a copy of this License; and
# 
#       (b) You must cause any modified files to carry prominent notices
#           stating that You changed the files; and
# 
#       (c) You must retain, in the Source form of any Derivative Works
#           that You distribute, all copyright, patent, trademark, and
#           attribution notices from the Source form of the Work,
#           excluding those notices that do not pertain to any part of
#           the Derivative Works; and
# 
#       (d) If the Work includes a "NOTICE" text file as part of its
#           distribution, then any Derivative Works that You distribute must
#           include a readable copy of the attribution notices contained
#           within such NOTICE file, excluding those notices that do not
#           pertain to any part of the Derivative Works, in at least one
#           of the following places: within a NOTICE text file distributed
#           as part of the Derivative Works; within the Source form or
#           documentation, if provided along with the Derivative Works; or,
#           within a display generated by the Derivative Works, if and
#           wherever such third-party notices normally appear. The contents
#           of the NOTICE file are for informational purposes only and
#           do not modify the License. You may add Your own attribution
#           notices within Derivative Works that You distribute, alongside
#           or as an addendum to the NOTICE text from the Work, provided
#           that such additional attribution notices cannot be construed
#           as modifying the License.
# 
#       You may add Your own copyright statement to Your modifications and
#       may provide additional or different license terms and conditions
#       for use, reproduction, or distribution of Your modifications, or
#       for any such Derivative Works as a whole, provided Your use,
#       reproduction, and distribution of the Work otherwise complies with
#       the conditions stated in this License.
# 
#    5. Submission of Contributions. Unless You explicitly state otherwise,
#       any Contribution intentionally submitted for inclusion in the Work
#       by You to the Licensor shall be under the terms and conditions of
#       this License, without any additional terms or conditions.
#       Notwithstanding the above, nothing herein shall supersede or modify
#       the terms of any separate license agreement you may have executed
#       with Licensor regarding such Contributions.
# 
#    6. Trademarks. This License does not grant permission to use the trade
#       names, trademarks, service marks, or product names of the Licensor,
#       except as required for reasonable and customary use in describing the
#       origin of the Work and reproducing the content of the NOTICE file.
# 
#    7. Disclaimer of Warranty. Unless required by applicable law or
#       agreed to in writing, Licensor provides the Work (and each
#       Contributor provides its Contributions) on an "AS IS" BASIS,
#       WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
#       implied, including, without limitation, any warranties or conditions
#       of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
#       PARTICULAR PURPOSE. You are solely responsible for determining the
#       appropriateness of using or redistributing the Work and assume any
#       risks associated with Your exercise of permissions under this License.
# 
#    8. Limitation of Liability. In no event and under no legal theory,
#       whether in tort (including negligence), contract, or otherwise,
#       unless required by applicable law (such as deliberate and grossly
#       negligent acts) or agreed to in writing, shall any Contributor be
#       liable to You for damages, including any direct, indirect, special,
#       incidental, or consequential damages of any character arising as a
#       result of this License or out of the use or inability to use the
#       Work (including but not limited to damages for loss of goodwill,
#       work stoppage, computer failure or malfunction, or any and all
#       other commercial damages or losses), even if such Contributor
#       has been advised of the possibility of such damages.
# 
#    9. Accepting Warranty or Additional Liability. While redistributing
#       the Work or Derivative Works thereof, You may choose to offer,
#       and charge a fee for, acceptance of support, warranty, indemnity,
#       or other liability obligations and/or rights consistent with this
#       License. However, in accepting such obligations, You may act only
#       on Your own behalf and on Your sole responsibility, not on behalf
#       of any other Contributor, and only if You agree to indemnify,
#       defend, and hold each Contributor harmless for any liability
#       incurred by, or claims asserted against, such Contributor by reason
#       of your accepting any such warranty or additional liability.
# 
#    END OF TERMS AND CONDITIONS
# 
#    APPENDIX: How to apply the Apache License to your work.
# 
#       To apply the Apache License to your work, attach the following
#       boilerplate notice, with the fields enclosed by brackets "[]"
#       replaced with your own identifying information. (Don't include
#       the brackets!)  The text should be enclosed in the appropriate
#       comment syntax for the file format. We also recommend that a
#       file or class name and description of purpose be included on the
#       same "printed page" as the copyright notice for easier
#       identification within third-party archives.
# 
#    Copyright [yyyy] [name of copyright owner]
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
"""Kaggriculture route-replay chassis (pure Python, stdlib only).

A *route* is a pre-computed tape of 719 Kaggle-format actions
``{"farmer": [op, ...], "hands": [[op, ...], ...], "market": [[order, item, qty], ...]}``.
The chassis replays the tape chosen by a caller-supplied ``router`` and wraps it
in small reactive layers (each independently switchable via ``settings``):

    hand_align            pad/truncate hands to the real hand count      (fieldbook_logic)
    weed_repair           DIG a weed that blocks PLANT/BUILD, replay      (tetsutani + task spec)
    sell_lead             sell next step's lots one step early            (fieldbook _lead_sale)
    front_run             sell before the opponent's scheduled SELL       (hook; opponent_plan)
    budget_guard          fund each 72-step block's purchases             (six_day_budget_guard.hpp)
    room_guard            keep shed <= 99 at hour 23                      (tetsutani)
    clamp_sells           trim SELL orders to the projected shed          (tetsutani)
    dead_stock            sell stock the route will never sell            (tetsutani)
    terminal_liquidation  step >= 718: sell the whole projected shed      (fieldbook _terminal_sale)

Engine facts (verified against kaggle_environments 1.32.7, env_1_32_7.py):
  observation["farms"][p] = {"money", "tiles"[y][x], "farmer"[x,y], "hands"[[x,y]..],
                             "unlocked_quadrants", "hires_today"}
  tiles: None (empty) | "LOCKED" | {"kind": WEED|COOP|PASTURE|PLANT, "crop"/"animal", ...}
  observation["private"] = {"shed": {item: n}, "seeds": {crop: n}, "inventories": [{}...]}
  observation["market"] = {"inventory": {...}, "prices": {...}}
  observation["town"] = {"unlocked_shops": [...]}
  Agents act on steps 0..718 (interpreter marks DONE once step >= episodeSteps-2).
"""
from __future__ import annotations

import copy

PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER")
SEED_PRICE = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50, "STRAWBERRY": 100, "MELON": 80}
ANIMAL_COST = {"GOOSE": 300, "COW": 400, "SHEEP": 500}
ANIMAL_STRUCTURE = {"GOOSE": "COOP", "COW": "PASTURE", "SHEEP": "PASTURE"}
LAND_PRICES = (1000, 2000, 4000)
MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
FRONT_RUN_ITEMS = ("MILK", "WOOL", "STRAWBERRY", "MELON")
LAST_ACT_STEP = 718
PASS_ACTION = {"farmer": ["PASS"], "hands": [], "market": []}

DEFAULT_SETTINGS = {
    "hand_align": True,
    "weed_repair": True,
    "sell_lead": True,
    "front_run": True,
    "budget_guard": True,
    "room_guard": True,
    "clamp_sells": True,
    "dead_stock": True,
    "terminal_liquidation": True,
    # tunables
    "block_turns": 72,
    "shed_capacity": 100,
    "board_size": 10,
    "max_orders": 10,
    "turns_per_day": 24,
    "min_sell_price": 2,
}


# --------------------------------------------------------------------------- helpers
def _get(value, key, default=None):
    """Field access that works for dicts and Kaggle Struct/attribute objects."""
    if isinstance(value, dict):
        return value.get(key, default)
    getter = getattr(value, "get", None)
    if callable(getter):
        return getter(key, default)
    return getattr(value, key, default)


def _int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _fib(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def _step_of(observation):
    raw = _get(observation, "step")
    if raw is not None:
        return _int(raw)
    return _int(_get(observation, "day", 0)) * 24 + _int(_get(observation, "hour", 0))


def _shed_adjacent(pos, board):
    if not isinstance(pos, (list, tuple)) or len(pos) < 2:
        return False
    half = board // 2
    return pos[0] in (half - 1, half) and pos[1] in (half - 1, half)


def _tile_at(tiles, pos):
    try:
        x, y = int(pos[0]), int(pos[1])
        return tiles[y][x]
    except (TypeError, ValueError, IndexError):
        return "LOCKED"


def _is_noop(act, tile, inv, seeds, pos, board):
    """True when the engine will certainly ignore ``act`` (mirrors _apply_unit_action)."""
    if not act:
        return True
    op = act[0]
    x, y = pos[0], pos[1]
    if op in MOVES:
        dx, dy = MOVES[op]
        return not (0 <= x + dx < board and 0 <= y + dy < board)
    if op == "PASS":
        return True
    adjacent = _shed_adjacent(pos, board)
    if op == "DROP":
        return (not adjacent) or (not inv)
    if op == "PICKUP":
        return not adjacent
    if op == "PLACE":
        item = act[1] if len(act) > 1 else None
        if item in ANIMAL_STRUCTURE and isinstance(tile, dict) \
                and _get(tile, "kind") == ANIMAL_STRUCTURE[item] and _get(tile, "animal") is None:
            return _int(_get(inv, item, 0)) <= 0
        return (not adjacent) or _int(_get(inv, item, 0)) <= 0
    if tile == "LOCKED":
        return True
    is_dict = isinstance(tile, dict)
    kind = _get(tile, "kind") if is_dict else None
    animal = is_dict and _get(tile, "animal") is not None
    if op == "PLANT":
        return tile is not None or _int(_get(seeds, act[1] if len(act) > 1 else None, 0)) <= 0
    if op == "WATER":
        return kind != "PLANT" or bool(_get(tile, "watered_today"))
    if op == "HARVEST":
        return (not is_dict) or _int(_get(tile, "yield_units", 0)) <= 0
    if op == "FERTILIZE":
        return kind != "PLANT" or _int(_get(inv, "FERTILIZER", 0)) <= 0
    if op == "DIG":
        return tile is None or animal
    if op in ("BUILD_COOP", "BUILD_PASTURE"):
        return tile is not None
    if op == "FEED":
        return (not animal) or bool(_get(tile, "fed_today")) or _int(_get(inv, "WHEAT", 0)) <= 0
    if op == "COLLECT_FERTILIZER":
        return (not animal) or (not _get(tile, "fertilizer_available"))
    if op == "CARE":
        return (not animal) or bool(_get(tile, "cared_today"))
    return True


class _View:
    """Cheap per-step snapshot of everything the layers read from the observation."""

    def __init__(self, observation, player, cfg):
        farms = list(_get(observation, "farms", []) or [])
        self.farm = farms[player] if player < len(farms) else {}
        self.rival = farms[1 - player] if len(farms) >= 2 and 1 - player < len(farms) else {}
        private = _get(observation, "private", {}) or {}
        self.shed = {k: max(0, _int(v)) for k, v in dict(_get(private, "shed", {}) or {}).items()}
        self.seeds = dict(_get(private, "seeds", {}) or {})
        self.invs = [dict(i or {}) for i in (_get(private, "inventories", []) or [])]
        market = _get(observation, "market", {}) or {}
        self.prices = {k: _int(v) for k, v in dict(_get(market, "prices", {}) or {}).items()}
        self.money = float(_get(self.farm, "money", 0.0) or 0.0)
        self.tiles = _get(self.farm, "tiles", []) or []
        self.board = len(self.tiles) or cfg["board_size"]
        self.positions = [_get(self.farm, "farmer", None)] + [list(p) for p in (_get(self.farm, "hands", []) or [])]
        self.hires_today = _int(_get(self.farm, "hires_today", 0))
        self.quadrants = len(list(_get(self.farm, "unlocked_quadrants", []) or []))

    def inv(self, idx):
        return self.invs[idx] if idx < len(self.invs) else {}

    def in_hands(self, item):
        return sum(max(0, _int(_get(inv, item, 0))) for inv in self.invs)


# --------------------------------------------------------------------------- chassis
class Chassis:
    """Replays ``routes[router(...)]`` with reactive safety/market layers.

    routes         : {route_id: list of >= 719 Kaggle action dicts}
    router         : callable(observation, step, state_dict) -> route_id, called every
                     step; ``state_dict`` is per-player and persists across the game.
    settings       : overrides for DEFAULT_SETTINGS (layer switches + tunables)
    opponent_plan  : optional list of the opponent's expected actions (front_run hook)
    """

    def __init__(self, routes, router=None, settings=None, opponent_plan=None):
        self.routes = {rid: list(tape) for rid, tape in routes.items()}
        self.router = router or (lambda observation, step, state: next(iter(self.routes)))
        self.cfg = dict(DEFAULT_SETTINGS)
        self.cfg.update(settings or {})
        self.opponent_plan = opponent_plan
        self.players = {}
        self.diagnostics = {"layer_fallbacks": 0, "entry_fallbacks": 0}
        self._future_sells = {}   # route id -> {item: [remaining planned SELL qty from step t]}

    # ---- state -----------------------------------------------------------------
    def _state(self, player, step):
        st = self.players.get(player)
        if st is None or step == 0 or step <= st["last_step"]:
            st = {"last_step": -1, "route": None, "router_state": {},
                  "pending": {}, "sell_state": {"due_step": -1, "suppress": {}}}
            self.players[player] = st
        st["last_step"] = step
        return st

    def _route_action(self, route, step):
        tape = self.routes[route]
        if 0 <= step < len(tape) and isinstance(tape[step], dict):
            return copy.deepcopy(tape[step])
        return copy.deepcopy(PASS_ACTION)

    def future_sells(self, route, item, step):
        """Planned SELL quantity of ``item`` in route steps >= ``step`` (suffix sums)."""
        table = self._future_sells.get(route)
        if table is None:
            tape = self.routes[route]
            n = len(tape)
            table = {p: [0] * (n + 1) for p in PRODUCTS}
            for t in range(n - 1, -1, -1):
                for p in PRODUCTS:
                    table[p][t] = table[p][t + 1]
                for o in (tape[t].get("market") or []) if isinstance(tape[t], dict) else []:
                    if o and o[0] == "SELL" and len(o) >= 3 and o[1] in table:
                        table[o[1]][t] += max(0, _int(o[2]))
            self._future_sells[route] = table
        col = table.get(item)
        return col[step] if col and 0 <= step < len(col) else 0

    # ---- main entry -----------------------------------------------------------
    def act(self, observation, configuration=None):
        if len(_get(observation, "farms", []) or []) < 2:
            raise ValueError("incomplete observation")  # factory falls back to tape
        step = _step_of(observation)
        player = _int(_get(observation, "player", 0))
        st = self._state(player, step)
        cfg = self.cfg
        view = _View(observation, player, cfg)

        route = self.router(observation, step, st["router_state"])
        if route not in self.routes:
            route = st["route"] if st["route"] in self.routes else next(iter(self.routes))
        st["route"] = route
        action = self._route_action(route, step)
        raw = copy.deepcopy(action)
        try:
            if cfg["hand_align"]:
                self._hand_align(action, view)
            if cfg["weed_repair"]:
                self._weed_repair(action, view, st, route, step)
            if cfg["sell_lead"] or cfg["front_run"]:
                self._apply_suppression(action, st["sell_state"], step)
            projected = self._projected_shed(action, view)
            lead_available = dict(projected)
            next_sup = {"due_step": -1, "suppress": {}, "r36_debts": st["sell_state"].get("r36_debts", {})}
            if cfg["sell_lead"]:
                self._sell_lead(action, view, lead_available, route, step, next_sup)
            if cfg["front_run"] and self.opponent_plan:
                self._front_run(action, view, lead_available, route, step, next_sup)
            st["sell_state"] = next_sup
            if cfg["budget_guard"]:
                self._budget_guard(action, view, route, step)
            if cfg["room_guard"]:
                self._room_guard(action, view, route, step)
            if cfg["clamp_sells"]:
                self._clamp_sells(action, projected)
            if cfg["dead_stock"]:
                self._dead_stock(action, view, projected, route, step)
            if cfg["terminal_liquidation"]:
                self._terminal_liquidation(action, projected, step)
            action["market"] = action["market"][: cfg["max_orders"]]
            return action
        except Exception:
            self.diagnostics["layer_fallbacks"] += 1
            return raw

    # ---- layer: hand_align ----------------------------------------------------
    def _hand_align(self, action, view):
        """Pad with PASS / truncate the tape's hand list to the real number of hands
        (fieldbook_logic.act). Extra hands would be ignored by the engine anyway;
        missing ones just idle, so alignment only tidies the action."""
        expected = max(0, len(view.positions) - 1)
        hands = list(action.get("hands") or [])
        hands.extend([["PASS"] for _ in range(max(0, expected - len(hands)))])
        action["hands"] = hands[:expected]

    # ---- layer: weed_repair ---------------------------------------------------
    def _weed_repair(self, action, view, st, route, step):
        """If a PLANT/BUILD_* target tile is a WEED, DIG now and queue the intended
        action for that unit; the queue replays on a later step when the unit still
        stands there and its tape action would be a no-op (the displaced no-op is
        queued behind it, so PLANT -> WATER chains survive). A PLANT is only replayed
        when the unit's next tape action is not a move, so the mandatory same-day
        WATER can follow; otherwise the seed is kept. A no-op turn spent on a weed
        is also converted to DIG (tetsutani weed_dig)."""
        units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        pending = st["pending"]
        tape = self.routes[route]
        nxt = tape[step + 1] if step + 1 < len(tape) and isinstance(tape[step + 1], dict) else {}
        next_units = [nxt.get("farmer") or ["PASS"]] + list(nxt.get("hands") or [])
        for i in range(min(len(units), len(view.positions))):
            pos = view.positions[i]
            if not isinstance(pos, (list, tuple)):
                continue
            pos = (int(pos[0]), int(pos[1]))
            tile = _tile_at(view.tiles, pos)
            act = list(units[i])
            queue = pending.get(i)
            if queue and queue[0][0] != pos:
                pending.pop(i, None)
                queue = None
            is_weed = isinstance(tile, dict) and _get(tile, "kind") == "WEED"
            noop = _is_noop(act, tile, view.inv(i), view.seeds, pos, view.board)
            next_op = next_units[i][0] if i < len(next_units) and next_units[i] else "PASS"
            if act and act[0] in ("PLANT", "BUILD_COOP", "BUILD_PASTURE") and is_weed:
                pending.setdefault(i, []).append((pos, act))
                act = ["DIG"]
            elif queue and noop:
                _, replay = queue[0]
                if replay[0] == "PLANT" and next_op in MOVES:
                    pending.pop(i, None)          # WATER could never follow: keep the seed
                else:
                    queue.pop(0)
                    if act and act[0] != "PASS" and act[0] not in MOVES:
                        queue.append((pos, act))
                    act = replay
                    if not queue:
                        pending.pop(i, None)
            elif is_weed and noop:
                act = ["DIG"]
            units[i] = act
        action["farmer"] = units[0]
        action["hands"] = units[1:]

    # ---- projected shed -------------------------------------------------------
    def _projected_shed(self, action, view):
        """Shed contents after this step's unit actions but before the market runs:
        PICKUP removes, DROP/PLACE(non-animal) near the shed adds up to capacity
        (fieldbook _projected_shed / tetsutani projected shed)."""
        cap = self.cfg["shed_capacity"]
        proj = {p: view.shed.get(p, 0) for p in PRODUCTS}
        for k, v in view.shed.items():
            proj.setdefault(k, v)
        total = sum(proj.values())
        units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        for i in range(min(len(units), len(view.positions))):
            if not _shed_adjacent(view.positions[i], view.board):
                continue
            act = units[i]
            op = act[0] if act else "PASS"
            inv = view.inv(i)
            if op == "PICKUP" and len(act) >= 2 and act[1] in proj:
                qty = min(proj[act[1]], max(0, _int(act[2]) if len(act) >= 3 else 1))
                proj[act[1]] -= qty
                total -= qty
            elif op == "DROP":
                for item, held in inv.items():
                    take = min(max(0, _int(held)), max(0, cap - total))
                    if take > 0:
                        proj[item] = proj.get(item, 0) + take
                        total += take
            elif op == "PLACE" and len(act) >= 2 and act[1] not in ANIMAL_STRUCTURE:
                item = act[1]
                take = min(max(0, _int(act[2]) if len(act) >= 3 else 1),
                           max(0, _int(_get(inv, item, 0))), max(0, cap - total))
                if take > 0:
                    proj[item] = proj.get(item, 0) + take
                    total += take
        return proj

    # ---- layer: sell_lead / front_run suppression ------------------------------
    @staticmethod
    def _apply_suppression(action, sell_state, step):
        """Remove from this step's SELLs the quantities already sold a step early."""
        if sell_state.get("due_step") != step:
            return
        remaining = dict(sell_state.get("suppress", {}))
        kept = []
        for order in action.get("market") or []:
            order = list(order)
            if order and order[0] == "SELL" and len(order) >= 3 and remaining.get(order[1], 0) > 0:
                removed = min(max(0, _int(order[2])), remaining[order[1]])
                order[2] = _int(order[2]) - removed
                remaining[order[1]] -= removed
                # A zero-quantity order keeps later market race slots intact.
            kept.append(order)
        action["market"] = kept

    @staticmethod
    def _add_sell(action, item, qty, max_orders, merge=True):
        market = action.setdefault("market", [])
        if merge:
            for order in market:
                if order and order[0] == "SELL" and order[1] == item:
                    order[2] = _int(order[2]) + qty
                    return True
        if len(market) >= max_orders:
            return False
        market.append(["SELL", item, qty])
        return True

    def _sell_lead(self, action, view, projected, route, step, next_sup):
        """fieldbook _lead_sale: when step % 4 != 0 (no town consumption between the
        two steps) sell the lots the tape plans to SELL next step now, for products
        other than WHEAT/FERTILIZER we already hold, and suppress them next step.
        Skipped at the last step, at shop-unlock boundaries and if a SELL for that
        product is already queued this step."""
        cfg = self.cfg
        nxt = step + 1
        unlock_period = 3 * cfg["turns_per_day"]
        if nxt > LAST_ACT_STEP or nxt % unlock_period == 0 or step % 4 == 0:
            return
        tape = self.routes[route]
        future = tape[nxt] if nxt < len(tape) and isinstance(tape[nxt], dict) else {}
        planned = {}
        for o in future.get("market") or []:
            if o and o[0] == "SELL" and len(o) >= 3 and o[1] in PRODUCTS:
                planned[o[1]] = planned.get(o[1], 0) + max(0, _int(o[2]))
        already = {o[1] for o in action.get("market") or [] if o and o[0] == "SELL" and len(o) > 1}
        for item in PRODUCTS:
            if item in ("WHEAT", "FERTILIZER") or planned.get(item, 0) <= 0 or item in already:
                continue
            qty = min(projected.get(item, 0), planned[item])
            if qty <= 0 or view.prices.get(item, 0) < cfg["min_sell_price"]:
                continue
            if not self._add_sell(action, item, qty, cfg["max_orders"], merge=False):
                break
            projected[item] -= qty
            next_sup["suppress"][item] = next_sup["suppress"].get(item, 0) + qty
        if next_sup["suppress"]:
            next_sup["due_step"] = nxt

    def _front_run(self, action, view, projected, route, step, next_sup):
        """Hook: if ``opponent_plan`` (their expected tape) schedules a SELL of
        MILK/WOOL/STRAWBERRY/MELON next step, sell what we hold of it now (before
        their supply depresses the price) and suppress our own SELL of that quantity
        next step. Bounded by our own remaining planned sales so it never dumps."""
        cfg = self.cfg
        nxt = step + 1
        plan = self.opponent_plan
        if nxt > LAST_ACT_STEP or nxt >= len(plan) or not isinstance(plan[nxt], dict):
            return
        already = {o[1] for o in action.get("market") or [] if o and o[0] == "SELL" and len(o) > 1}
        for o in plan[nxt].get("market") or []:
            if not (o and o[0] == "SELL" and len(o) >= 3 and o[1] in FRONT_RUN_ITEMS):
                continue
            item = o[1]
            if item in already or view.prices.get(item, 0) < cfg["min_sell_price"]:
                continue
            own_next = sum(max(0, _int(x[2])) for x in self.routes[route][nxt].get("market", [])
                           if len(x) >= 3 and x[0] == "SELL" and x[1] == item)
            qty = min(projected.get(item, 0), max(0, _int(o[2])), own_next)
            if qty <= 0:
                continue
            if not self._add_sell(action, item, qty, cfg["max_orders"], merge=False):
                break
            projected[item] -= qty
            already.add(item)
            next_sup["suppress"][item] = next_sup["suppress"].get(item, 0) + qty
        if next_sup["suppress"]:
            next_sup["due_step"] = nxt

    # ---- layer: budget_guard --------------------------------------------------
    def _block_requirements(self, view, route, start, end):
        """Planned purchase cost and item reserves for tape steps [start, end)
        (six_day_budget_guard.hpp calculate_six_day_requirements)."""
        tape = self.routes[route]
        budget = 0.0
        seed_bal, item_bal = {}, {}
        seed_need, item_need = {}, {}
        hires_by_day = {}
        quadrants = view.quadrants
        for t in range(start, min(end, len(tape))):
            a = tape[t] if isinstance(tape[t], dict) else {}
            for u in [a.get("farmer") or ["PASS"]] + list(a.get("hands") or []):
                if not u:
                    continue
                op = u[0]
                arg = u[1] if len(u) > 1 else None
                qty = max(1, _int(u[2]) if len(u) > 2 else 1)
                if op == "PLANT" and arg in SEED_PRICE:
                    seed_bal[arg] = seed_bal.get(arg, 0) - 1
                    seed_need[arg] = max(seed_need.get(arg, 0), -seed_bal[arg])
                elif op == "FEED":
                    item_bal["WHEAT"] = item_bal.get("WHEAT", 0) - 1
                    item_need["WHEAT"] = max(item_need.get("WHEAT", 0), -item_bal["WHEAT"])
                elif op == "FERTILIZE":
                    item_bal["FERTILIZER"] = item_bal.get("FERTILIZER", 0) - 1
                    item_need["FERTILIZER"] = max(item_need.get("FERTILIZER", 0), -item_bal["FERTILIZER"])
                elif op == "PLACE" and arg is not None:
                    item_bal[arg] = item_bal.get(arg, 0) - qty
                    item_need[arg] = max(item_need.get(arg, 0), -item_bal[arg])
            for o in a.get("market") or []:
                if not o:
                    continue
                op = o[0]
                item = o[1] if len(o) > 1 else None
                qty = max(1, _int(o[2]) if len(o) > 2 else 1)
                if op == "HIRE":
                    day = (t - start) // self.cfg["turns_per_day"]
                    hires_by_day[day] = hires_by_day.get(day, 0) + 1
                elif op == "BUY_LAND":
                    extra = quadrants - 1
                    if 0 <= extra < len(LAND_PRICES):
                        budget += LAND_PRICES[extra]
                        quadrants += 1
                elif op == "BUY_SEED" and item in SEED_PRICE:
                    budget += SEED_PRICE[item] * qty
                    seed_bal[item] = seed_bal.get(item, 0) + qty
                elif op == "BUY_PRODUCT" and item in ("WHEAT", "FERTILIZER"):
                    budget += view.prices.get(item, 0) * qty
                    item_bal[item] = item_bal.get(item, 0) + qty
                elif op == "BUY_ANIMAL" and item in ANIMAL_COST:
                    budget += ANIMAL_COST[item] * qty
                    item_bal[item] = item_bal.get(item, 0) + qty
        for day, n in hires_by_day.items():
            first = view.hires_today if day == 0 else 0
            for k in range(n):
                budget += _fib(first + k)
        return budget, item_need

    def _budget_guard(self, action, view, route, step):
        """At every block boundary (step % 72 == 0) make sure cash + the value of
        stock the block already plans to sell covers the block's purchases (hires,
        land, seeds, animals, products). A shortfall is covered by extra SELLs of
        unprotected shed stock, highest price first; SELLs are moved in front of
        the buys so the money is there when they execute."""
        cfg = self.cfg
        block = cfg["block_turns"]
        if block <= 0 or step % block != 0:
            return
        budget, item_need = self._block_requirements(view, route, step, step + block)
        market = action.setdefault("market", [])
        existing = {}
        for o in market:
            if o and o[0] == "SELL" and len(o) >= 3:
                existing[o[1]] = existing.get(o[1], 0) + max(0, _int(o[2]))
        cash = view.money
        for item in PRODUCTS:
            planned = max(existing.get(item, 0), self.future_sells(route, item, step)
                          - self.future_sells(route, item, step + block))
            cash += min(view.shed.get(item, 0), planned) * view.prices.get(item, 0)
        shortfall = budget - cash
        if shortfall <= 0:
            return
        candidates = []
        for item in PRODUCTS:
            price = view.prices.get(item, 0)
            if price < cfg["min_sell_price"]:
                continue
            protected = max(0, item_need.get(item, 0) - view.in_hands(item))
            avail = view.shed.get(item, 0) - protected - existing.get(item, 0)
            if avail > 0:
                candidates.append((-price, item, avail, price))
        candidates.sort()
        added = False
        for _, item, avail, price in candidates:
            if shortfall <= 0:
                break
            qty = min(avail, -(-int(shortfall) // price))
            if self._add_sell(action, item, qty, cfg["max_orders"]):
                shortfall -= qty * price
                added = True
        if added:
            sells = [o for o in market if o and o[0] == "SELL"]
            others = [o for o in market if not (o and o[0] == "SELL")]
            action["market"] = sells + others

    # ---- layer: room_guard ----------------------------------------------------
    def _room_guard(self, action, view, route, step):
        """tetsutani room_guard: at hour 23 the end-of-day drop pushes every unit's
        inventory into the shed and overflow is destroyed. Estimate the shed after
        this step (stock + carried + harvest/collect - feed/fertilize/place + buys -
        sells) and, if it exceeds capacity-1, add SELLs preferring products with no
        future planned sale, then highest price."""
        cfg = self.cfg
        if step % cfg["turns_per_day"] != cfg["turns_per_day"] - 1:
            return
        cap = cfg["shed_capacity"]
        units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        carried = sum(max(0, _int(n)) for inv in view.invs for n in inv.values())
        produced = consumed = 0
        for i in range(min(len(units), len(view.positions))):
            tile = _tile_at(view.tiles, view.positions[i])
            a = units[i]
            if not a:
                continue
            op = a[0]
            if op == "HARVEST" and isinstance(tile, dict):
                produced += max(0, _int(_get(tile, "yield_units", 0)))
            elif op == "COLLECT_FERTILIZER" and isinstance(tile, dict) and _get(tile, "fertilizer_available"):
                produced += 1
            elif op in ("FEED", "FERTILIZE"):
                consumed += 1
            elif op == "PLACE" and len(a) > 1 and a[1] in ANIMAL_STRUCTURE:
                consumed += 1
        market = action.setdefault("market", [])
        planned_sells, planned_buys = {}, 0
        for o in market:
            if not o:
                continue
            if o[0] == "SELL" and len(o) >= 3:
                planned_sells[o[1]] = planned_sells.get(o[1], 0) + max(0, _int(o[2]))
            elif o[0] in ("BUY_PRODUCT", "BUY_ANIMAL") and len(o) >= 3:
                planned_buys += max(0, _int(o[2]))
        shed_total = sum(view.shed.values())
        fillable = sum(min(view.shed.get(it, 0), n) for it, n in planned_sells.items())
        needed = shed_total + carried + produced - consumed + planned_buys - fillable - (cap - 1)
        if needed <= 0:
            return
        priority = sorted(PRODUCTS, key=lambda it: (self.future_sells(route, it, step + 1) > 0,
                                                   -view.prices.get(it, 0), it))
        for item in priority:
            avail = max(0, view.shed.get(item, 0) - planned_sells.get(item, 0))
            qty = min(needed, avail)
            if qty <= 0 or view.prices.get(item, 0) < 1:
                continue
            if not self._add_sell(action, item, qty, cfg["max_orders"]):
                continue
            planned_sells[item] = planned_sells.get(item, 0) + qty
            needed -= qty
            if needed <= 0:
                break

    # ---- layer: clamp_sells ---------------------------------------------------
    @staticmethod
    def _clamp_sells(action, projected):
        """Clamp against a sequential stock upper bound, retaining market slots.

        Earlier BUY_PRODUCT orders can fund a wheat wash's sell leg. Their full
        quantity is an upper bound; the engine enforces actual cash/capacity.
        Removing empty orders would change the later lockstep market races.
        """
        avail = dict(projected)
        kept = []
        for o in action.get("market") or []:
            if o and o[0] == "SELL" and len(o) >= 3:
                have = avail.get(o[1], 0)
                n = min(_int(o[2]), have)
                n = max(0, n)
                avail[o[1]] = have - n
                kept.append(["SELL", o[1], n])
            else:
                kept.append(o)
                if o and o[0] in ("BUY_PRODUCT", "BUY_ANIMAL") and len(o) >= 3:
                    avail[o[1]] = avail.get(o[1], 0) + max(0, _int(o[2]))
        action["market"] = kept

    # ---- layer: dead_stock ----------------------------------------------------
    def _dead_stock(self, action, view, projected, route, step):
        """tetsutani dead_stock: stock beyond everything the rest of the route still
        plans to SELL is dead; sell it now when price > 1 (on day 29 everything not
        already in this step's orders is dead). Highest value lots first."""
        planned = {}
        for o in action.get("market") or []:
            if o and o[0] == "SELL" and len(o) >= 3:
                planned[o[1]] = planned.get(o[1], 0) + _int(o[2])
        day = step // self.cfg["turns_per_day"]
        extra = []
        for item in PRODUCTS:
            have = projected.get(item, 0) - planned.get(item, 0)
            if have <= 0:
                continue
            surplus = have if day >= 29 else have - self.future_sells(route, item, step + 1)
            if surplus > 0 and view.prices.get(item, 0) > 1:
                extra.append(["SELL", item, surplus])
        extra.sort(key=lambda o: -view.prices.get(o[1], 0) * o[2])
        action["market"] = (action.get("market") or []) + extra

    # ---- layer: terminal_liquidation -----------------------------------------
    def _terminal_liquidation(self, action, projected, step):
        """fieldbook _terminal_sale: on the final acting step (>= 718) replace the
        market orders with a SELL of the whole projected shed."""
        if step < LAST_ACT_STEP:
            return
        action["market"] = [["SELL", item, qty] for item, qty in projected.items()
                            if qty > 0 and item in PRODUCTS][: self.cfg["max_orders"]]


# --------------------------------------------------------------------------- factory
def make_agent(routes, router=None, opponent_plan=None, **settings):
    """Build a Kaggle ``agent(observation, configuration)`` closure that never raises:
    a failure inside a layer falls back to the raw tape action, and a failure even
    before that falls back to PASS (with hands padded when possible)."""
    chassis = Chassis(routes, router, settings, opponent_plan)

    def agent(observation, configuration=None):
        try:
            return chassis.act(observation, configuration)
        except Exception:
            chassis.diagnostics["entry_fallbacks"] += 1
            try:
                step = _step_of(observation)
                player = _int(_get(observation, "player", 0))
                tape = chassis.routes.get(chassis.players.get(player, {}).get("route"),
                                          next(iter(chassis.routes.values())))
                if 0 <= step < len(tape):
                    return copy.deepcopy(tape[step])
            except Exception:
                pass
            try:
                farms = _get(observation, "farms", []) or []
                hands = _get(farms[_int(_get(observation, "player", 0))], "hands", []) or []
                return {"farmer": ["PASS"], "hands": [["PASS"] for _ in hands], "market": []}
            except Exception:
                return copy.deepcopy(PASS_ACTION)

    agent.chassis = chassis
    return agent

# Extracted from the frozen One More Wheat source on 2026-09-22.
# Upstream Apache-2.0 notices are retained above. Generic library only.

import base64,json,zlib
_V10_TAPE=json.loads(zlib.decompress(base64.b85decode('c%1EhU2i2vlHGslXFiDiO~3U>y^^p!>OpsFg|R>k2JjjNjP=9VZ^r(2OC)c7WSn#2L}pfztufGmsAApAs>sNQ$cPgse*M4C{`=qm@gM*Gk7xho*Jpou_xba)+pA~)<M03Lzy0suF8uc6fBgL)|MTDf&u>5f`s`0X|MhQw`SkI-pTGU`?CRMsKfHhU+kao&Uj6#)haW$^f9C%1``3Ja|NguEci`W=yj*_w(~p0C_u;o+eE#A6`@cN9y1u>r&#T>||M=~{{`{Bi4eM+C`s|nYpTFGwac~>C_@|$L{P5l1ev`<TpC2AP-nN&|=l35ztdIWu_mAu^U2onK3o=Rof97A_fBN#{hadmz`%lZ$wjX@nT>kU>4<CQp+?`AG!@F<aGl4>p{q*tEmmi+(e=-GbXxgjfg~;XbJ=d>;2)_OJ%PQ&pn!VsRlhwL>!G4Vz;a&u^5h;+_`llXt=2nyMuI%I%pT1Rs?PEgWyoExzer~ED{64Y_@z1<6q!hR1B9TTkTR}E!A+{}F!F0hdm%hO=q>^||e{&=Bu~qlDdw=?}{C>Z8!^TEpegE!3nyX&kUkWNmHsAiaU-oKHx**{b!1CVEn_r@pYGnD#yDz`}MYdTVq`BFvar>^f-zzE9!1nEOi9tnsD}>(~v3$QRn`+UAb(=LR_Up6nK7IU4`*QU~9TbPqB!7=wmK?5Tv^Zi_)9rtqKDL(0i1Gs4`5=?~ulxPVx9@(p2-&;s#9w)Jxu&^(MkQQc1-Od1s;k(#7q4cWWDsch+28+l>2a`AVDYt7OxMVr0I<w2@;5ejGf?#9#a4|6VSUi}fBF4ACMX17)VlT<YVh#3a&suZwd%^lU6z+(l1Y`Ju(XzfGplTwFttVnJricMN6jivMHhelgBw}3OFitv$ckP5I9##MAAgSL#Y}LM9x#jP($x#Xob_O(g#=Oh)OA$KzWi-RT*Xx^#c@$&NYj_cUDeK9x%jX9!P>(VSh@8H>(5mSf17Nd4h%QDBW50E3hmpEA3nVQ_RHTkj)tZr3;DG>rN2)?Hh=K`)Dl(PKBVnZn<9?s-i7L1HtFb5ieX>Y){OifKD!k(CJ`0QuhtfU>C44_Y~C*(j`NVi$%u>|L!PT0@e+rTaXVZ>#qBrW+@(~=y0+(t=lNcePx=b39XL90(KaTcKd@<D?d4ulF-_at|5k6+eHw$?oN!N%k@t5cF|?&L!0UJ^*pcWk@AuIz+DP5ct5kf=2i{onZf)NElVQoe+a;$H3wKTSI)AF?^r;@iw0WvE+-XCO)H-=bzUO4!gBa6CT^_KF)tofMbGWoOOdYuhK{$EY%@4NGIlD0dCMh1^?OwN`R3SQO43e>Hl6_sx+Oj-X!Auo){<f0r)CCM5oCOqMLE_8AiqzKgn6W}!E^(>!8eCrZ1@E;#IXUF31>VYg(HDmEAupT9a(b=ujSn6!Su5xG@*;V&;P~Sjt^25Xu@~zuo2!J-fXI_bx|3FKwye|4Cr=-c?)j)JGC^2#An8M^M`P#PtKe{pYTbQl-e%n<T<^{(7q@@2y6bTv!&fM%s_<a_$&cGB4zuz#z{w*7pAP?s3PTVw2#3b(-@bhP{l|}=-<NYo$%*GGKCu0C<wQaDBxS@v8->>_!V=iVOh#K_NuT6}5|p)!A_C6@*o(B_Pn!U3l-dKSR)wjS)p<N!=eRhnWg);Raee9`SvqoywLBoWN^#PC7!M?|EN8nn9!1GO2@kHPlw3s)KfL?&Z@k6|L{TWy+?VCQ{YV6yEc=XdX^14YG9*IC%SZflRokf!`pS^dEAcpcO{|n6Vu=ma-wbJ~$7`NrU5Cw+Y!~O@{IkEfhGfgtNzbG4md#2n>A^<r+ry1|HjWzg(3d?G-_7%ZO|tv#_KhFoHPBgMQN=|!;txjY^~6VBMY^a={9*PZkHG`h^hx-kkjOjgfkn<aK4#%`e3*b68<+Z;aw|@ro6QbY3M)`3QyadCr6{xf<xG89E4<kO#5n5O0Zdce;K=7JOF>Gx`5C!f1lA`p6OZ7eM$46QB=`by2e?D26r~r>9y~rf$*-Bn4N!4SG85}5sC*>bR$!d#HtfF(LF}QC7weP?ZcR;GJTtNdsfO^K4lHC|0OcK6X}&u%CQ$?k(Ye;bn{$G(FJ2HyyjG76fd*vrIE`(Y6k-gduzgKxBi%DE;d9??1c2KZyWB{A*aN#CxP29pf>a?gU;L6?+Du^d8b#)Wy0JBAd)NevZ?3uM9WIvN=@(tz{o%O(`OBwwzx?U_r%!(c&QPT|fe(y5Cr!-I^ZrC69X&RNR@}NtLL`Re?YFuBO8gzGS+i7a!}NBICxK64lI3#x-~7ESNZ43z*LGP-P(`Kq=Q0NuUrb&%ZaGEIZ4W<WiLoN5xwAI40QPxMWh1VQpgZ6ELZy;@;WW2HP9%+9ZBCDK8oh}68g3?ZYQ;!10UToEP=DMv`crvAYgr2ju36q|y$!M)2(2P^(2#sQ>MufF9tZT0AjPE5+djj-F4WU@zQa2#&)J}6@$=XRg`%n#j?z#IR@ts<kO>*<DSOrDSl|M;w}idR4=b_~)HQ@N_R~}^tVaYP2+&d^N35R^MUju6t5oH+@XS0FU+!m_l=9?R<5IZGBcoNdAV6hic9Xnt>Fttm*p2R~MUA)@@|w#oH*=eVFVDB0g7ntIUMM)pxS))8IPPC%d9I3>7?Ln=i^uQ31JYmt4W~vys;di+By^#7&AqLK<GZ~W{XA%z2<TN9k{hi!gJO<JXJdp@1gGaDM+D#$c~ybr*32YI>7`Ta+m$7b9V=G1l1L^d2_*oW-e*%8FP_Txu4@Ns0BwLaAv>D9V?bg$i2%M=QLq!0weRH;-K*WrQy=O`s;ER7BxeD(DYjsqtliWtEZ}Tx`hfh4av|X-+=M<~I%PI^&Q&#8#%9~tbsK@LQ*om)fL^r;;HRU4^=8P~@rJ2SSOb_aOtlGEHH`}OnstR%r1}8ljFRy@=Rlg%o0K#bY^n}1EeRT!Pz}X9JLb!s8wkJ#={;lK!X$*}ZzKjEy9)5hypIw;5K=VJiN5^#Ch5A_&O7|IwUoq(Ra$*<*(J)c-NZ#L<Mz=vAF_DdJg6bLzE-3~GJOm@uaJ4_=B_ykyk`Kug!|k+Tvw+Ur{{2iH-${Ix9otyV}J?+7Z;%Ga&w9lH&By(d@BE0L6}S=lqSfUrWvpH?`DK}O4mytiA;OU6(U9gRKF;I0ok#A{QX&Py?b+ltj%{GQH)J!f%c(n!1T|^UaG9;X2~#Ny6i=L)--d7B)W8`v>lGqozl$%V0f_+_sTQ}bBE1m<*JD*1L5~t=*QdYDZW@(twr5s3}(KHS2HOUSPs9riYwf1-k4a>7PcFVT>?z=*Jm^+humzy+9Nh1Qi}<`2+zziI*G?uJsws?+2tDfdZ&mH9uqZqAnqG=*~i}OaMWL{c-+HIOWYq(N(w(IU{`-|DRsv|G137LPIKl#-cm9iFH}_`Zk&0?%BLGHsGBP^pTXh96u1`T*6NS@y;E;4fWD#(W9~Fw8R=zyx?<D41F7KRd6t&#`XqO%X-?>b3+#`_sL_-0Q+>jSg_W;H7zK6*hwYYe5&W?v0Z=D%D<kO-9rSoG!KC<kih$scA3to?^258IzT-t65Gs^2f43ry8Hg80N*7yv0G%m#l@$^U!079d(wFS+CzVyv@KtJvw=msz`T;Sl_rFr(V@nkF<8>av;?~~e>;*^t+qd6_E9!Ucd{p?m@Bn<8WGQ#{wnD2MTcccZ0j|K|8?u&~JqT?-2v-`Oq`;N+p-0ruu3M34Y{V+1a)7w)oVScC1i()uEDlC{DsT2|^UdFsS7%CTkFo>i{=m2Q*I-M@{zNbs^^Fi|tqGrJ(|um<X1c&mY?+@Vs@)=!y|T)~_4nU@zlkjPK)<{DK%Bul3f~I3=gs@uKN~54gRO{J>D6-iMgn&=@H_irc3>}(p4$pUoNf9lY+sTD%h_~NcA<rmW-DMEv>G;dFGgKiwqOKqN>-mR3vYBEdYz4&2P|!qGWS<F3#hpQp-~+eG9n;^*{$y{yS@p+$L(9=ymy1se6T;MyH18~$BhQ;lsAQXksPSB7q(uo|DN01n<OZ~)|p7!8Ee221MY!9Zpt1-FG+3iW~bFBuY*a&Q3*INaPx9VfdF7W_gyX%;pW{-hbwdFcVlQ|AKgavFL|}-?pJo+`lwPN3@p9%Uj+@MXvIK&ouw@-M&`s~N_gNkem6C12e{j8W5*e@lx2Ta@!ofpHjboS%0f_T4gF)(W@}2TLA6DnU$}qdYY>4@rl1xJw*3x%tpYe=VoPIF3^@C?1R=XOKk&u!jw$6E)llcqZ`ZX_!e>g&iv^U}859vCv_bVM6rRdYAB=#p8ubQ|pb+C-A`@6(HQ=_;YPmeB(2D{_I4f14$T%f)8EjgJFO;+*RNZa9QxKvQNT8PdCrofKeUTYswcm0Um*g~1X00h5$n$ZtMo1ei7vxqfEKsL88+#2Duw<(f=pd{lWq9D_I8Lr1j~}D$E#+87gAfuQ@m@V<#KW_{;jgORU1q*eR-d86_V9B(MRJ&_gyoVoa8AVyl12}V)yPapf!`v$6g2LILGVt>iTT-hN+}WjMhGT2m=@YlkPy7{7{@w9){P~bXMaZ|dKb9VD4p2SRq1C5g_rasO0|mLyU#}zX7GV?Lo^!O)^}^Fju%IH0GDm@7D~nJzyS?PH1d7E`>okR@*F)hGI{AG85-(N74gfQb}}*@MHewby3uusn??mEF-Av4e7)x;lAvZ=h8|da`fk@Ga#Nc-wh(}zS#W<8IrTv1WDy;k3MhyndYOEXm0wjnI}B6W5C42odRX270v0WTu?wf#De?oDB|yq;>QsnY<lHos2vVfky?;5j87f$esmM;ChDi0mpY||c@{gaM!>ZzWkI80XDV7NfaLx-x=Yy%RBD<eTh{=?3<`ai=Xq+A{&vd;euVxKuQA=L4o|hZ`{NsmzZI7&edP^ct(%I&CFiCmM?q7jJ9-kMEa(o8Fn;^7!(vgvdMmYmuN(^5!(Nf$uGY9-lom}uLcwrV|9g>(9Alw4}B840)IJg`btTSer^6@bLMR;d@Sco#-;zwDg2i$u3V`(83=p@a_y&lz1J5k3@r`L^;?qBmYkrDa=g;I>SFGtz?-k3r@({pSDfOh9BAGGcUe!|$|%p$@(w&=g!r~i^k-J((t-x?rELJ3%j(#`R_mT&9;t5Q1!k~ZO05bZDcN#PO|KnO3h#>;?(hK71Vl#aO=vjeYY{D)|W4%j&i3IY0@r_8}*tQM5XKM0(}?h21nLqiWZAIe5EuqF|nrghWZg>Q(!<-m#H5-b5<w0sBL4vDOK^WJwqey=xXV(|fFF82Jndz{G=CVHcKZuB||NA&iY`CC=k0g?fFDDh`?NFfs!R5S3;r+Y%L0FqD2*CE3;y3aaa)VAvC%_KxtnVvG<tNZPFKBRI=0Raz4MfQv^?XVCmG&Y+LTIhUgZ$VLkpPO!gWJLf8CX7Kc>{jsr0Y0pznO1~}6sT9F03!SeL=wToieXR=e80FWM09qQn9KMo2<|#*JLK;MIP4W5H`4qm#muec%r~=)9*YKY-UgNd&i%n|s)K5zh>6k@lsluNh=EMnKFfy;FmUm_7Yxvk@Ww7>%FavOt>ck(mSqO%9brQgoijnBM3zggBJuXJ&c1SF1i_QQI;32T987Y$1PSnK-Xp!FGSi7v*?tf)jGPXHjR3T<y|7gLeoQ3$dAS~O%EKo`KP`tJ*UzL-y+tP<p1Pt^a08XxFb?dh*&skc1-(?U<g(_n!Ni%!>!`blMsd(9pALCBo@W!f2M{_j+X;-!60!T4&E*H7T-ch5_`Eu10zec6fkBF9x`qJ7+$!+BU830W6jX+aDPqVBA!F0^rm%!{X>S%&p8+h8#DZ^S5tUF@7D`j7Z{pi+F99Lp4QJNwIvO-kV}qLe3L5FCKXzkhsvk^NNn()$M@fK_>X%3!M2qF)GvbuO?F08t)2lc3#fjnER3mc&fN)l|4em#iZJk?a4{T~g%X!d19HHH$>(fyQ!hdg@dVNWC5%ye4Nn3!ZA~-5aVii)MbB+#gn+kG`79{7^yu#TEP-;5>0xM=yu3Wc?t|qWFYC5OBh&M-Vha%gAPKDGO543vDGW2}}TpHNn0;3GipK2)0W`E<|VPHX;Be97I1u$)iF7)cBRUq~D+%VSt;$7N62R$)aEg){R4-6&JqCTl@{|O?J+%+V5QE7XDN|fQUAPL%UuFz;tuvgQ@|HA6LHlN>^v>1}svAY9#IV617J-APAy#PQ_Yx>W#<X=b%j%*s$@exa?TZwFc?x~}M?&-DxUWG4XZ5?-yacH^05B)2(2i4F}tTNmQJCj3NtIuGw^h*$iTac%TYQQ#W0`{iIL#FVzaV4yPPiOo&WCU)0F|i=R1@e(-FL$m5p3^nYbm0Wn-;hZ_G_X(%&dmbBud$)%CvevB!u|@%5`ez4+O|AOrt4*wARZup+qeg#09PPt#R-e_2k4Fjjt8%hTzvJOH(?_(5Y+B{n{SB>53*txd#PeIKX>8|;FbnC@tCZnbj^8Ao^vwyd!Ba^R0qi#7-(Tp`)Yo)U4U2)<${6wRyUn)APN#&i+E5eX$3iCiDOPHO9%l@U)et8p|((Ci|`;j<qVR^4I1lzVb^hyH9#qNpO*)l;3<2uDm#213YK>1<a-G}DBR60)?Bo5&TPZWlH{~xT!>8k3bng84ufUJ*okjKC6YQ2+BDI6Kmw~=<h$NJt>3Dvr8Ox^*NyxvK-S8#lME&kp+eoZPDl@*V8}QoFVX;!%=GN){@FYMLuFWvb?Ed1BFylEGBGcOX%c$dz%X2}_;u5ViR;f|2?|8CAWBzNVvq(C6^LR|Y2(In{lbdGz(c@WCY@|0COk&}RtC^YorOgk82Ta>t@wTMTvo~zgQ&w<itF-Hq`&U6(kd;jq{g^p;tuHUy>waudCZqgI!<~pHOzo77(1qj+N`Y7q%|Hj3Ww%Rp3ahx@?*}Ra5;`wlzwXu9{y~4*i+J^l$2BCn-~@%aw@$Bt+vT$H1<6l8e318D6yTHD4ORE9!qxENK_Pv$m)JASZg(Zg#0-I28Rb5X;b9EJk(ov*~(z++nio^nXFJ6O9nVPG$}@K&yBkgkoVN+!6NL<6liw_b!Ky$uroG>MwEI=IH6FY_4|DX*@xn2VD4D;VKX*bf$lP#iXKw>s<7>BN@R*aV8_TX5mTyxY&8ZM0F9i{uw@vubgM|Fr*4G@Q3de}KpA%z8Ef*J_;s^64X<~seve)KmZVXdNlH(&2`Nu}fDS}8VP!UXpj(<`$l}qL6<PVRP+*%5z(-c<E}i{>c3T`$dEvZ^Lj*;T!9vOMPD)w`5&|WPt!&mk<z|uzl!z#;*-VYORP0<5YUy%-7b_{{5SrD)Qe8z+_AXXNP7x#zW#**Q&zW4k>bz(u8j~rnSjO=ntoaRre-r)m^;dU(H7hfAK%b<{e18o5h72WdF1<DkN@&qYji$~nZjUlU=v+G?<!1lp{-*F4Nufspi<O^C^IYHnX<8RqIXgf?X|^ywd#0z=!n_sHz~s_6HlG}mxTpDJzxKQ_>%!Y#f_)YprYLg@z&CF;%yv(VafVM=oU_bQVLR40NZP#QyAJ)6fn@76SKc!5+?Hvs(!&FH+HoPmPEiLzkotnT-SbRUIxcLo3FC{0TlpQ$=V<oE_bRG0$y66V=ohMcfG!sy(TUPXR3V^Lh+td}TC|PeqftR3n<UUJpqM7@HW`KSdNgfISWPm06&={B9K;g14so0PZM|dZ4A7MfwrRO_UFEnMZZ#u~h$^Gsl8g+n5P0X5YeQX8P4^nr&r1>dtF}p{TSFF#a52c*6{iY5=4TJRREQ2$mzGD{8r{J}(LS084XK7uZ>xi_wJ2*d!i`W35t=BlbV-!mm>6ncOApo9wN~jKJyX7*l*6{}3LUo=ZhRyKmP7JXaUIHz=q_kXnU`L~RH^4^Y%bqev<G++loqk5h<NYqJj0t`INUTBVan^Q<pi6#-001Ptd6t(!-_b4^W!;&r#Jn-Ko<u<5HAH6z}vV2g7Ehm(5Bhxn&z+Yv)E+}OCtA_QyB8^$uXKX8Fxkk=z{|sAG4i=z0bKADR(aBdcOWT6l^8rLgAqmg20x($KEVj3+t*(h8yB}g{l|2(5I1UI_MaWNu141Ms)*_9LF<2Nz_1=i=lyu#I`U5Qs6oni7HDB4bpAXO=t(g@WS3X%K}vduVlYd*q7l7;&%Dwma&y^gC3GvK)g|hg;m}P9hR>F?QgfnZqz6Kqrn!zFqdY!hm&Q>3o-<dUBAEtO*(trVJT0yuG^25Lj+@%L{OMzlrR!U4x>81E>k5WApOLI%@(@${0r6@6{fV6dRyIuD%F=%i>ghARSi~so3|N^E{e4<_t8%QdJW0hpeS4tY6h$L=lv>D%MdhhQc3Sr;Wst4_Gl<o>dFVt_4OkkgAv-Axt(IuW%7nW^)yPs?r`*55@JjjX935s4{bM}W7A&KK0+U`ypN``vu)HzNrfcy<1@K929UW?NuR4Z1I8h+Vmd5h2+4A`U%=>Lg?cB=#IrPhC!?%MJ|0Ox$BF75@oBah4jGoyRSX^hpvMY**JuWml65-B+>k>rS)_`P9x~$?Q>DfzLIeods9JiqNPok@_0*p-{yXqQA>M#~F~LBk=?Zv|Q8XTL4(iByu-%+xB}?|Bg1<?|Z3Rm%+-S7pn7k4VQ;&Vcf>7lk3^I^$y`GbjtW*ZwUlw}Io8mmmqTi@_UT2qPRyZl*&tjt3OvkI}yL1A^`BIUf0N&k2#F_CbPHQN2&-*gkGrF?eX1E{J)SN~)u;U?u2N(-rHTJ68pjBpLDr4}mx28O$l%zO<+@LE=-+Gr8T7-s%y>J9hl=?WxIx)1YDZSemyS4iiIRcnoYZ+%5LPwK4h7j%_bDS9B#O?L1+Fbm@oiX~l@DH;|APD~95{7)!F1o1SfVvREL~!2#xJ2mDK$SJZx5ROO^WhP|1*OLfd9v%_nPAuV%=EdFk1Gip*u7j`*t2L$@KFUIz0Sva=%6S)pC-R)y)PC!0MUy|vlHigd3T=_Q~@ChG+W(Fwp`53pf3mcaLwjnT6mxy9aW$PTna^8`6AXFt?R<prf{iY%J*vY;Cmd@Qxud>OreXMF{3-M^#^W_DaK%mJ<!AUl?p^3G6SA<IGG2@P85UKb!fML{_^SFFMoRf>C<0f{?9oq3cfWoS+1>#Z=PU(r`gBbBPXCvNFBjlG=1djTufbv=`(VM9nbks$8^ML2DY7S7bW`wbBor8^6F0V0+MrrJgeBHN;+*@ZOH+7X1-1Jer5;jGMHxTXO4n$?2|<nTq%}N4G33^t+89cR|k!tni*3|+l*dniEH<cC(rI8uH~(o)Z4&`1FEui^p5Lkj{aWwv!>Sl+_@oLc-oU~-1Z=^Df{*u6?GN47sLYX+E(KTb^?)|oZ+LkM&b!KY-f=-MQCfbjzRcUV03*Ft=d6(Wv6Ra!B0wOKySxE$6twDHGXifh;gu&hw3pk)Y<k=SdwzOd<6LbuI~y5&-%eXx`vW-RR#}<zjKP04pGC`tFtv)krX?upimSs-!0Nmc_g&iQ!iN{){t}ura(5x09$|}-Ja3PcFe?PlAU^~T)xPrB2em<5Xxo^wD(`x9cIb8xhJDgU7v0azQ($_;V7-LEi0B&%15)|Z<{{|tBI%tB<fWsG;gyxUtOdC3vk7(bZ0v$trhBNnI?HsC>Z3)-u*)8fjihac(8n#M)sj0qU%>u1@MyjK&x*;5xp7M0E7VQhc`mNaj$i^P=jVaI{nE}-LzSlA1XI0T&Gyzwb?p)q0~^xcS%Z>F@Zn8BMe7T6>K%OvsI@Qj&oyg?xjkvw<w#|dBW8R0bnA&w(3FOTnZ-vGpVk>Pv79)#EHonmR#U!K5$TQHWO(mbjHubum-h$N40i3D9#Y}`DeFU|63HRp7~&RG^@_Rz}Yff0k1Gndw`DG_%2b{O{e{2Fa)>Z<icxk|CTp5Glky+|7fM&*OsX)tZr80UGv8<m?UC&q|_qxYix!NLhQ|v{Xdh)g<o^9SXVe^mQBbe?4ybzI>UQy4wt{Z|EG^Qw`&!4YZ$F7z7LE{`gDapBaL3yWr?iu0tC%tQYMQ2W5|_M(?CqSZ=}Rp3RCOAh8%<rdzvCPp&uqAf4Kj_SncHB1btuILE1016)F7T@fay><s5xFrs?UZHnAQ+HTA%il{X-k>3QVwhlA+VOh+uRBok9quC2#BI}ozR4vBLagW`NVGmDOQ4BpG?^{TOJZTx?@vaMY?b3Tq=jLu*gVWI>TgW~#wwnc%cx?9|zL^jRQ<T!||w>~9DSP0nP)ah_f6OZO3Hu7HiLs1bA)y2GipbP6)us#-7F0yfldy?<5i}?4Z5tOv98N`AY2Hqm|DoDAD9H1%uHfsPKIp6?V-4X(=IMi16f=r6bNX`%3<@@hxdaieFMm4p{zwUHfFZNzTQ5cdQRP-~*P>9tbA(me_UKKi_Zr~!^uMqH7H`XPiQ;$DKd8&`%834>U%O$WIR6~lwL_g>*u<?9)i;9OVo{a6U60!_#x(Wq+wP|9h4Q?Y43`kDZhH=tb1whY`NQcF>H(cJ=9h{S54Jw2srRZz3E?J%-+=LE!fRjS5$i|oS7^UQclu3%OPNct1PV>eP?-WZUD}GrUVU{4>{C+x7z|8w^8L}~@1?|9C#9kOs`P)l&`K&sZXWQ`M&O_7D&O*rRRnII}L-lzSxg3b519t#&O{x9qOzMp!M)*J^gA3a`5(|ZvbymwCv@;K<7h|jUC)6BsHG2du4JIBXDN|VsKcS8|vRsO%IXF}Y80rm5+3PU(nP7-#3@p<VF3Xl4E!<4!Sz@=K>9|w3Ue-c&L?fo5J-_O#^+=WmM>4y_^_)-!+XjIFMGFG55`=BV@urR|JWIQi>-EzuutGqc@v0Du#BxQXzu2SZJuSws;2=qill6>cjzQQYHJl}%*d#kSSYmHz{`*%{ORk{OqK_~$JBsQFtx$(6cvBSrj=na)suN4Ya~Lh_lPGf5M~x%{L|8&+e;u?}29G?E3Z`n5&gsY}o_VqTT|5TnxS}3f+_^L|&i$dUUoKJv<-=MU@4?jUXwfJ^ZaI)UkPTynS$2^y_M$6?ItI*)A8i+tJgaUpGi7+?gm-QeKE=!sHee((mrQ#-&s7A?e+A`FeFE%p+RI<6|5iSjwkq0|2#jOwe-WPHA;8?eh^f+E)!&sg?<<}cA%T=bt#G3W2PKxKhs(uTl9J`A@wC3WrKi21`-4m(*N;Lal6sgSB9YiyniGkDfa<yC*$i|exWESIEj3E>dQ6(43*5#~7+Vu%PmFl@A_!50#003zHh>>$s?h<)whz^6Epu7!A@<(`<wK!SNpSL&940Kqv6CG=Q(-_LRlQSqGqt^xbjjb|(0Dk(3`+(_(O_k*e*gH^TW4H|1)81Ho+-$$Fy}fubw|)6^1K=10wL%j(l}ucPVJKr_zjUFlR6l%1%~>tBSf5S9hp#)Xf@kd;P9rnCy4IqvvcR1YX=?grLp}vj|sRFB;^u&$ZE-M9LZ)Bfzf&e#o`J#C|VF(gwxSx&tB*V9yZs_&WtKvH&z#@_m@*c%C@=#iRUZA=KC_CPoZmq!3scf#_$B(WK0_1J*TdH*vf&~R<<>mJO?K&WQY#__D)L1tbka4MyA@k(pVErNC*lZ_PK6s2G-R;=Ljp^lkYuF=+(uT_5CpiaKGUlWKPst>hb_aT&|7L9I<-~M!)%Hcwr1%fnKu+0%QF>&xu)v;vNMUtYoCOEt1z$NypisSPGmJ>y5E3jvZ)Lu1D;U_@*cezTKE7ALSlQQ-i6|Wy;IS_cS$jg(Ezq+9MMvt4NDbN1NsJl11?sH8sVW@BmU+NdQ3DI{}iBZkb(9vI{?ki=Wf<{tDLKs)2LXDaBz(2<3vVfx4Y`3*K4{?~)VYGTqHm5+{iY)rhF66y|_*h!{S>T*ELnpl*6*8mNTWUGYYOFd$|9-!z<T*QDJX*AwR}d^KD}K=0LjmCQg{OQ&Y^N_LD9T;$Gxv!!B01T8kE0vMC57@NrFf(6heWpEpE0JCW1ED44J^x;%6DK!S*%CfmI?2mM^ZcJsA`Z^Y<10b;7_p&zK_d|DMkqH)ffiBLOI-+}Db}5auvX4|`67|0mNgqJAVa_Kh07A!BoIKQi39TU_&PuSdf^nk3gadO^2t9-aV#0}sBH-xuxCmWy!bw*Ju%@r^o#6C;4FoD!CHQ&gZHcl#%s)Zswj#wr%6z~Bz{&bI;bwj*6z{q>fjro&&Q+8fpzJFq3>Vm$(TE`J!oxyM5W7c=Gtt=2=2TA`gui~>PMc`F&X{-%jKL02Yn_~IT*fhUtUaC-2r!A8W~Nm{>uQufaJ$912#qtDz6u60#<@GAyK6P$D2Q&k!cZ)FF*^D#x_VN(&jloEnjCcw%uP{!m4quI&kP@8v`DXHeE|+m{%XQ>p1gJ04Wd`sA16+u>@X<zYO4bRvazMmh4#Ib;e{%5EJK5AQ2Xw*CE8)>I`<4{t~kt%>i|i6kBE_px%xcqG}UdeG<@$;%qxp<iUHv&GD@esOZ)`aa7KBmaA>Gbe#udMO6BF@@0er6iDCzr+%{DW5X%Cc{N7`VA5TT_W1Kd?AOjSeTp(G+rA>(^n0aY=XxF3ipD9tLZ)u#6Msq$vR;{G}_aNf9Ctz&c0Wv1)ChN%nK;T8-j;0UC_D@XOz_jE#y^=!<_9hu(UOI5L;<@j`QSh?y0ijPt?C=mJ47i_w#$cN?`Yev0x9q-Sbu5Gp9gaH!u_>OIvH?lvfGfyhxfr}DCTC@QiPr+C<M6#u;n;vSrb5XSohbftlLZTbATp^+gMTolrgIF<_L1+>MJJD<!CMQ0WBl<PH7*T0MdrDVJuez?9U>{pX@4<UI9)x1nnX{O!RG5&4vl&}>+x?^On}{!O=P#At<u8`9R@zd>9H>I9H6#qtc_{lQndpL%k$WE^t~T1s+MR3PR4g-AtU4@u=c!U9AfR$tm&<)hiTa~XH<dIr}})}!R#@TA*pgvR2$CPMy4e(SSH`k^jD3-+%JGWlBWF}J>wr4XtKI2FDETawLd%3ZH6;vfe{C+1(b9=#>$5HQEI#DVpO|mr#8ip4P*h*lN}wZ(v7}C$BP}tzRFvqn#EDZptuB6<|#;J2J<LHWeGK3k{nRpO->J?oLmkIwM%(f>{Do69xik*GUqvZ6)#JYXT?a<-|2ttluShXMM<Jb9ehHuL_le~M_=f}Y|^W2?j2^P*maZvI2d^7E?!SbE2C7*;BM)HNMGa7uf*=9OGL`JSlH6NVoSG6@jMWC+B-se5mL~S^dkaGt7<MP2h^Z>MTUPXqmfS9Az;-#Iaij~2J~j@s&<(tVEg6luk0Az^2!|==c*(%V1*-+oTK*1Fsf=(7CdTfJib*e5K2F5tj>AMWF{w_F`H@C9FErsEdbE?gR{IzUNK&299g79_+lv^3TqX>posqo$C*f#WT<rIuLt-n&e##LG#pn+#Z@)-WwZf2t}u(=h4v<0`B@Q`POa45Eup`PLia9#s4Z57gQNKF$M1u#W)qe*w@3z|X!?eqrsU(O25TvNxkvQ|S0bIraw$V%^>zn$)4#Cnhr_e$*8G<$Fj)l;q2hsrlud$2P6<p|0;pvH<H4b6drCKkb7~&Nu86b1JgXELVh}1e7KYH^or`$mm8@Xpmn(LMVTepXiprLvTb#jY6(B1eoG%-2*x76^kgCP!9nl|;MrqyB^qx*Gm<uI1)Ro|n!eWEXq`NY6Y3CG(v_%|@L7d9TBsgS}63MM*=qOy56TDfhJ<wKIU<nb7Ec@`+96cj3uoF328b{rtfZ$AAzMuiNkSTOc2Q%X9y`(!8y@&4k=roFquC;<6z6DV1D;N!Rf7<3OS?+qJ>@3w;D6_815~Nq?xVZUVKM@y#Fnngi62j$jhWF^b;Ph3kQIoMVdN`s0FwM%LByBqz(Laiu(ZQpfS+qNq$E!?$^*=#jO3d3OE#r2UJlVaFB_DVDV-U6jMi$2(V1|8bX5yx~EQWbh)KDE}q94nl>nSJWQ;k8NcNV64>ELxx@BUYhz7;aOkIKDtm@m&h5uw9QAYF&G+HfCz5nO?j_O~%Z1e-IR36n+?1mWUsf$`DB@7A11*N@RAQR)~^;NzOr;$r?U|Ltqke=Hx6N<T@OUsk0+4I<&NqQt7OH}J|`e0BeT_wm)))~CnHh)VW)p-@{*15%Q#5SE90A{k0^Of$bD`XIiMwJ3-l#-LeD;}aAiDT|(&Lz#)DYWIk`dz?fdt0N5#-wfTnjWL)$Ox;!7jx9W1T7qa=>^N$XFt8W`b-b7L#lwOF@sarm7cp?Io(mMELf3QcMVv&dJB?(_N12tL*zj<1qd_nNWQss}9_<i-d;68=DFL5xZQgjQ0F%UEi;x?DU5fHxO0bo!#$T3aV%R=&Rdgtm#OfFjnSk#WfCR=ZD!>sH?onoBhHg(ZD;3U_wAs^05U6=bz^<48yR!w%{&p^Stlu42mSywYA$cAf&f+6ijKM{A8df1!Hc)*$lxB;7qD@0@+ohu|lJ|%zZ_o}ZH+Ml>fLpiZ{j%MbJ`1glba8n!CN;v1a=WweE}UQv#RWv(ctuoRTOy8_F_ubzTjp?(Z?D%UO*!9sBCrW<r=&Boz^+ihJ?m|E)LOPwP7n}9eQBSms8PSrE(#o?=qX47?5v}4XEs}1&%3$;>pbY)joxA`Ni0wA!a^fMa8L?&X3KWnQ>D&}Ngtk6Q6W^ch!LT~1lRwcmQ*AS4Y&+Q6oTcBQ@>{CMOVh_4>2q$;WZz$MRg+jBhv2o-%wu^B4?DZ>1B|RImWE<&SNP$ptKk9kYA}sC{9O8%@Isg?r%BBEih^m5UR|)G~jqsVJi5NnVTOp{~7S>D5<s?_ZePRR_$PxKC$!}i{pHNJ*S;1kY&v`>d}U%xG_yfSYR98n>tn5QRX-6-#uhgq>dC?UgY|61WYVi587-OcJUM>OTb5ZAP!;!Di)~^u+%*wW?h+w^7v;s3n4a(CJuVW(SUq}d3U&)*HUi_asX>GQD}*k9cI`u;&Syk6kx=9$PVOFRNKz;k{d3@SduX$huDs?>8u5??9D((S>s)WLtQU;0FR$1I>+<CE>i^TBy$rfKZp#980JY<L<X=Ho5(NH!*sL7N5uCmEPBb1CpLOr#R5`sAzD$15Fkt3-%=C0FUr}9%nn5(q#?jyXY49ih-xMrFCdkeq86DTa~v>Jz@&m{+ufHO@X!E?<(`uINuXF#idqO>sg-JLP?meUw_Sm)-P@M?bmsU*>CC)j{}@}#R{W7*DrU$IK&~v`mC{ZorED#yu~IwyUNDvFI>1-aMgWaS5J&_lg45)E6^)|BKc^!;|20@rR#=}|8%v=t`C>+FLqcmm4n1)@O!D+Dc06a@jDUGC8fgdB-JKC6$pvO7CWQcvH<1j+wIp<Px&|nL990JPa@2BjsF+$Z@F+g-Je}IYz|>wiRlU7Jfi5cZvUCCY16w0NLyAx1dP<j-S8^O^H0h2Pa%ziUhoUP-GTbc!?2(|=V6$nWdP=852uFgg)CqeFNtmbPH~~>`)Xi6fV<dKzXDy#Gb5g~goITNGf^UF{LujBNZWO0tVNGu3aRqcrhwhRSOjY*;AW^uNSuReZqY6T)<=X#W2o4S_)13pTm|LcEt7}&{|E_-;6aAACF-XZ7o?0@TW`#I4IIf9qPv{<<ul$|#=&Z({U}+K4O95cfTBgH{$N`1UStca*<i{%sk_8~mvoyr8&3H740wa=Vd=gk2@Q~SY3h~lA-RCpQX%2Vz+3KA3-ocU27Mcw&iPeKX1!FiHD0I*yix5?J5u&Muu+ld(AzH!k93H(C@?_Cm>oJ?aXJ%O(rP>=ty$&;;_3lebqBHCXHq#!G5ZUN3JEUip`6w(X=yRyv&&7BaCYNXRSdfE+uup)Yh!BetBJ2@<GYKi21~t@v5OhpS+?yO<#J}TFfLg(Mc7s^DObgb`%xxlD4F+1Tx3#~_inc(=Z;<fVwBAFdnhSaa<MJp>Et|dLFoSS}OQtz+($F3>kn^?dY)nW_-!1Q(_JU#_m{2GigR^8v_vm>r%B;Y`B*}gIXdl2nWTV>-215+g4TjiPmMa%HaB4sOqvE`Enulo_rMl@<g7nYM*?u4?s+gO7j2Y?4cX1jc6`wO|bJOf<#czpmJm_eTcHj<FxSva6)<p{ml_!9sDec9s{9@Lrk7bY6rtNpxRQ4Wo+obS=Su9Bg3~KgVACRM=Y2GV3)WK+<IgLtvp7A?vwKNk$W#~pWhg_CY&Ym|Qs{)6tR5wH+CNlt386K{eo-x@(oM1@ir}{^(kFhXK0PGO!rr4}RKQY5|sym6NdKy~?D8F}UY>RkCOtlSU*2_wQpSA`ELqMH2D*+kdGax{}T8VZ8?T51`H9ZF7&*01;sKr?0b3BPdv=>h<tRgua1UKo;0wYataY4ao!TE2Kqz<zvWlVGepB^gQoKLi5=r;pK?yo0&1h5DMOAWig>7PaF1$bJ7dIL0ZW{i@)@Dm8zR4r|+I84Hsx@k!>?v2g|+`R@3>ad2voJ%PF5x<)*kZZ&H%{@c{Wz&FCwv+*Cy`FT`QJdr`L4@K|NmM6}E?5DX4<E`m!k;zQWf&9{jNxY|sHGCW81m%`I}7MGmoB!79vQNAIYY70)T|g00?HcjJM356;j5`7KVs%;7dU9=P1=^9!N?sTNY-@CMaIx@BVeKE6hdL>Ak$3`0_$iVzDD8?(gId`<-190IZ35kG4c&M&DW+(4~B1sO96{NfCjoNr9KJ5n?YPqC)-LNN=T<S0>RB_X*B%0R2mQ8H3lUDlN%jcoL){3n-`~&Kt2Y<^7fE#1?N!khYFAeK?(xu<^_OJjX~$!>i2AP*Iv`qAFN<ZBp_%W*HoRk<*6Wl9(P1RG<^{Z1U7*)wkdHqEdGv>`eT7jtbI}_=~;#=gZ~i7$o}&F|8VyGjD6yy2u7=T6S-Y1G7;6%X(B_~1J}8AzM0^-nbt}3hQx?0>2g-<)QmNLVs+ND_1+;2K|sZpOk_=|vpOp)d5I+dp+xf2a>&(YuQ99CJ1)A?(3=tIwKtqnQJk5D7@)N(pxHp|6x{#^mp~`u;n`-?rMCCZO!o{NcASuQ9||q*0$%p=n@alIi$?(1dfKngPS+*e0)yZ*Sy1fcaTw_ho>^kF-N?8zPx;g$U!kl603R`p;bFA6*i$THiEaxzSgS31d>Jf^@_BnE#<yJxU0i{lSh=g}XcHshif-bh|Jmie)MuBvxoG^$DA>TjlQuJT+8JTSnv4K<fUprm9Tik!#}j-Z%0Z>74k-v=$@Uv?k$L7&-<=!qwDqI=7uQn9w#7^h<vc2;Wr5;GRbOxR$-!}CP;gLOzt|8^H83f`5FECRaQXxbF?`v<_3`u=m=6sI*@S=53Tt4v6$$o*<+e#dde6GK@Je)2tvx6$l5<qv;3Xl_5>?bdZEXNwhRsBf%j@<+(#&1D<U|~CWLgw%MC{pZ2`IR(cPdD0a6MuUJVE~cXD<poh4Dc`Zl2#g=h>JWidc3KHhX|hNIX_RHqUq7CXY#JuLNH#NyW5s_3$rH2=XJ?dEne5)K?)I=EspXLt~G4orMXu)grhDy%eaL#Q^`BQEN_l$uMAfd(@o|of(z+_7f%jjyESO7QDRTIr8ajB-waP-N%wZZ*O;FnKtOVTRN}l8VW2p#dH<+pD6dIi*{()I)SuRSJ9584(ORhk$HJJEU$l30WZhvI^pgo%ec58iBpQdJw+?e_jVS*VC4lUeFiYfYA{)A^`qj6<}F#05yfFOJ*n_o%wF>|VAggYiQ3GXUR{notgUzyd33~Pt7J`+t(6=hCAo%^A!Se(R<V)C&|2YgD?R34W>nSON}JQYv|dZ|eX{4pO`?LsM7iy8DobEzt)RgCu)h=z_p&So1AoA4l4Z8lUZ~Uzj)0lY68#VYIBmR+R%mN!0yiVzkSS7^J(*G^+ipYaAoE=)8_wkkA}NgkF4jD22aC5vT2+T2C&7$XG1q&GlSmLd2he4!fKM0X$!NZNZC-&M4iE_kI!vgyx9XmgD7B?Vy7It9eumTw5{}g#WEo<EO#$)aacj6i{jSs=<y|k+&uq62m*UXZgi1+|evxQrFVv|q8`FUcun333MO2vcLc>`g^cbg0MJx<<^<lXkxM#ake1mQz%a-K%l1rT|N&;f8DFJZ60zVCg+4bU@VJR7!6IdS|l5lznO=V8?UCzgmaSF64z;SwJ21+v(eJ16)exJkqh;xyPregZ3C}Wn$%&{rRp1%P41H_9W7G!6T8%WvhJ3uK>ry01lC5w^3lnuq80J8AygM|-7T}NG2ta=!JGl0Y@C^*PZ0fVqe7Ml=w+TnxJwiqiYOWRPhV`xAp91G9v2d=#Mx+h1S$`FHg5Cu;-2Wh~3kW~5aLur_63k)?c@}-$SVyXwbLR$otWgH#gH1TE<V0CjMh*?o68#g>H%8_~}#3~s^qdu`eBdlm5D%zr1tW0o9!l$hads~xB>FDl?E)e)lyyW~1;`I3H&EV1@%@}kP1IyK!{JC?mE=SZTGt3^T5L9QN$$?FIx4jw;4{(nL2*5dpZ*W`3*!;aMf-6-VpCo~yiKM`<<3^}==$)#y9`vU;24F((d>Xn$@K-NDqCF9nQhUP?p}Y=oI8VCDutG=tZREW3*oWK#O?gybb<bqTh^m#ZbW&y}DaM|O`GFVr+8*~t;%c?Hr-I~qmSHN+RMmCk@hTInto9VVsFUDO&DIRBFK2-rl_#;lR=kv^&5QV4wHhoZ=L$s?rLlwOj)eA$)U{&4!o+sMRghMZRWf1LG*(HY5oczso%sC@GXaq(_>Dx)im_ZHn5wK8d<2Hgz2>xiSHR6!PEF|Nv2LhkEX;O%5WdVrwrNfzdCY@-a;PY{W;Adu$$zO6R9+LVIo4~2_w$Ry8Aj^(!h?$0?c(EA(xb#jau>^%EEeffeg#dL+DcCXbxCL<S;C^W8$4FaUAB4AYKmfR7WRaO`$Kga7#EFm-NM;I%daX4gIY-pb)>wZ^4W{PoWZ%p%M1$};0?{J%ByUB*l>foCPS2ibHc$L>xa&IiX;(P@D{lv@`=(Q2a{#aGs}Fr=1h^+{xQS+tgF(QLs65<>Qmzu5k~Hg<p)r3y1%<9@Okhw7Q&CId?j6?2xS5<N;D_S&AJ>Ys1qQ{1`4y%_c2eHxqQDm=93u!l9&74SAdMXL~&G+?<A?QVl-Brg~R#SSbs2FvikvFLr4;^#4+LGLrcg)8eAM>BD~~yy!4VY>Zy;iJNb11m4XNtld>(!Jf-Dhl(u_(zz^&8<&$fRsFZD|ks9>SF*>M)SdM~CI(Z!mX;oFq>E9~3vhP!MHIyNkUKleTs1qU0Qxo7JQP7e$yTx{*<-B>dI*%OI6Vb_<RqDNR``LqM<n^<xnl$+!#)gF#FcFAlxRWl1iV-^SdKu1JXH6+!QqXA4tiXlfL%P)o86y2>9%Y%bOjS1{k;j%+-7ga7hSJ!q2T<;!$7z(W99>azm&ZpnvEy{1EEU6|a>5e<QnH8cfNBSJxMc7*P8zI%vR#d{rp1T!KBD<CfNDQ|`s!4#850#Nxkq4rP(M_${kwO(%q)Z`vMjEkL#aZF(~z(vs!5NpF}1<FzB#wbL7Z5#6}npGtf@1oR07Or(uPm*)K8iRg)MRyVg>q6SnaXSzZGnpVMF4H)&^LeEqxB??ev+&xkz9`2+og3QSe6rcmgZ3sCPWKf{2`%<;=E}@F@3+E>plo0cYnVgF~zWNl|1Ri@Z&~Fza+G?8T_=R>U|LL~EQU<zXe|vDMyh@VF0|Wf-<|?xqiyCQj3IkSL0pr#de%#OyWhD!WV%>P`n-s+O6exZOEWR~VwE4EB0k40$FIT4nQg5Ynv@YfQH=(J5~7f%_TZSbqTwqkJ;A@e|#HcHYEG55)}MG?2<gtu|ydl9N~@9dv1$k4F(U<e-{|LAi%BosB^;mUwUw&r7l12A7Eid0=VU9F{^Wkk{dG3dt<h?i(Wvz?dM_V-3$@eAbbRJ5k_;1Vh3L6$z&X@cIuUOhgVWDADMuWGIKVUm9%@)B%aBy)K@_fRQBR2*3{mOLwEcgpTv%qJ71-N)^C^NN*wSS#pBtSNX@l>yT23(tQ|&IsJ_ne%n$=Am@JV)xLW&&sOc&fXS^+*C$W8#;ZDMK4jFAaWA}enx%G7==DT(nH>>QT9?j`8MMPtxUuwsn%hANsFHv<dfL$_qO!10tZGy=IQa=VsZ0?z0eaqhbf`{3g)w&@%Dn(c<#BbeRQ*GHqSU>f823}qY~$-zpluMHi<(daEI>)ULk(({+)AO$03bZ1H|~rA#lX7r0k2>&iz)nL!Z3N+^nk?}B|BpCC%^_EhUPSfDl4^h8TXvk4DHVHY0Nh&Op@g<{gLmX$?J$6k&z#T*(3DCe{XlqCf+3a<F?ua4UdS;LY>wXJeGi~HX5FN3g#F@CoXjRFbu&2%h4fN+fb`g_m=bTKDGFe1G-^R9YM@AmgMne%|_UaLQ$RBOf2kJigxa-ZKT>Ighmhig~0{bbur5xWPRHMWo5>pMgwU4R?kSQQRzv9o1>s}dO6ZjSIM#Oz7v++CUdffh&U6wjF26pye`eycqOi@U}S{V?PAmrS>&Z8>3FRWGE|X;RXqi!AkQj;3cy8uk)r0qV_+i)!mpG^z)156^3J1!uq(vaAQw>}>90y!7V$HnNiM%2c`xUAi1C#}z*LW|<h*j=;8J-<A+a@uPV#Emf=p!oc$CpGwc?s^9vh?{t@B&D!6#rPS&9MJBJwx~6oA5?DIm%m`4SS?%vj1&w2QeY;O!a?kK}HOZE-W=l~TS<!7(tHX8^^*0(#3mykLR^<>l??-o`a4vvBm**1R^mLLooC%PS?52HUX8Ir|WHFJr2h(3SM*A3d~}%6=>r5(EbC?~4Y>Nm0`OdV@PwI_dqD>+l{NnNja`nt+~FBsNfcC@*+}Lq4~nG_A_qE?_l7EJ+DiidQwCjiNLTE8LYs--7H7OHxB6K@*UxGIu654hUyniIY)l7X-+-&`;9=F3ct6C(quhm(Q|n4)eumIT?nQMYF1=F{7=GrR!GdZ-7F~mFZYvq7!Gu>?Vq26ymKugbOumWc{JJ)l3Tu^TvQA<jyQ537SY9_*Au>E9xi{5{Q?o6=sx9cD`fH9_1-s9aVNlRzjj1%)7{Sjkek{DUK^}h58+j50ht}YMbZ9${*X4>@LxmEaA>iU|`5bUg;yIGeg~(c%C?MWOSkZlb6u8SA9N}@~-0N^Kl=wk`C(ky1b)1D}$Lp&|3p8&D-dj>o848LKc-4(<ikQWUZ3sN}-5}sH&9<yDdhuvw<MgtI>c~St(1j>5$}5*)bdF!VXZ=y^)RPAW+3cB^kobtmFcj7S5H*9%NPD=^~9V1Dumf;!hoBseue!meyP}B{=u2;ITpg1L9x|z$QlZY-lan&oT=PjOX&A$SoCozUSXNirytik>l5a)JtQVZ0R8#<HZ9<&w!BAB$BSs-@VMCRcQr7kp2u7La(j(qA+a&PALM4%T^<wam)5k=XBiSI1&T$te|4D5M|gJnWie`m(|Yc5vMHOMWxLO#c3*5%CuPmR?`e2|5(RmDl(;q)nW@O`z3j7i$&e7khU@vZ|LsgZ4lBam83}_8RiQ^el;{w3Za^w>*+NbDV_r#u@BKzi4#TuS#9p&ot&}W5!WQKXaz9QF__Fk=H4%T*fnMy+BmQRS%9zWUo{t>mm}4f$}4mvb=@cf?XqCqOVDdw?sVN%hoD1wgU->joJIb+*HSd-L<(f;SXBf7Z_soPC6{7hv(Rjha!qc@=pj%;s9(Y<*SuD90a-yH=Eg;{1Gopj)GD|)k!nO`IpaoY<-n^sm9Rty@zjYDP@}XTQ;49bYS`tUr1o_k%xKWT#I91cETtpCDDSLtrT}tKJi9h&v}r&t0j4%?;(Y?)3kP||tdEnv-M&BIrDi}aGbB#Y1nIQsRbNuPZA2W3V(>N6ujrm}!&Nai05q{gUk^Ut+Ekf;dcpFziL5|i9(qAUHYY-Fa2BDkyAd&#>t1;AR>p)5e>5fkM_Lxe;tW)Pn`5;eX;A?S2Q)Cds8=PrFkyCQ`aC{E-omomrn0$CgqT@5<2r<YQKq=ZUZBg@8jcDCxnN-;oS!ye4qd5jZ}{v1jyLO<igq2BjbtqP5%Z5&8Z3frC{^^H3F)w~oL#WPho~v7<bbZkM0N}7c373g0Nw0<Ey|5c%#9>wp7_{44&o`%+r=F((QHV1amYIm-Q`M-YuT#7HqyM#INdjLy0x;eKD!w@K*W*u;P&MvRnOSHCAUDg|9SiW0B*0p%m')))
_V10_EXECUTOR=make_agent({0:_V10_TAPE},dead_stock=False)
def v10_replay_agent(obs,configuration=None):
    return _V10_EXECUTOR(obs,configuration)
v10_replay_agent.telemetry=_V10_EXECUTOR.chassis.diagnostics
agent=v10_replay_agent

# Replay-derived production; sale quantities come from the live own warehouse.
_V10_CASH_ITEMS = ('CARROT','TOMATO','STRAWBERRY','MELON','EGG','MILK','WOOL')
_V10_CASH_REPORT = {'sale_turns': 0, 'requested_units': 0}

def v10_route_cash_agent(observation, configuration=None):
    if int(observation['step']) == 0:
        for key in _V10_CASH_REPORT:
            _V10_CASH_REPORT[key] = 0
    action = _V10_EXECUTOR(observation, configuration)
    chassis = _V10_EXECUTOR.chassis
    view = _View(observation, int(observation['player']), chassis.cfg)
    stock = chassis._projected_shed(action, view)
    preserved = [list(o) for o in action.get('market', [])
                 if not (len(o) >= 3 and o[0] == 'SELL' and o[1] in _V10_CASH_ITEMS)]
    capacity = max(0, 10 - len(preserved))
    available = [(item, int(stock.get(item, 0))) for item in _V10_CASH_ITEMS
                 if int(stock.get(item, 0)) > 0]
    available.sort(key=lambda pair: -pair[1] * int(view.prices.get(pair[0], 0)))
    sales = [['SELL', item, quantity] for item, quantity in available[:capacity]]
    if sales:
        _V10_CASH_REPORT['sale_turns'] += 1
        _V10_CASH_REPORT['requested_units'] += sum(o[2] for o in sales)
    action['market'] = sales + preserved
    return action
v10_route_cash_agent.telemetry = _V10_CASH_REPORT
agent = v10_route_cash_agent
