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
_V10_TAPE=json.loads(zlib.decompress(base64.b85decode('c%0>ZU2j}Ta^-)~b3HUEi64H`sOfIOnr1^%Z^PRl1_P`Y1`O}R?7l7h-z|$(_ukAn=fsK3TO>6G1T?!?B<n^-#^;F>fBgSf|NF0h`}cqO+pB;0<JGV4K7W4oaCr5vfBirI>;Haz;p><G{@1_#+rRw3uV4T1>QBG@^Iv}bbpPXT@4vh{y!!p;yLVsz`}*PV$E%+|e7bw(e(_(w=JVa%kL~Zk-+6O-`Q0xc{`~Ia*Kd6O`R?x5SBHy-hyOS<AN|AofBNm$?Hks|_~X^@cb~s}`{TddfBN!s_tl?%`|$C{zkGf6FTWi>;^W)n)3+b)V)L<Ax%}hZr!OBqe)ykvpI#j<kMH<=_wi%<bKOgq-tTE7@&5kz<L~kW^zq&MJ0>3>z0Hg3UmAO<5oA2;Ki_@4|D_en_TgWX*Du7c!7o!a3&J`n$3{e}zAVc0`Tn=#OY2vUS4dr){$LZ$f{&pz0bf!0ovSH{#CsE8S)~T_<o&z<dY5y}*mVK#gb#WFe#skCuS&O;zZqS~U%o6S+g`_TSJ&58@o}TpU%1==y=^TOlt*~VORkARGMyNHfA{6<Um;iR?%nYbf%Ytq53IHR1dAmAVxbR8ek8vp%jZ0L*YL^7xpjZ)H9oY&kj4k#`l_VG>_<tbn{RE-bo(I|kwjb4{RVL0=_9%aUVL+|(x;dH_<FUzo>g+8QT*YWo=g1Ejq3n4{IcX4`y;)~BCXSzKE7Z2&Fn6M3nCx<jeV(0T8$!1aMX|b5Dc}vgX!~ftsuf-I^G+UAq9_SF4t>ryYSK0T+QR>K(_fY6p0Gyykgx`5XQ}D*(%aS?whYHF_#WC3IRkP1-ZZvz>fz#W&B8n7gd5k{URWE`PlR$o%;lq?=4}{pai1i(bLg`o`3Sv5iC!OwBneFr5|AXFF%GQbX)#*`~qcu$sbl9f?o!dcIpH)@o(z**RR$;QC2tencv@k{CM~N%U?Fx2Q5aizp~VsyqM?sc2X<Zra`y2vZ4e(otH*2-|RUxm2u$AXgUfm1X&?`)Mre-@3^!#TE3nzPddK&K#Q`YPnNp=il_~Z6{i8qO8I#hs=nG=eh8sprwax;3o#F?Pd08~4W)lD;~=A;Uq|C5qVe|H_ZQ$X(&Ry?p92-^8#nS?^zSQpj7N2GgZ$n^if`ePmAv-zA6<VW;>Y+A)4xD8N<NwRT>Vw)8aqwEfG^6-0n&Wibc{kNj=$_Wz7$Pcc<2z!%zEwgV^8|lxAf=vcY?(^Cgk|=L&3%pNv4{)Z%!_EEvPU8ShuvAt6s^kvp1)|Qk8Pj^Q{EvAo?u4R1COIHoJR*<L5;N^YP)*zz<xT^rfsQeq(*oB{f9eI~5}M@Zcq)A9>95CfAidtyB--$<>JEZVJ9L_JCGHH~m?8(Rj-6r&_aG;F^LPF;Sj?n|9?C7#zRPvV!=w`8#0v@>PN{Eh%JmF(4Z+N<17m@TL2$KYqIZRVM9zx^+SSh$;=B3J-0h!hdb&_ow^&&vz)@naTGLNu5P~Iw+B9eh)r?e=xm?ZvLhEaC{}C-v_hO-)H1=$0*8?nE=ajtCS3tiUSE&1*eX1uu%q@rHjxHF?3r$^_1M44~t~k2@DIfQUY}kR!S}&aep_SS6ImzOUYH_@bkM*|AV*<EQ<VAFCXo(SO5N=2-r(5RKd@;FsBG(D?=g#ar*UYum?@reoTx7NW;|eN`Gtt!iI1zmcr*)1-|(t+f!H&0NWSWcx`!gr_WProG*?3PQNP+v@7x1aCAG48;asXx1sqi1xY>8V}KwFphMypMgsbTA9)q&qB8M|y+86C$ZRP^#4ie6>T`YIm;`qp>cHFU&m!Q?#-%BGc?x2tTDVWQm8MxSpvWGdM^da#;uita%wjah$n{2k<e0UQPrAgZGdU9N@3Eqg{Ol6*6TQy*O}h`S5~+$}#7|13811tTR*NFM6z}&R&uCsCsq=QWyd`EYbFrcBOo@qC$e$I&tqAMi#kpC|k)8-JxSk5+UKrGC!WTx|z&@IKJ$>3dqgX5zas<Uw82<R{zv*mv`=a>Nq;+c+4sx;f5hHfFkHQ~qRr+NPc-4oJUnp}q|7Rd;=7Ddkl)-RkrGPQeHgu7_AzO}90#UkYAnc$ohXZy{^No6KrS~`O1(P2)?**y!lB$CGc-QdbHM&~t8X6rfQ2Je7VoH+fL;Rqm1s^}ol9WZ6c7ay$0_^}R&BG7>@!||fC-vf;%j`q&bOkJY_{{Ml=62%RGf?r54V7#_cb5c*;*8>B777F!k6Ou#SUIKOOU3|A>EoTH_K?gsdpGY1OAy(dU+)IXP4jXcVuz2eqPl&0?E)!%x@|+x#bQ-Hp=!k`0jCn<6!3A=qZ=MP;O2!LA8yB2N+O_Moj%|u^8k&?N|CRUfV}2EvT=mdLkUuiXAXJ$+t_(hlz^3IdF7wHCPE(10*BN(<UV9i8Fve$>U>ZR(#TD_D62*21MjvDs}2?N7K8Bl%cpn0|LN}2r+@ZpIE&fd=8v+vt8=yzlxV2x1g%sQ`%;{8;rkwv8HA{ISt1~8i=cs6G}#7Ud2s6m5BtA)$Za_T_^M#jB_M8MmKzI3ZxVzO7*7T(JHQ@_TslGhlEX7>3A2>e^f8(dUmm$oYps;rlzERI`jkp<9=g#rWa9^l#X}%$^Z*vE2EaQthav99xjr~V1c7oEIS*j-ca=WzS)}gLd^lN*h~y02gRMA>!i-)0`OF(rDEWZuX%CP(IPD6K&0vq=zPV6=0LfA}w6i@_@SHQ4nc3%5Q&#zNf}k%Jarc3~J>i3jA*NU;RAh4N9~gRMP{>d<K6puY0rEUad2nEY1x)CB6(ny2_q-AAxPE$bH(6=QZ1|n!GA5GQx$+BSQstb$qq_W=pHy{Fo58Q(rG>o=8dL^nZU0r$yJ!-C@$DK_<N>{c%JUy>>7q#Cp*jve`F?iv5U-LUzWmQGM+T;BCeO}?h4n7v4b~wuUvR250QkMeO!!2G|9W`tMbz|YD}U~wY$dttNx2%;PyqvYNF=l_yJg22`(Ao;PQKz-O!^YfAzZC}tzF5}m)^_+);B~dsu&toyc(ecC-!8rm`!e^Gk^sZphsP~&3E|;dB;=9C8;qND>T48g$q{;iC(xifts#^<BTQtMUPM;#*HbeGMly0`ppKqC{*R+072)EEg8H34dM6dZ7!D>U9F7_)TGKmfagn8cPcT3$V_0-0357?%6$i-D9}qe$WS00vqks!A`0=v3%(!I;Mw$x@A$FBz$#;ZJ~%D=7yj5F_T0C=oPNQ0sP6ASavo+{bbiy?r3k?&f*ZemiscNyhNRz2-~%a`@x!`GekAy$nR;p*gTg}5#l}`3Wkm}jxYiLI`zC0m6kNM#Tu6)*>G8(owG3=C*LHkUymrj5`4%AlJ-(h0C%@UH482wf1!+)<w{z~C2h=%0S(kVswps{stvBL(Q~aH(Y>vR@9N3LC*5gJkD5!=P+16k+hy|M%u%}x~N8|#s-BeT%Gi`!Db3Rn5W;Ry=6Vga)fznCk&cyFQtRMaEr=J>xxi!hrJ@-ukn7k4)L@Ze542iCkF~M*9=fCJ*U@M;b_aIpm%-j_8g4S#=YgY}8CrC*{`F<10mK<Cv9B~HvvhgzRc8~1@>R(+wzVjy)T&j=PM72@_g$=zda7R6gO-AYRwh_fHx6xtQ4VUuU3#}0+mkx-n5VJ;02AXcDv*KN)JuY2|4!nSITrR3OpG-Xqy>7L=F3urL-94;LeRoy^HpXmCYyhm4ZvsYA+?JcZ@5p6TZB{$Ys|K6uV(vKIDv<xN%zn;0stHco2t12bLr78>Ns6sY<lNvy?VNYR-KiwQt1otN_0Qt-Lkn`fN*3R=nuT3nGRT9{&1dcZRT#(=v1x$SqoK&<O)kWQRF&|*3V$S6oR?OWK<qR0K=2=W%EH+I(1E<d>2L&Z6zp|A7EM<_U3fq>J*0)hpC6o1QUn+yF6~vPc0B6)gTP#bh!v?NOT?EBTed_%S(C~tC|BPG;QB#T<}v#f>S32-k+xZ`n(tQTx0a2agRzww_|MrzCgu;)b%v=L*{$dhV}V6P0W*gsvDcagWW3tPxy6^mV0XyUkx|AK9|E_r#yHnVdMdA*=ZP*8&gjp<s`CRW=$C3rWMy?Xhb+0wm>ic<8&La8Yb<_|92DaSr9zraRBKY(g0IYsL9!x?&kpoEOt=dUA>ew4CqMA>YeU_48tm*X4&y~lSt2c21V`bQ=_%n=K-Ce@VfTX3pa7g6Ky8$a9v3u*&4+&59yNRJw@@QsrvzuIqk|6)<518HPzo}|5o(2G099RuxI4B|qu_HoG1r&~wZqY2)C1M}3|bS~TGlK)=w)>}&da<G9dd%}()AVIWU%yDB3r;zW|swLa5whPG`Nx&BaKU9Ev&r%mg7up@+nnOiPce6**eR*t?=oxXfE;yj0|?W#+*%EIrkPN3u=30t(XQrl_X-=lxOU!MPc}0;xoq1M8tOw$qgTV8dC`N*T~;tvL_jkZq#Fr@b>z^Re`lKJ~{o~eg`mFvpPQxc)mt;NxYfBe^!ibQjXK1*DyGHv=F9Xz!TgQK5meSBPY-<*TSxdFff-^K|`u-$3K7g_)l%D&0bLwLJZzu7m<aZQREwnKN3Fq<43>c`n;(6F;vZOzz-@ONSgW}wK)lQtbC_S7dS#rt6{~Bs;7s7nsuE^faesOi>EI0k|=-v`R?vl&y}CVyZp!j#=m0eF@@J3XsxZ03@?zqB@g@>2^b`7x5`+RsLKr8mn2=pJ((#@oT)^crORt1=LS?)0dRS}AJktzdeNf|Yj<n8m5YE}3yaT)k>3mx?ZfIGsxFO0&^Hy~vHSeJ1zy%C1F;B$PfVE7srVBo(HA-!0gCnbtC~v|JLl`0P?}fU%_;%8m0&`5EWz<qyt2ZQrzT8nD0Yk#`U+~XiD#lxPIa)8cKco&p<EO|zbZus^J%dTgW3&9FWt+{nhE%JgVLFX&ey)p^v&olD~jo~78>5U-v0czgg3aR;D(5v#V)iDdL3V4K5GU~eL970ya!~6*5dI&EA+lpa?T)N=c)TU`vZ6lzvN$TP|S#vNQmi8+PuAPcTj`yK(gO@gCd?)n#BMIv`@2Js(f??w}wTd?$?|{>l&H4SI<ijK&l{Ti)Mx$74g3N<oWec9cVt1$nFoX_qdm*@YFtWTugZ#F3_@5A~Ek7pBco2z`w?#JJQgVdj}}_q|U;IJNV}mX#r71{N$j|LR&98Xy@Sb#hwW=(c)2}mS$+<EzoEeB@K^WrrU_XCc!GNYb>4TKjTBW<SvcR`WF8@AH@qpf1_fTOa6iaC9CK2_z4xiS`+l}89y&U*Uo<!ARUbn?t~yQ75G66=p##P0C>R?_>$(-(?YjtR2ZTF0cmO58Lp5a@SdJq@1Yh8UyNU#P;84yGv$f^OJWUH4%Y6Vg7Fe(s;6LA6Hz)CgVci+syJJ2N@8U}6@0s=0dnM<R!|APQk7*rI3<h|X_{j>Szv^~bB8DV>Hhxnog!XZ-T*HK7`2mSdQs;yEbxV@A=PaG5!7vbX@E8YZB4ND2^?V6j~Df5;cloO_O@3dlME=Yb^?K9$>KKOW3%ZXHAz%!tTvfrL*SL`gz$K>@9zTug18B17G1Bo8{Oyi20a&x;M?|S$<7=<o;EY_3)~ge7ee^0D!!i}8<3sCP$9Q{6}C7==L1BM<sqxINmY&2ILh{eU5y_7A&J4w(qW`QiEgKuLnU4ohY`r15Hng>#}qNIjWJ1_Y#E_j$HE(cRnRyHb6JgU%13GiQhuWTg0gi;(hvIJ^gJhs9VUH}W(ZwB$?#Ybh@i@#@Z!;?(NwP@JXYW2HhR|JlXZmY*o4qZnbpdgy=KX-3DBC8`ARGjmZ9|goC;GB+d5D5``hn|&e_my@jg1AFpJeyMMQ#bi;0+LjZkRdKu`i&>}*)mGZd2KBNDG~4-rn6m-ZI;lF4sbh`XXQ8!GaM;4By#FiA0#(*;@d?4;OYCOl>P&SX46<=*F(t(5WANJ25#T<5(_)|894{Nx0|VZ7b`F_&hGjjFx}^G`FIa$S+zv=g&jXBIgqyD6-N?_QV0Yf!7TYXw2_SC}`IDC2>#xzl4wc0LJ0Pj^vrQ36-ybh{}b!d2tAC7rFtgz00Lfv8IpO$Jecixy0xxY@RS73C=CD?ItY?NI_r@_@g|FFAsW*;_+*M2^cURIBdhN*tk?NOW8yC%816&05jG(AHfVizs{s9i8}Lox-mw-?@EWavgr4-vUhnI4KZ&;M-mjD~=`_oNR<xjHb^RAFnfKbFtOc5dLLJ!dqXV<|{xFqbN|jj})}Nv`+FO5cTVZaUPvSVrKLb2q4Yg^5FSgypFOXBZ{wsNP8p*@W^rgqYICqMe|GFfT38!YgCQ6sQryC;8tX<^w16zKN|h3SqNs;F%(x8Vm_8leS^JneNE1cCJPL<j|aSX)VC%F0rHAJt@B@CY=W_<^MuOW2M>QeP69rDg2&`)74%|JlCjgH^Aw|Q$T&ukapT${Ea?6sSdpu47efh<XrRJcHlnEH-+psEj1=(MxVGd*52ZoC7I4)jaU?Y6e*BR#^gFW;63x~dA*Iz<$+M=-y5w8{I*`hJy4I2o9|Eo;IW<8G<zC2l6&^9?a13TV8K%oqVr}hd!{nrFnmRl!qIk8eSl*q}-BZ=c^H3rOLMR7wFwEpSgZ!~WleMJ7?^VD(H9Jb4A%gfG$cvb3sBTPv{i@!-nDGYvWz2;F`zzki)K(^56w2nk72Se}KCYM)FA$)JU2ZhhX>+5faiwT<tDIZe{CrZnrpmk!R7}^%E|__BYS@C(DV8CCC(0s<@)%V`-Z=yr4%-_HKeE<n<z>*eq8g7ZOM`Omm;|#RE7w!$(c+K5ih^$u)B*~z0R=^=w1F}xQ{aahDRuAb>L`>&IEqm1l+ACp+vPY&#w1iXD7vVXQ_2%;U|AOy;0g#=&d>*3#B6t*bcLU%JI)$rH`oPA@TFhFObQGaH~k4AJfCdUqMFW|_!4)71=)s$S(oDGxC1x-768%obSL3-zXX^bUg*DlKqf8UZ|b;Ffym_W1VyB+_~T(&2!((Yd0>`2Ddd_dCX{d_7Z1YPB(VJ1NLT@T7ST;2?58`-1@5@$C&}^)%lML#Ppv9%a84Bf!zurio$&MrWNIr3FtjRWSf&Dn7s4+F-z#9~V!p=Y;V3w=k=C=Sn+bhYdXCSnTx8EOF;$36+yAP(qaG@GbiQJwz}l#|8f6Zf`1U~s>W*_0CdD3YOr12KEr*$`KQYXJy{V!czmbX(qzhdGco^mlooSnRQ8t9^D(Bf0SWuwGo8tE(24r%wBA<*5atdjqs$_s?i0~EJV6Gy=ohLO8ys<bUM)hVmWM-}Scr;=P^dWZChfuW%_9c9ac^g43_2Y-14EK>yr7gt=XAQ&S15~d>VK^Q8YpO0F@Qo4#)`Y;=LlrA)9dwqNcEK-^&h2B0H{!uWr(Ok1PUROGQL>YYu(O33#jIG$Sc$25=7Jkgs<>zc&S|+g*Zv1e5(;(aO}_)#A_X(#0i!54=}v0I%T%VNEMiEjX|n5$%u4)f+naMt;K$IbxuQB#(5-s1q4(xplm3&IoxL0|Ah$=LDh^i(pf^JN&60;R4)2*H0#*Hkgq^x;lB7UMj}_>5Y&(Ur1GJb);Kn8-w=9H@e00ZB>h1dD!*Vv|nF=!z*@l6qkTwaqLIKBE8E`ssmdCDZH5o6m#)Q&r@@|@j=B<8aMIF%!QE5*f8><6a>d5aIU#hYms<B?|h++zuL5gSc;}<4wuh%+49Qw^_zBt}ca}N1+d(lASm3GxJMmcZ}u6nS^BR1{O_zw#qy%2KN6(&}h`e)y_XT4P|)(ujkUT3)Yi`cwde$wdRd$X;2%t()Q+9mpdgb84(OWn9l7Do=H`3sS1^!UpB7J#*y1!zNERhD>+>?S9DWgJbQ<?{~Ct9h?Gu5GXX1d0v{3g*Rr)2h83Z_0+52dskH=$3`%4W`Q&U-dcX((fe0A=`qX<kL-&vxlaqu`NSdCG8EsWZ-ZvV(N|LA5C<UhbL&><vxrwjMSi${Z&b|#lU{VZ41~ea+Za>aI|NOVX$)Q&bs|xgP*#+IwqiFAB>&gLQ|qdND1${zcL(DlN8vVHH>rM3TQ6$E{K<c!A!oGStKx9_D;j3s>_d6SS`?zkcG6;ku-&SeU^<eS^zd{nfPxSORRu>w0PuDuuPx}NRXAm4W%<<HbQ_tI0=gVmnh0j;R=;S(4<C8{$V|8R<x@GM;D#tKt_dvT(euSnxV>qMb%cz_*KS<5-HQKAJB+p1KN<GriAp^`#)1P7GZ0F4mr+#p8$@BXSLgH&?0dCx7yHnX-K7aTA)C~Ojqc|9ozY|sPh^vaFjy}X?jsCUZ4vlL9zA%QPpnI{1jD$1PwC4Ox4O0lz0L_vDp5Ol)5f;ihLk}C@<`DxrAGNGkh1(0}&$t02^)tVg&|5?R1VIWo|gaFb?)Q9%ca0RSePoIeR&Q9Fv{p*(pSsqnAQz$#9K|xj$Aaq+G!)s|>WK``u|96-`FBc%uX&ptmnt0MOKHokK?6B`3%M;N2B5nIE5!`yQLx0-%TQZ?^&)eh;B3Cq<svRU%)Kg#Q2zq8J)PaCz3ic38j;0c>$D9c401Hp$V_M;ALJmwj>s`1~E}9VUR=el2K3(?YC?s|kPvKBn7q1f?_<@a<GuL#=E*LpeL$`&1q7gq4ZjCfH6yuklu{)AR=Hg&~3iQ3zV2q=t%;hMQd~?l&Rvu(#ArmDAG>vxCjK0_0U###)&JhFwkC?k`pKHf&nCg0fAp!K1<ek7s!RVLQUJoYp+-8DC>MRSUcKiA?@vncToMd>~4$vAw~NP!D+0rpkytZ6e~NF<R>9cUqkvtclKWp!it2c7qV<IId;`#num+p^l)TmI4kDirIcCABeL&PNk5z+YQ5W-WIbf8{fpTtvACdF6gtIzE+1pI5PAUG*ivbRCzOVJPJqH^fdmg(h})zF8UWD69e=9dM^ejNPu-#QXa88s-zRB#XJ~}MDY+4C<Pd|g_pPmqmWSf92aeRpJH{cve&;ol&m1oDr&O5bc6vA1dF=K%dk!sty+A@y!nMHRq>_UUZBAnq_(}l1lnO<=!9?E06)Mz$tg93Og&3%b}T)TRoL>nm$BoVqim2A`QnQtrZHPGJSK5w<<|O&VIC89Dq>{49ZbSHNSm2vI+U@oq`l6>br*p^y4!|0FsWJ#R|CQkQSlE(Ly!qWM9uI;Px=F?^a$5Xj(&3JHB?lim9I`&G$^y&Uw8bzmHjKSZUN{x)I=XjAG|HOd#D+Rj-?bg?<rmB4E0u;Ne8k6jVB~^y0<A6AWLk+q?gm!(-cz-@s(`gI|)V7NB{-gj^}5X;H00l3P9hea2G{8PDU(_(-htyPUzx*0t^Gj8D}r=(BsZzD-6g?`^VPP0*+CS!Vo;;YBV|MT`2*>hMOY2scA}6UZeeO6R~CWxF|`+?-1WJCp~6@o_;X7h^F&g+EX`mjUueoyu2berZ#L$Oax%|#2iS(IdA`sHE<WBsGGL2%9CLsD5XdEI}UE$u4^l4A-j?UKe&n=E{H*W{icg~MEzCnvFv|Esr@oM-ZnTy1q?hcQ<cWNRWn-*R-$@QN0=v6vA!~k)gxH2y3PEmyeAGxvrCv#nJTh~a6xLstifw$S|+-T7p%*usn<b2k)2{b$BFPCPET=!PWJ#&3+BkTO;euWz!P)Ba&!;#octl)5C+HK!Btg@5jI7(`I(7SuuS?c(nmoyeu-ZX^gHA_CqLQClpbZjhpdcM;5Qg-JUvx#j?Zow0fi9fvAd_E6WHDp#r<y0i3h2%dtP}&;-ho&JX7zcvdqP9OejtRDwed?7JAuiTq}V(6xnu1V|Y7+v;ZB7cNaU51jk-nhF6Zp5W+sNtWFoAk*$@ja++(T4a+Kr5%JEc^s1g4h}0?t5T3HG3X7|?6#+{QwfS!rJTV)QuzM*9rioCY3DZ7#VqmrVADNM^O6COw0^S`ixS$wZdA`k)GSfe2W9ONqEW(4S4WNpr1UFlCrKg~q&d~4^>Z}(l#DO;8c@!`Yi*gEw@&eU$T)@EaMpFvQxoRwMAKZY118hd{HI<Gmnv49m{R5R9CUIo2Iz-)>i8J~17V5(TovkFiT@2O2Ww5G}@nY?vBR+72<%NoDwQh#+r(Gq4scipx7CYG|!;lFe0|RJ{r7BL`5#k*o#rc8Oy1e}1jkC!Ws%P1H?eMkmK`4NZiLGT2Zbbmei2f4vd?9-!V92ZlU#Jdbb?$WTPIU3JpBRQjoVj67*J3caR=W56u)lSfUdm*)JL{Xi7^@4bHKgx}-K+L3c<Lk2jniGv612tKelkcXcZMfFrjM;UA`VZbMH|G~`a#-rzSnnikm9%!16WSD{1xk^UfM|SJQm@=3<|1VWgW>9L8;!B4I}&Q71~BYkf^5`AlRNCJGo*B6;6zLD-KeH?+1^JreXs05Yzn^0$w9B0?!_aj-yk7MYU)s_^!?>`v#nYQjPrGK5WaUZsslkAxI0+oON$=oV)-wwtNyt23A)8XJNgU7z>J#@`-Wk17^k59RKJ=SFIA4_R`Wg=KJN~wnN5-(pxm~!%7nN(6Tjji}X!lptV(WWC!t?LAO%lhzFYs!#)Y*HCCcG%82b;2diMnBI8X{iV1|J3Lon75>+JMati!%-GJEcpl5zHrAG1TtP4m`B;Z<ucW!l;EW;K!2~ZKOdExdQSwy6Cv7LeuF@9P_YVLdT8>LBsGl8sp$iTA&AYn%Co)aCYi%?)_W@RZH5`ntNHL}A#jz=OTN$XklnOiA^A1Yn(Sn#K{0}%0T<MH<ADXn7sX$MK>TwUygqHJ;HIeIvLuLYvL0FPWu1oYP;{$Y0$Plf|o!S!!A9)z;&JareLYq?b-6AjsgLK&Y$C=CrN><##y8;Qr{ajfoM>01(l*@6xyqeilzl-_koqR!rm5_2#iFt<$E5p+0_&|Kqk<E4|0B|d%g*l5-LWnmmLvO-`coX`q=h4}8d%>c?(phW<0jdgO_mZtAaAX<)BleC&?*;xQ2K>M#hz+Dh2A>}{ndx^3n8#GC?OAQI_&G9bxo#ijm8VBcIFa`<Fvav8o(X)cvohC)VvMLD!xP9azZuqxLWPX%%@HYN_XD=Wq=qknuNw+2RQ;90nari>vTuj=o;bm@;Vx@q?J?aOB-IUs}afCiwLkQH>kF7XOtvDHG3Bn8eLiqNbtA9jQJnLY+q)0#KD1B1_VE5+n1b^sXu_o$gyWWVLj`yIqU+mZPb|?h1N<y<N%*qzrVff0bs)XYujmSU&$B3;8_2BqLG=l~1YBgFnfC&|aa*rkzdB*}Rqb6>vbQ)FPMz8JksR9GD1~fC%^Q;!1K~{rAU!8X{sL;6+ZBGTmrH^gmzFym;?<9c`{$Z4slgzp@Fbm>^2=EdgFeh86;R|MXDJFFn9zYqLqK-yDGQn+{l5qGSxAg7(q*w*CR@oa1fLd=As*r^&(TU?2;uQy@yYi&)0r9!f;e=p~WSD>&qhA2r3ER(LFueH-MVMt!@ax^@X?Y)hyg3w6?da%v8B+}-6_~S`4<t{_s>NC3GPceKcOGa!!E!5?Ne(%Ogs-3&ifby^EL31(6|*stlD%{c9ze^RYVG5TOKQvJCt{V*NXm9}CtsEQ(>=iivM?i>#MCJ{cb%gn53r1`q7rEhhAkWs=a}O}z7xMx^ZseIILV+yS^<@ok{R!)wNBYaH++&!Rc-It6fH3iPVOOGwWPz?{%&BUh2R_G%bHy`M0&}tN3>fr{5W6j(;JbBsW7YaDRKm^IgV+}0076>69!bca_4V>5D}i+unnMr1aUZu%?0=E`+?D6BP`|zx!{7wIt`Pi5`pPq)>3!+Lo6B?U<Fp4o(sud1zZlZwanF_Da{azI(Qo>X-LRPmkL8i)`hjAtaVEsu|Sx_G#G^Y=v#m<6nLuy*%`GuTF|I*+b?i*y6Ejn{~MM+$19@4E~-fq>1pn8mm!**i%;}l1#FegbAv6?!U|DT8zFBUSTN0&WIa8>;h7qzp}P7)W|<W?_G|Rwl{olhdbyplHGm+OEVl=X*2MsuGM~MZQ=6-!vYufyd0i7x9!Jg*6S7~PQodB{bqRNcbcHxLW5b2x{Evo24y2r~*QSgNDi=~)XCNzEYYY-Zg!E2QP*iQ<nzRi<Qbur54NU-?01@g}K-{KV$w8wMiAsOUo2EUJdh=j(7#w<Mbl>@1On4qx8EXUqkqJo-Gsuc;Z4YlEL<2z2HC~P+%4ssEsYaJQ9AFUNCh9rLdzbO7<^{Fbcys%shB20h%2L`)-*8eXLvY*zmKwf0d7y-FCl)ek?eZ!f#K_wQILS^4MqJL+#)$+3r4LpkV`13ifWj@1`y}{ek6-3j>)^4)WX2#ube?4SEfm?)=91PLXVH(6-b-2OF$m&5sw%P2&9r2U&zzYDZ~v_n9SXNlO8{}<to6Y~+h34q<M2cmO2>W|CTa1u<-$rdz+~#^ivunO=IqC^R|(FC*t)s{g#CpI^hXVhDQJp}b1MP|zhSr`Gi0{gmPI+gE3tG&z9&AhX5g))8IntWE0$)Otiu`R3kF#rmunhMdgGw;3aS_iR-;NC?);;p$wFjl`j@vRR&=fqcXL&0lWj=6u$F<eS&kmKK}c19gCon;m2vm6=7bio!zqnCqAlPIJwq~c0X#T^hva+Jm1;Zt0D(B66YB?I1ilq?B-Jqcjsp$07E33{v>1vrm+(<`?gBcQH``?XlRG=|Kv>RQKS|s0@mizmWj0+Sx1Q-dMU5;mVB7wg2TQjnUaCwG2MC8&Rh<`>Il4my^9AT;uC8$fir-)aZb@*VgF*VCdeHYN=Seidv#d7<v5GZ=ebZ_JMG4HVH+Qh8kwOcSYBBHpu*aOXJyHlg?-WCGC*onp>kMFvkxUrtj?7qBpNHiYZU$Q1nrRP)6PM(l=d|gRI0Ffy28NuVGPj8d76K-qOOXYvy>cYK&gx6tZXY}6$;u)RI}i#<F40BUK-82}6?UK%c{0YAs!L?dQ3EVdn2+^}O8Z;<AcG5#iz|$g;ypMx>A1eHgJLC;Ww16uhMx=F6m8OKwb+}Xh!x~OC6Lxwu6}%Hokk*OCs#ThNwRBxl)_6+S}q!|I8CW}0I!y&q2s_0u-TeKPZXA!;jdfgNHSrU`GdiZa85}c-*wHtm8p)Cl_d222AHSrn+>C5&SxZ6IuqNSp~7LZ`%~GyC;QzSlfFF;<Oc;8%mf(o&>u)Lq3xFH;l1DpyFOwmW+MtoAm?UREl+e>)u6Q|lZXRMAPXCDO<upa;XmV0r0M`cY(IjDUg8hOWmtmEs~wW8+jJphU)?YPF&to2b&AaDpvS=0uhhs_BJ?<zNh1oe#DqcPV%{PQaiy?h#B;Qma7Zy9!M;S6gMm^HyWbrz22bCBG3`TcU%XlV0kUOjWq~5c@Iuwe8eMaS4N*%v>Yy|sI43Nzcr|F0U`vzbW$lkcE{$>zie+BcP(%s#-QaRzVc95ggQ;9lntWSdr;FoLn%CjUSDR45`C(f|QXePu(X;(l1vNR*_IdYgP81Xd#NpAt8wE{s$pIxIH=zpK)&dEuiK0<IEa^J{O9I;HTqL$s;OJx?0IbmNrd>=)vQT*(c2g&w_E*3FH6^9E;4^?aFNM|6o$U6K56BV(YF!?fcAMz0EdfuN&o}Bykxw?ALd~f4(spv+z%OxG%me&&T$9q!@Em^M2JmBo@j~XwD-F$;vK!mlgk2@pZ}&1LMfWFIaox6%V|y+;xFG8C4~*@=PVmBX7S(7l(a_%NOO<AZs||DD+b25a9A_c<huTx|tBx&`DYcbO78rqBVB8G$g~oTYzuCys5J3`(B7k<I4VZ1o8xQ97CPMvFi%Es_S)pCW{9dDZ8)s9kqajtIb?~^Rr+rzMxQsUh!moBXqZEmzpspn0{xW={*-8_Y9zkD<Ato5n(7ryfE^nLQF_2(@8s>oQ?RZycS?tNJo{eSD-HrPU!q|I=+7cpGyg@388f+=Ua*!r(vJtEG;At4o;0Jq6iVn?t#d7=cEftDrHHZjZw%8g-W)wY+IMx{_j}2F=BY#eNvrfbrikhTtK<{dxC^!KIxb$)hFfeADMLH)>gcD~(#`PMCKCW2mtSYO(S-wZlXKLrogC8ldSm|H4T9W>DW`jXt15e6>X0`%a$T<}2s&<)YY8ELct>+Zlh!Nh|2O1!Sz1`N;gz+EgM<HR`C_|}K1i>oq5@<T0l*49mN(eR`7ad0SHl|GyItf50m<n>_Nw>C@cO!$k?2_uBt8NQi78wL;CAIppE6o(T^U!6gP^THe;B7-p0xo?9o3kA4#v<v4S`SNh^vW6+v5A~8b1e{;eEJ0pJkZf^X-$=7AVaCL4uo{wtgOk&w2{S4a6ZsvXj8n5ulc^Oy%A37C*}G`_?%N5Cij$vfHi2<G0Na9SkEp*nZQ+s_k_6)Yc&(vB5*`co%};b5Fp7G5OpVSpCRFXdlpv2<Tp890KUdAMhc~P06^Lo_z5$WawS2JWfhGg#8Xd`9@OUzKE^?5OZ-&56|S^}Us5p_o%(QR`8La!U&4I38i!6JD9x~&{j@-Yq;-zCe^}C=B(Md^@WI~W^1AQb7JruY)F~R-?}SgUs!mYI%^9q{)}~y5Y0pQBT+cQwZPTZpZ*<xr>#lCCHCt}gkIK2+he!c{r`27rWd3(o>RX2i3yVDBwR42&=;>@Nrq7vlt~Vzr)eyaSr5~7#fI^K;JED_4)~(%DyTU_?TtIIuieIF=SFu@eJIQ>XUL`~iUjRyMkOb)-5r{@htsYj0^DB4fyMx0uC18u?mav#JC3!t6`@4NjrcBl_<=m+h>BMJ_px`=;3YG(j7`YYBxj3AbPjXw5nt9=HpnEx$Sej<jEs-X^7P|NfY@5HrtXlEbwK1zfE!XwT6}^S)^S2wTI=Oe46La=6m5k_ThR$YZOIEGHqk&F6N1Lusg=Y`gIhkjAwp&y_tjWa|&WxL1MFPdsY;NBi>8r}SzI>_r?N;Uht~^NE2QCONo1)ZD^LU<Kiu1jjzf!_Z*lpAAFZ@*lu4qdGNZBR)2abL2#ufhEY`rAlmsnp@Sp6JfCbC68d>UG&^Q5Z1XQlxnqj4I-cw?|Bi>OXJfEqfTREAG|AEMcjAQx=llVSBAKm3H^RTAsYhDE&Y^LOGGKuxMP&jCUw08MiTTZgOhFT_C%`wV+0Ud9<88K@8ppk$CDT*NU^`#Bb(?j16)u=ZBua!vMnn>cZMePNuOcMTKMcPDmwwiV(j4?P6)EP85KAgS;XM78~5fZ6W9)h_nuK?$5|cpk*elbhIC+IUKZ0tP4HfgE9<WwBlok?cEE59#bPq(On}!aV!U$(809k3U{0#1sniPt|;>0us~|JuCxYqbrLx1C(Jy*aQ+ufq_FcA&=+;O8V&Rc%O-vzSmSkVAf;hNtRu;-i>tnlJR9H;V6W+c1vkF>VDyC;bI#kl?w9OmTcSq0}OXHs<*6?;k@61DC~IyDm^0Jl}KmRi|til$+|Yt?uKZ4Qm3TL*&jXpQh}gvfE|E0Cz2E!S3j)G?z<8{c&Ri%Y=Z`9Gc@!)x4O=@MW)6-PQvU(93YS5bY|!^2SZ%2LlE7eu}j(79cheAG{=l+9e0pQ*tsdu{iYt>hjyrjGYEk&1}&H=8MvO+4&_59?wJ%VlYzQqW49I%dwg|^SzdZt)3TF`D0G=evwM?%xg3hlG}~lmR`JO6;0VfQ4xYqrfSi+HtPBG2Ke;Nzk?wwWhGCdIBJF5|6{L}9Y!Vlp$$%hbE!&Ho4T$iRSX@LY8^Ryf3GN%n>3lox2$gCJdmY#_=)W3dz@!%eaX}I#dz!(d!iW!Zj^NVe!su%_=n&S!n&Tc?r+i`)EMaXrv$c_ud!p>MS}sO>I7tm5VI84p$ETIIbpX4|TSg=*cSJUN`Qr2)a0kwlc%lTe7Ub<N*<?0Q5g7nzPD8QLe^WwvoR+%d870VSO7x*|-v!sgMiaLf1R|qDh(ypcGSZN^6J~oA+s|+U+oDR{g2dKEQml>mk3t7pFz~RhGL=%5C*lk*1pyBrMH<ui+<X$th7t#v&@xDf#V5)~J3J9_U+cH?24s|SJSuHcHLCUuG!kg@)hv%h72L71wRj91`Bs^cPCJ;Zf!B|p>J%GB)MW^9x@_K3UJ}{Le~*#K9o}5<Wr}<uId{V^WxRVydaNN1eqH)J;qS<u*i9FDEJW?Bl6?+njl+ov;FxJ-+$FGc>@9IgVhI+xJu?SDg~mgV&a4hRPPncWjpI4AwZHY%(*Ztp?`xFVw$SymdXa_b*}(?cI~B5Cy{h<?H+k&ZE^7%!Ck;~7c>vcQY8o-bLX9=qoHs|6_iD+f`vUC1sSqWRie66oFPewcpsT**=GU7h|M*BVj3ajW&ul0jcu8c~;ACX(Y&@{P5D*9<`)p5JVO>Rx+~vS_v;y)IbAR+Vz$B9jl0Usrw%87t(YUH&TTJRqRJ<XQAr>X!f|B6nnq%yL)p^8RM_~?^vWHE_qKUxpq5*qs;B|v$q@4O_%UKCw!dE&58k`KY**O`qYy=o4dVoj1I3B;JSa<5g%uzmpQ@|M55c5fYi1X7CRzQ2EbayM^N!}B4oHiA^txFl`D(R4YPGX>BaB(hig0ys0!Z4`^6-(ZbT;+a}ZTt=beP^M!Z^q}LBZdX)sLe$GvDEw(bm#{fD067eHf~JWX(r?C!9c~gH$nOZO$Xt&;TyAdhwnQ9;qSf>`?E;g4pZVysa0>2?I6)!=aa1)>m&If_6yA6R@BoA2-a8X`JyF)zWyt;14<hsIh%(mS$@8={V+Nmq1n|@`wT4N&vzg1f2jrd>K;7)HV2I<WF<YXvi1`0W96pjK%rz8;wZGY@g-GX94@STYft!6y#xM%1)vg2E@u7qW=}D({&lImy9eMTkl{Qv-o&T9m|A2Ki~n*5<2QT8F48SLsqWCPn7WJ-lH}4&VJMNTWpyOz7{(h~gYB>QDO^~Dhfmom33EK98j-!dzHSE<3qjmJ5%<2j1P^n<PgEM$>~9jo2C!Uo-`O?&ErGd7R`+G6`+)N9d9EFK9is4oOFeu2N49b8-H(bw6c#t^d1;5~xHPgp(>i>*)db>5thJlLeq`*?D5UDT0v0Vw8fNV^--T;_Q{3K_ds7+4iv?7V&{&k1)~a4_;f5(dhbl}ZeERT9HE0fOHwIi9Au`#6nyaeH`KaQ=sJ~-<3N4p(?i>$qsDcC>YeKs$#m?C(Ld3ZQ;wZcr(wJ!UY<%n(AT=fC+MXK2F2b}byCTeXCk!pv@uQ(|d%YN#6D_`|7BwB30BDG3`V7;LXD4s%Gu=nGn6!Gq#3`y&+xF#L5ZGstX+h;RR|6JhpiM(yDe6L_XFf0RuV!sD@?o&?2z;q(PaSZ-R%>u;E!6)BU;3OJ0JFhPMdpETKX%F=^{=5vYpjiLWo8H0^AIr%NP1Q2{cQHJd6mbC#Q|&CaY^`N=DWSt2=CJmry8jEg$^F1m|pvwQ^&BCYQms2w|WQ!=yKJW6V`)v+$%C>n33>Bo>z6QH`VB1GKM+Oa($nOWhy3HjUOASBMwal>Q*~T@2o@W2)r6+`8zHOEGfKH8pa`3&iK8GG|~)h5|ESGUHK|{l!s&t!NEm;P-e8OL%Ct`zXh*_IB!{~klR?t2t)-1uc+X`*)!%!nn^LryDG+9vnRs3f|Qpp(#dRqz=-4`yQSNR#rZ|ZHoO!tNR!}=$A<mOSSvFL-+=TAue;kv-(vwhPG`O?6!6<AHG?uc9$QAaU^CoC3~NN&KfREnlgVBym9_7#PUhYQX@HG8Ahn-v;myI7!=yrSH&3~p<o1v`ETRrVVh6>Nvh)C7w<jT?17v1U&sl;YA2z}^xR#~@*PmK*l#XDkR@KAc4F2RaGOA2Q1`u!tE>FvVF=7)bomGhJQY{3J2zw6KHM&JN+8AezXjA8%n>umo>4}&;l#DkT2&}#MjicLjk&+U$Ko7jnMpOKHB(U$jndaImm$IeqvEXu@0ed}M1+2wjs}#<)csZOQY>nG(WqO;a<`#3;ntu;i7aKW;iP{)*oX$QZ-xw#2JLd$TS+5{5Siw1D#>oPhZMPzJ=&+?g!C}TbV;bqV;XxT7Ym}TX{yIJiG_}n|P2Moq2k85lZ5Z}<6B)^lm_zSahfN9Wpn>jD@APCTxajdlVvQI<6T3rD<XEUhH(6k!Pka0h>=TfJrIk9B3GEVV6H8Q{xL{VUJ8@K*slwEwS|{DSglc-cUsql5LWb}6#Hf>iJO?t$yODTTHIS+JCM3a?PM~%_o7faMmPD{+p$9X%I}HsS%dI16`#CMI7za4)ewj@OCD|A!TEP*RN9x;Gsy<V(G63@>*I^`_HI|j}&A20U+5F!KeF!7XclwSb_=?Yw80$2AM^;~K+If6Fnf4T9AG)mg22^K@N-=9Hb;N9tbN|{f^$v;DHJC1*z{+6CiGfm85(-@#mPNsDVUsq#AKs1C)5g6Ulh*vK_^zZ!J7&=(_1KE<I6*&@+(E#yHr-{<qc+dJMjfMdU3CQLH4IT5M1YX4kb;iF3Jc=xhziY!B(1pcp^54iJWOFM9V!0s-q9h|^;dR9_>E6_Z6fWikvJXJrL*sUVWG$#L>=vuKHpZDNo+@2h2Xn2EMNy~bLh1I)nVbay^>3Fa5+qNZT3TcB<o>>H+QCO=D6DxlM5(40)~^cw_4rRc-2O0gy+aDI#Qc)HNF-_O^-`~X8KX4PriZAeVa+}fp#u=jmm4%;M^i<IA)t<0FK<>mJN!@;NEbLUSPi|!hHBCgv7(zH0%*X9B_h|z|9%q>0DRA%f_6%I^-l*@b33NLJzM}Qi9rzrtekvU^^Gr<kx)pNX1BWO3eTY_B1Uc#Z2)E_GN+~_O-}ha5*8M2$%p;O*8U+IarsT$E~5t=$WO_j%Q36oq$EW5f;(Q3}vQm&gh3jnjmkCb=JZdGZ4q17AH-$OLeF<)|E`i4tF)%N}M`e2mAzW2(;1(CM{N2G<nzYj~P^nrM)9~Qb^9g#N>hvL5~>qs|RQXI_q$<)DByIf_reZHZ>QxffdHTl~n=10=0QecX_R!R!z7#;B7v@36HPV-9nhhgvKB^M4z&6mzGyjo1-+Jq9`pzPfSQs#)}L<1iJ$utGMxt+qs;N%nK`oRJ>Xnk})6FYE|~A$zyx9;)I8Rj#AmS@3C(CXGlEH@M!FOQM9y80n}|Ox(Loj<|ZYdMaR6X(J#3Zd3PyW*>@|NbmN<B0&w>Ja60FO1taTg9S{a73^t>H1p#qwR`tjxnlRh|7ERQ8+$8y8QLqTP=v842TWFU2HAA47DW(KuK-NzJc(Sv7c`&xuP?$-rsn)YQC8_>W_^hrV=ivv)^O@U8f&p~Dsp`qSgh($91vGg9z}1&O*;G511s|QR?qf#T_G@bzUOKtJaKDckMb3Va5uz~Xy?X=~UA_<it&`4VxZ~dTArAAT#6!Im_+20i^nkRefic47pei>V2ms2JGKyTF7t!(!XWa}3Z~_5>mqHhAqH}-w!aDc<rj2%~M($9mjd~ig6-x0CboX%H9zDtl#je^~ryt03prFymCt9lYc_m(glfd=TU}&uNqSimzbsfFMPB;ME+h*jH#cd$KhB=F_hZ$Rvgd!uiOjUTUBc=9wx{BxN@$3XTtIx@*XrxBa%L-A&6eLBl5Ov;UoG!4+aRxP>7muJAw!Je$4x$?9A=`9(!u3T0BH43;R>6ao13OjQT!Ds$B8#2sU~BNq+?4ZZ(Vaz(`7%>!q4WGF&Zk)DeFcPDPJ<WwN?XWBlsJQnCqAz<01+(?%RiIIWzMJOtO?1aD6%>tZQZrB%G%*G<EGPR?KEj3K0{y#P|G~$%IQmv15^vyBt(|XVg?a4^@e}X&O^A6`KC{X#J6COGSUIJ%uRD5`i#=Z+$F^63=j<HC#Q2kTUK*4^hRm>fAK_~;v9D3f&#<;;LWFY`rOo<;Wx200mVsB)$ISYm>O-WTEV`%Y`n~VIVfU6@lYgmD9q_13j_cmaBm&7^)t4|opyVg@gt{GOwdly8iV|F`69wqbHI)}SkX%oN!+p~9y*K+ZisWNGv|0a#6`>!(=5&sH4vn5;UVL33qz8N2ocMJ?-DOgPW2?PdKg`XW<tkCH~g(QRa)w?>E+4B8y<OC4MA4#i@`bJr(jAyl<y;m+17kK(_pCK;Up|KR;Ng!AN!zSgTsiKXiy`P>Co%gz$s`pc)2M%f(uv0^BUn>6tjemP@C*AAmqi-tmx4}bOdbYs(+h<;@7;@NW&zu3}GC0DQGN8g<j0irwmm#Ycia)ngJXc<_nllbRM|WH?SbYg_papH5z>P@%|S8>TyM$qIP7J4N!6*Ng{BMgS9hQHx{LZY1&1UlrtBxv(kQdn1{6>?w}hk(Tj?#z+07Y(3#KiIL+LV;x&PW$ex-C9fjW>LQO#Fqr^qP<vATh?QkOa#S4ITDo_RdBaWANZ|SW*RA=54wIIO2*VgA07|^>C<j5G4p@^eLvJ&ycKO3gmNeqb!B0jbjc@q=)Gd$AhH;0SddP(!srG`UwlYa0J;!!r$6C5I$XrEyyl^MB@^u9b$5Ss(yHTeSIity^mjea<UEw52zsvM)zgcFii{FwW6`4PMKkFJpb`Te5ns<+9fLQGP!+aOBMm1Xa(QSRHjogK}^ML;oR&g=$aB^%j8cNOGT;Cpi@T~f2`<N(L_42?5!h>6@Qp%&jx=Kpv~fwX%I$YRzk0}%}ClLZ|%>Hyg=PF@bDU^if^2f7AwLd1csg=0#sc>$|zY-NSh=*uWXgct)efsSKjnM5|B@A$7Abt6IZyfy*B-Nnu#8rA_c3VCb+e59$tNz4YTG7ltYutvz_KvU2AaL91IIhjfbfA=t`T1BF7V}WVH+d-JZO<Yo9@jzu-^s5Cu?10}7KKTMQLNuUj)B-wD9ZQ1IkZDK-5_APt-Z*|&83XVfcU<Tc^wP*KP~DmbUi_0q-|6JSsw{>Em&F`jovkC{(s4)Wg69JcoiW_ODC8|cqRG5tOscX%E~?}3mO-hf!dA8>krya3C?krR;H+kd)_ntq1lo6?GLWz|!nLe?OthX5l^V}b2}|HvWq4!>>?k^P>p>46$S*22*n977Idqc6EIjOp)7YiXBBx_;Bsb5C@jx}3T=(h0i{wdXGOM6uk<GCb`gZ6>2kC)p+%GOU!0_GQloV}XPAHHiIWBr?0*9HlmX`$P@h6T%a3R*r19xa6dtgOLPpe`Y?!OPd6bxaME~yk{d^$jRRW<ea_95Z&NPa6xz&+r-1SuY19PxL$bYQmqe$MuNUpWA0^+T@-kfLs)KNsC*(vWB9l><r8H1f+I6e(0(Pr{S^@nrnT6P6z28`GhTBV+#MfjTV-Pty*9H;z0qB;^c4C7@&hHZ;}Oz1@{|nbr1TAn{Jp@$i_al1&Fds|yQD)kUb)7ZW5C-+B-eUA8l`+VPfz3)vmVLYy3>c9x>SdJN@?Es>0{D(x`KMGA3o*}$i!whXuibL?(nFD+`Ru~h;#+?0rP?6D2qQ13Cd12&Wuwb(2!D%D`qnjQ6U;|hY<VI`}vpaies&UNbAU>!wAnz8X!yrE=x2F~x%0DmO<--@&kkkHGO3h}MJ-8i{7YoRc=$=<|(YG1{Trw60j5aFRpurtV&PF|k1)7Cf1FSxXW^^9c*cEO2uqp@Vw8<U)q)Z5UuKkYG`-nH3Y*5~-}wK0xPJ*Ex4j7G_sb;U$I!z`fg`|&yqnn_M#j5=vmVMCef{n-_+m?vi8d%Ts6Fo4YRbypZ#h-;gLmNjStE*>WdLHoM6ys{pSiHny7g$^z@t5>3e;t$|`w<W^q))0cY3Gg$>+HMIWjO4~U_}?DaQeZuYs?;6Bf@7mklj_D$TME=xO(8Z0&0{Lo4dk}9;slnG-Gktmr3&h`UC?$$5Xz99+?Fd18_4JssJzYQA@}!=kwkT}*gOH>;{_wBi0&uX)+(u{b;Marvf-j0ACBfRYJN?Z)q4Tzj!R|X5Msxc-PJR6^s0%A9A`G-nS&0Yw^c};NN^vJ%{^!6(fuZHqf!E_L)5c`8^!V-jqBtdHYxApeJi<fJSXRd#bB=o!|UAyh%!c@N>yTKcqxU@8y4)WJ>#t339@n+DtPO$g=a%K^vP$b;Y{MAkejL$<4|jJtf48>cW%O!`&VS%z$Tj=p|r53O+JeTpc6}FB@6_KnkKtO7IAR_I*v#AHj*@cdv^_n@9sdgh`By3?_s{ns9GES9GT<OeJ9bXPpg^UNLW^Z8eePZ%vLAcjpY<{(jPKvP|dFnS_`tLd}Sd*>#EY7d+TYj$QiiHNQiZahr(ruUkEzMb_W_oP)X&Jb~vWzcoPZ7K_4I^RPqZlL#Zp+EtjiihIHej<Z4XUzwLz<Jm$IX>vf=%ii(?T@~VHq$g^-Vr8gR**HD$zB#lZ+pSSTPRHAgKeQE7LS8T`_xfsR4QiU$Ygeutur|nGy_bdsFx>mWm)(q!lFh)q`F*u&+dF+z8J3U9lv;h{u@v6G)kvYt|VTKr#CpDZUh<iv*mrR?y3JFGDf+QW<zFO@KpjU9AG9wcdh0JZFR{;B5#ApsDH_${CSRJYh5%hpUAteMcb8JS8FPuo`ti@~r-li4W6Iopz_rGjtI^QiV8CPS!!jdH{w{ypeoTbT_pisXwFfXO-{sv_=TDYrvT1HKxGTQQU3c3c_P7@$<`5}`YWE$f`L|J%}?&^pFYMocpL{O-u$to4F%8Yu#Qu|1w7`dndq)PGHOK#R)e)@7d4`n6AT;n`mO}DVFCoh5g<jAI-`BKjGf>tB|UM?=9Vo3#RZ10YfugE1MX8L$%-7qnMrfmxV-eVm<OOh&hR(*Y({-&kzT&3{jJ+Sm-@u{Oniu2(zT<9M@e`I<C9{%IuKLOm4UrG')))
_V10_EXECUTOR=make_agent({0:_V10_TAPE},dead_stock=False)
def v10_replay_agent(obs,configuration=None):
    return _V10_EXECUTOR(obs,configuration)
v10_replay_agent.telemetry=_V10_EXECUTOR.chassis.diagnostics
agent=v10_replay_agent
