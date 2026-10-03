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
_V10_TAPE=json.loads(zlib.decompress(base64.b85decode('c%1Eh+m0khlHI@bb3Jr*H_2|jaXGy+#P+ZUyezRA6b1um1p&h9VWc-<|6OENWoCrixtV)pRdGf@158HcCBod?+%CtC{rUgC`tN`J+kgD~-(LNfKfn6Z*FXI5>h9*%|M=_w`fvaHmkYnV{Exr>?SKCJ|M}(hpI`mcPyhCpKYjoCcRzje<ExujKmXz5*T4Mt?cL3vU;W|R??1juU;O$tKYaZ7yZv|Izq~tL{`$Lb|M>N%U;gmJA3lEk)2o}?ySx9q+1>iL-~7u@f7-s`@)&=9_4CIce!Tzj?>>M3;~(x{fe-xpQ{R62-CuqY!;e2b-tEIDt04CGdH>-bK7RUix%B4Yq40Cvo-SYH`OhD}|MA;T-~QK+-#>gd`_y(7c5?dW^Us?Pc=3Ju`kRkTdQepGB9imHPVEGUg@vE&b`ZrMKYsfBof5_Ed;W>d4{ybNTi5CQp+Qck=h{dIsMJOHk2?x!);C}O`eGDJmCYAI8OX!5MY$0``PiF42337Fx^NcD_CC&nK^qJRV1MaLy5E>$)s4aBq$JKaE!tDx{dkr$(V40jzx)34pN2j3@oQ{^*p1u_npE^-FQi*%KA^pU@_si8;peY^{N-1%F+OR{<;O0MT(#%%T^%We&;J%aie2vH6O*cgx7bdbPFg|iPI))jXHrjqNzTm7S(#FMm2aDqGF6-MW~Vd53uRo)ngMH4KOcR?oba|b+V8B(_W9>uKfd2bk79lJAz*surDP5e{$U``cVb)h&*r)f&gV`wJ{RrsY7;mthnS6-y>Zb3U{2Md=h_-PQD<K@B%scd2ajs+eHN`B*8MQskiEI-sd;DY@!_S;S7XpobzzcPn_^0rnMtopJG+oQf2Asuz4G{tN8KM?@A8W`(kL8sKjW|KRWuv(Y1UKS1QJ-dfY(|>b-O4qxQ?jK&gSLDF8*h4<r0s<N(|iD51)Uk=U%dQ!;d|FVftfd<$k<`UF`ZVeDu=~!P~i*rjuK9xi54(?$N*b{OQxjZ+`sC=9ucG12?hfL&9(PfydysSl9Jq7$tOeIY;hm`$Yh*B~5R<i;`XBjEzoCy-MWo@llV{D$~k3cxUkEarWZQCG7TZIA@Ej$`SeCOeOoBx!A5H&8k^Yu;C#<Vtnz4I4|-JXe3zoz7jU>>?^r2)}D`nLZp;h5xZ&%GMI_gxg5h$+7$lu8-B+;!QoHjvryH+gRFG#KG<Fa_o(D2tP#&dys^tYp*-a`j?n_Gru%&)c3>vyv2eJ_Vm}0*si3!a08S%tX(oz(2hDJ1#mo8x4qEffeH$ne|1`;<nZu_f?jN@^I&l1wX1Ddu+|ygTOmDC{J|;Xi_kMAU{b|`)5n!jfIbxnP`9jOatKm5)@Xt(E$5-OYK@IQry*C(Vn>M9g;F7ypuU4VttG2=FL~jv{mc1Rs-rCw#_@|`k<0n3RxVu3Yn;OK!iRiwIpsOb@VFt5z<4%SSBp~;N8mE5Mr1>!Z?uLVP!r1+$yvY1%_#-OP=7o(`&gER>{{83AKYVOwK}=|KQ*SuFJ17xg*e_nJxs%8dQE}JqpVf!6(>FM%H(|wL^#0bCv4$u^$jk-UmfM)MD0kbhU7l|iNVO|WwXDhQ=`8x`v^y`v_Fl7GY}Xco+5(VHC%jL!UW%fw*|-6oMUzl10WF%8Tt^On`1<>Q<&`@i3cq#FxAsuM{^m0guvzw?RGFKRlZUjGArXSFLp0LSVWnoQTV5){frP%uZ%3*eGFs!SgYM%Z@XeiUSK(X;-(I|ghUcpX-H)hn*Cjcp&j$Uz+@5!FzZCa|<Gb~u_~!n=ZrJ^G`^3-j7^pgNR>iY!)E7Y|?Fn!BBGR+U)E7tJ@>&`B0=g<ME=A;HwYzb{wLUQ1)J=)KU=a3X0v>Ffjmq2Y8I2@WJ9rX^o(61_AC@Hl=EZF>ZB}hArA`-BbP~j-cxUVI%?BrqA=@|onjZ4uFu<|5!z!5XZ(u`!b4czMT~=|scinx#jNC~@F&1RYOcc>8P1(EW0p1PQnn2E-YH(Oh+~(iM4hQ?30O&(|6Uf0EsY@f?l%h{y0X{V_fw#%KgsN6-{c#vO&SM<jVJYA2g6SWA{Qm2o|LNoR-~Ste*s5qtsYh07(&k;Bb68`5<j*#RrjX7C`=9~^R_>!^&h*At_d5lY9A5Bqi8N1P&*o|G&Ox4QG)=<>Apb9Rk9DLouM%#xsUj@5D!He)7G#BBN&vLUfS}3;BwwX!4{i+Vg)VxW@9d&n(Jdyb-H23@y{f|MM#RU%4x;hSRAzxe5QK|Es<%L2a#aqkQvygKR;Ze*i}shM-R4dh&)w-@eB-*8G)Dst_f@I^ri&%<?16&@Y)+7bRhc3taREN59hvC;9qcpKt8?0<laKlW-p<=d;K&gkAwSt&;Qja}xC?v6t*2p{@VDj63<{(dQZoz{)_K;QNrCn9Bl9xR1M`DNK7$PjpEykumcnBl2%l2CCxkOa2_Td;pKX&!!k~VjUr|{uL3B)ptpPj&zNk&CH4q9}CaQXyGDTA|_){4u5H9MK-Y1(F?G6l228=p3$m5zcp1>QPWF3H)3G@-@$rv`y>@<bP^*c=fHn#*eXjjQ3#O#y6e=JqfYF8BPtT!qj7dT362`DuTC+JC6scvePbGu0r4_}ZcATdF{L`e$=O91U&)EwP>H%0HMrclp-1WG&RkQvJ7?s#F9;PI{L>o$;dKth)X2Y{fex`#dZWZSG=X4HLb(hKMP>eaXPh&ttyKBDM!(M$^6m208>as?|b-{f|~f>4XDCtHCao!6+tfxsSQ-tgJB@bs+3g!b;lp>EK71^WAkBx5~6=C&EQbN!e>cZoy&r2g#8%{Ro(c{#@XmPvb2f`(^#Dp5cNTd8_dOIWhSjnLquxJt&Y7^b8NW^`-br<-%y5Gj$ay}987Wvx4a)L<bMgOkSiDoWzUIZ+e>PPSnm{0KSsg6kII@n9#3bCuNZfp6|~6@t@NCX+Kj+g03)1K*qgO0X(bO498CA^YM)E@5HA<l6{5WQDe~ow2MJE&Xm49Ip4~C3l``%KZ=3%x4(9;2P+<#-MGX9IGMX<;FK{5Ps4JE30+R?ABOgsKwg{c`l>&M4=n%en1)yQ(rZt3x%pNR4Xz2b>AFBU<FD5@X-Rfm`RCoT|B?)sW*2plM)kOHT0>nL@mKz^UVzmZADG-=!U?ivZ&w%oblkz-Rf+`mVu(6NRLbh7%x|Zmu(g&d29T^l`h=A&*&#rule$PU7dK!N2$3@xi0&>=L>%l1~2~2JxFyKe(MinU;O_ExyFNt#$fT{1wIIX8CeKHD|c>R9FRqSw>Pe}V9`V>e*XMvb2xwc`n!9hM-OYp+N^wIhz+?JZb8#j9#SaLLfXO-0Msw!O4<qej)9t{iwgn3RXt<np<q~rx}no-rS4WC>f^o0dnFma;jB5x{z}^DUTt8Ev3CwymD%_vvGaJz5Hyp#rvemP4bz8?$;$-4r9dzht%-teMmdg^u{ErNtKIvu@1VL8(al)4x<+4lY{RZ`6Uzxj+D>%cQ646{f$9<zqG_bZNhic7-G`@(HVQtC!E3y~DKe5uJdf8u{{HuFk0uB8{nvmLD1&3gDD-L(stp7otvgGJQb&;KMmY)oMM2a;NfXZSll3On-Wmv6E85^i6Wf3rmiasPV%`DzcN|w8`PW`lB)R)*xcXVBloeDCv-~M^qoegG(yBs&=TKk^&JVr20P?sW)DF++O^kWBDp@%>!4U<Vgrhe2S5(1pRQRD@ItxK5brJ7QGqbvcu$2SX9ZC#ifgz-8b1%#4%l`a{8!?kpP5DqAWHzXkq1}#H`P4ZNns_<}fbC_eokP<tJGEus9o6J4fL1O(lq&;MrCh5smOzVyCo1Fsf?Wqv91>NNIPB$wko3s&dCGgCf0Pn)q#2!w>5wy7a;5@*XJUi;RAf#-#PS+R_nL%V4JxHle%rae(Sec0fIQ)sodiIgnAs0YgbH+|bSm6a`*#jq2QxBr<7kYQMRQJED!?{6;-?1M^?ZUTCzfQh1v><d$Fw0+Ql8=9724etn+H)5uhsx`Go&`MV>(F&aXYHL{<FuYU5fhP&gOA?K=)j}5=Jo`@J>aaZqQxQ2kzT-yFzD3Oz=r7TyKDcGD~y1Rep*$>qXpR(kdJH+j_~w*p#q%RMi)X9z5DiC&i?{h0{G5S4zKF=5WcgoH!ZY@{2ooDuj`5HJ+6a?0hAtE-W&FY!3nM0)pewq*2H>cg9b-a*C}8v}&Iqp-EOXW6JSQ3iunrG3jY%*Yj=T^J^~X>cn5LN}M{mC^_z(IJPgTK3}h9)zVjp`2dR?HMO6141c!w{O;K}ySS}Pp&lz}u;!D+gNf<@3NpIcag+AMN3N{vH5x@d4(RPpg7Z@q3H_lhearF&27K)EzPRYnqgBl*?WV>uiv!OkX(5x;R!c~xc81hVKvu(+5LqnlXM^O(R+msqdWitBE?DYIU|2HG3ymGP1?@m4i5S?@0nUR!wer%;wrxypSwIEb?u-Rlh9C>cFpOCp4<(!gd>`bg8zC+GcSLebl_ri@iOat=Huc(Zv`vTych;HHHl7nuJxhl9@b0E3Y}J&rwSaj=3`By^>N%yLT-A;gDoh{zO%S#{rwkh4Vgd9AwxYi1xK=Mz1QYpGnuR>FQ(!%-`gZqM-!>3i{DjMOE{_@<Rheh&r@8^95nA&aJhxA-z9Y}OP0dkOy@fM5_9yj#h-?GZmKF&Jk4Jc81a6$<`Qx{r{zav)05A;X5Xhtx8O~D4B@Cqxw++L~R<{H4OAU36TbW*i$issSu&2vK0|yt$78lL>-3*+Bk`jbJ(x_#E;8Zn|G+Ck_wd6IqQ!-oSHMn+m8+ji8;m5dMfAEkpiy6D*F^~y8Rx{aJKRl-)EJa#YFK-%9GLb3Th3vq@5YqcI_~F4GX`4b25LTftv04<{#g%IF$A`{Ct2@Awfue_od$bQy{P-XESqV<uaQnQ25`+MYhW#m!Lojf=B10Z-i3+=?JNwn%s{%+Nf&-cR{AB~>?lM9a+6f@QFC9TQu}=9$D2dD*ln<mKv-;M3R<ntYsEHAk2tydNzBX<3qS1>cQLYsFOQS?yd6&DW7In&dEdD7CvRSu@3BIL`7C!Fyb=Huhb~|-^MX#b=hpx+tg{gQ#$?<^>s!<8;3{dw)huV|@(uj__uGEvsJoccYD8Z<zomIBq<)pLF$5z)-W`p?AmEynhaUf`4028gkjgCXq)g8l%XWNXMGfe@xx1Pem1v4!UJ#_g%I*Za+ci9?14r2eX&rgd0bTj9J>ZC@8XGF+Dle9v&?;lLvDz#})Nf-h5SG;*M)73$%<$EtWG);3f|6m{wX|e?%>2iT`S9Eum=qP@aa!97MMdgUPDtFQ8pnjk+$%ZV#bWTce1n0XXk^I9Q@`~toWh|P*bQ*3!j|Um~OQNuZ4|tLi64a59-|geo(SFVPft=Z1R;3T{h79ZgX}O)&g**mvW*YX7KFdUw($@YIS%lq|XdsKi^1}Iet8?AlfK{Zwt6J-JK6B(z!39_e28OetBBwaBqcTP6p$vW6>U3I+R2d1X-pC3Fy_b20LByb(4}hj@+weV7_(P%zZ*?xboAL)=HTp&nbd6Rpg*tca2V*B-HsK-zt(Mx>*5ge?ZdQ2UobG4D?sU9{@b18&c5NoAd!v<<-wCBY(Ipxcv1)1#?_f+0o?e7L^^kz=Rtp4XqT5IyS_E{lnpT+)2Q%qJpQv8YyfB6L?|buT;$&g&JYPtFE#?l?lotxlV}=tG8ykxP40RP`%HXs`s48#}baMG%54K1b=)=lRq}oxSn7(0wV`~1SS<1v^mbLhPT+=%I5Xc^#ejtaXLJq)acDcVqq|_WLwL!;7qw&B1y9^+1A*HuJ!L40TAUC#mM#F~=19YY#v)}|J=>J;AlJuqG3J)l1bxuU7->7!A?f<0i&T5qc<fNG>s0$Sxpn!=(6=aZB3?FROriPUUDv!E%R3Nm&UKR&m&s`oDc}{72M?UxN8hv)P|3nqje4^+$y{#TSc5;WB^i%_g3eO~iW*F_p4^7yo#<va71(0v3hHSTRxHFp#YKE4YGx7BIF|8#A-BmWD1~Z<uLRAYROONCC@*DrSiya&HM*gaW65wA4WE>`MtyrHTdvn=JUB;gzY05giS$a8V>8{lfAQTSu+?sQg{VY=F!b=FYDac>q(FkChTC=2Q{xZ4}4xUzIik3&kc({9q!Du5WttB~1e9%Yb5!ow>yO|_CheGkEG<4YG>UCLa>F^{x!~X}kNZ?68{|~E?3;U$UoGK}9pxANNIpel@_i*VgewSH{9wbA#-Df@9e&F(FC*Zb|QvFZU27r(77^_k1j1j09pN?B;guCptrmy+Q#{cxtHFyIK5gcd_Kl&B;bkf=$Iq+zgg14!R)R5;_@?(XV!aQF4aq1P)F6UwORX@EjK^R{d!+H0XRZdwXmnvDe9LKQiimH!aU=XT!X=t`gn96PHq1;0rk_9d__3DP&cXcV1cdfomt`ImJ{Ez~VC%T2%EO^+QH-^n_0|!#!E@5sP9o%DC;86~{W;85q@Xb=%ObfY+6Jlb0?g{f92|5paM30TmD?^3dZl4+&Y=tfGzmIY)c{<iPEgVa2qa-C&zkk?)EGqhm+aWX#`|;b^Zpr6Q0VJ(tbqF?wYJk~^d)pCXSv^Hal?11f=s&KXWVMEwB<%K#lp({enqYKtf13J&TE?IypI!KZeQZTZ=`pVYOUy7(I05E6R5414)V>WUK}$l#L4@5CUt!Vhm8(XS8L~~%vDwFLG|s9MzYx2o2YMhTr-cDW2S118A5j_kb*Huj_9lwO;M752@M;`;`I>3zW}TmARMag9X{G0?qUO%_2hkXyyOZ&mFq`8Vtg0}$#5xSqNTBEY6qKhT>r<(8r^Z0`RnDubiyRv6&l9nNzzuVN7Rw7-!=kOax62$75vFaXi*yam1lt>YdTVNV@;N;71zlYYR-pyW`)9BY&!{KcfQ|Ev2)5>6p_Y~`OFf@1XvdaMV9P_S4{#@7_v33WRji{$psc(%E?BXktDJ(zkqX}ACF)LD8eXh4{R--@lEx+R`zU7Z2JiT-K;oH}Y$fwK6kpuISHle`I-4r!COpY11$}CWCF~85tag(@LMURttF}!Z2!Ksuc;@%J!vW^ILdIJRRs~Qej-fEANX}De8&l(s!d5mEb-=wBce*yWL??S}G5Hi`-f#2m;E-T-_(Pd>L*d}ac}PRj!4Zlw`khd-`a~dWq~JvIU|yvRVQ%>pnN>tv#Oq@<1}b9J6?xhIaTX(thC+-7P*GBt@1kcKgFljwC6ha=+@^C;0(<kbveL<J)8uLPFxxSpPBF&v8$iUg#m`r)k`e7aGQU;4A-Wp^)j?6dJQyeOy#?+ZKT4BC-K76j{XCRbVm$$wW;!BC0aCg3+=B><o0#L!mrk-w3TpxKP5ZK2E#*r{(R5n{df@&+r&`!T7LlCsl4G98fdwEgV|J?5&u22lye}PRKi7)ATd)O(7<p}lhk30Bsa_Hmz0q-Y+G6-tnii#_fD;WVdY&#B-gq(F9s(%{jdu-|OVz6C)%6vdA2|N(pDI+byGgFkd1u4aIjzn0Pz+738S$}(RWqTkp7zLXS2@>ej(Y20L7<2PLy%KWQcO&TW~_w5C4)gbJjiyLX;FKECG28dU53Bin<w-0$(E~taDnm5oPlJRQ8IxAN2U>>F)VA%uyiEXOWC=hb}g&I8`B_XoSz6&lTs=i&<&O_1rhoKQj4Wpmpr^4lZs7il*<C*L;4v{gTOsCRjHGis%c^?knv0=KuveMp^f_shnC=%J@Y_5`qLv<Gaxk;t^GrP?XgFf3%%H)^bEv3=NwL56iKUDk|68?V#TJKHY`sI^qmrDqRqY^+xr8xQ3z@uWy*NNr0GfTo?evPY+mJ(A$<IjDCvmk-z`M#mIue3v)d`i!i)8IuOM^`ydhY`2;AT03xNo%aQ}XZR(|gZ@unW0H+5J6Q`W=GsdZI9criMtK+cdXqH&v^_WifwCshH}q>$AFAL_TTBvQ6sjr0od)o&D1KrO3guF`UMf-|eY*|P&e6WLq_8~Ud%mY{5qNS0Bj8AwlWq9vF`Va5sJ0b|$(Kwo4E#GO<w>_&=~8Y^<zNXkDz#)W_a4x^;HPCODLNduImwqXLy-2qT15b5tqpmov6PEWhhSa~ekMd(dUohS^JvgF)e(GA`P4MUeGso;RV3Y|qn_8jCQyF^$9+JRV7UMmr$E5de<B<3RS)D$g&YH-7C8C%N_iV`CIC>3cy^=`)0?#?*Ie!&F;h8osp(@FDzvfvqsib2qA=Y^g(f<Wr-<~_EXho~3fMi!t+5=9Zgwy(QAmo%{p0R2VMjgu&ujibCBa@dM*Gh`Fa;oiP43!}hz7OEiFF(HD^4<kxcf2}StQ>dvOT4Umi4XiNrN`!ohs%hW|i*X^9z?_q;9ga}oLPjwoUy;{E`rz|#whdx%<K-%DF^<4`kJe*Q{Glk!Tfi4<?(p;i3f(P-+AwBsVWI_4y1tiJU72)_N0xAzQ~jp68bj<AMORdqGlLf;^cL5NMNjB}P(8$sfG9891ZeUMBeSw_R)Q^yTA6F|Pq2qbYq9@7fc_29I+CmzaF00nDiAd??5N{H_97)Np;tp|8YK7Q;r$cHdfe%h_n2@keq>Se215x<({V-B6I%BgI^$17z|zFm5Ii_C>*<(b8TmnyEd{3*V>V1xR*=BD4o%vQ;~OVx-g;{a`ianCAXf2C&PFLY-hh-Zv{}UuW(#2AMMbq$pvm*V&<%&dUiJgU<Sw@G{3nm-*EtG5S#Nh!Xp_ma5O#S8yaW{0IX^VJ7R2V0ZZFCftM+>vW`m<`oRd2(SBdPK#yEHqMMynuQBhcdU4REzCM9WC(zg~vpGICE!dn>9mgy64chc$O^UR-oEG**sQ;?q*7C~9dpky}5rR^fVuj}xxUIKJ@$shnh0L%N+-cfOP;S+l%3RRM~q>O9JN(KpxhW;+hn+N-}k;Q3sio))sAzHk_r5nw8ADXuhf!4`}o6_Pz-vVQZtXhK!*k{NEXEm_VWup$`$woZQsYljoqIy#muSV+L16KpCJU<WaYJ2;dOEzovxU24B0!8AT9u?04wrlmF1FG%zE-rN~nMh{iK{y+V?mMdAlr$ux?v2#fLt(Z;9m_AyAOt9*Y?2rtszYikHPU2<HMjzKy{7eL-Og#Zc64I9ps<)2BaD<IfT8Jat(qrn9ZJaVdK`#S`HaDC5qd&L6W?l2yuuc;QxjrJRJXS1isQC$Fh<iY!ORCoTurbqwz2)Asa>_dU6D3OTuPTwWU3cPjPeQr;h+-g_s10d1vddodPt?G87sT3Dm=4YE&*6WvMx-d@ElTQ9HqJ@aeLi@4g^5ng^^-(;FUvMoJG!pN={mR2w@D$G<z*EZ(3$99x5Jb4j>LZOj${Y&K_N0pWtR%+5O;B7GO?y#%@)+iO|V2xIUoN6v7>jx9hBeSr~A>0fw<s@=u|x<Y=k@Y}f#X8s@iOqcN(>4g(OKtA83iAJf@p162p=syN8R5C@Qgj*mVNMi@|IvJAth)FQrFNYtsCVXcOm!l>F`^~8ZrtH2Q!qLkh<iskyPB?gnj#p^@{*w@Zp^Gp{q4b!JyHmW*tgr|YSTV>tqcoLEUaaZVqcmYV?R6n9dDkPLHOnR3BNuI??3+Ind>zD;H0(-=fA#n?1%UvIB*NbuOX|nzFXj6;b0M2en-3vydO**wom6g{9zyUtf`V%mEa&7E<AR`&)@tC++*xzD}JSZtF6~-y18;WDA;UIDLrj*PDBq}LSW_T1T&u$U?Jr!q7A;+v7Q!AJ@nL=#jV9qx_2o>XgPA6QIrPhAnG@}|ffB-LXP!B%p<qE`^i|oe!{mL;psB0f3hql~OrQxtq^X@@YL9trDDS@m>9fpnh`~XhUncxTo-TRt=!nZA|aE_C4gQJTbg8eRW7Wf2t`+5%r+OEdEnx-w+JF19~;84?<%(C?TW*|pk;gVuoG<bBTH5uSF4kwumdIG5K_t}*%Xt@3HMzNEg{@V;DmaUz7_{szjbyDKoO2897ZrTEw%6n-@WDzPA$)1UrfxRWlJ)eU$$4#A%>lx*Qs?(PQqlWCYq}b<KgUF5%c3ovD?nZyI7JE}CiYF5-Do}L^C;e#Co42M-6QzPl+u+!lMqBGC2NIls!GIHDdk{~ed!`)IsGl*(cfI-Q#A{q&=vvk<SyabFO&bm(8L(1Lj~Lhi-FD2}oI5@G)ERkWMO?IE7o}qv6&5c=2ah98)L6Lf9&auDQtkrnRJ(A^9-`C&$zZm>Kr$p_ACyESO$&Pa*6}>hd%O(XFmIeL+cYovtoO#PghlK4Y=1(>90FhV+7-_*Xv8f7C~ev+&gB85c~?-uB$a;vRHm<hU|*XV?6wbTFH+CTcC@T9tMiN7=SVOhBaDy%K(PnE{}AsTOH(>dPbkuA7#Ipbj?2((Xk!xkA3(0qA(gf30%B3`#t_c2^L$#)zX|I6+9-a8P*^(~)iSH~n5l2~^!EkG6{v1nP`rMTyN;%qU|IiiZ?evRu1k2?Q1m@DGTFby^@wLpC#S%-_=sD|JV>~Iw=Hoqu}<;jU$z@MFJKAV)xDt%-(5~*?dUv66+jC_10&cG=UL*o=<vFJVrwrA!&8gp-j%sR?+3EJpgo~8<=YyHk`SORr5pxheqD@xc+-UBY?ErJnf|P`XFc9~)aT1iX+ix>_&JaH7+wSb)#}kI0G$=Y=`fwX{mKGrmc;cSXNiz793Dnq4eKF<2a#~&1G0U%Q$O5c4}kaEZ&L%q8jRckLa^1Ottv)cl=Q=i<-FKQC=rzKGIS4}gy)sH{Uv^g2GlhTr|`Jh<|U-L`a`N4Pw2HNP`Vp!6fXqx3sXu-%5+>;ep0JQMkI{yKMBu|(c#U3-c%@JS6PN6`MAiaNF|r_i+<cajn0D-TeeNcy_MOO^A5++^yb8KNjb%7y2{#ilmfqH(&RxR%!|%ghzj?RmH@^MLs?|H;RM31pl9J3(3AB`rnUIIy*mP(<t5g@U4BW*+qoW^j#gUKmO14hC)e)Y9WvZK@65Tj`D<}{tLHM`u_l3xF^xZP8Z->ryV8d=uoXDHfYb@N{a%Kpo(!|h`we{Vuev|F$6?syWMjsFI2fb4AD189YMmLu!d!vfbwGx=4}{ffHGPlQQ<U>$>P-eZbF^#ejMrqOZr6w>(?+ruP##4Bzoo$dlajL`v!Xuh@<-m|W>1XA79DW<4x_oyTI^v(bJJS1udx$wW{JFoy8f9e7s8CmXjvFV%h#FH0!~igz#t$DFP$H781#(Fcv2>pVB2SQsYPZFeDWE02F`C-q3_93b6(nqS17aOsya_4v5y<p(6u#^4Z3zmB+HQ?I|q^~<R^`+_RNt~jfR+2N(?0fJy#Tn)92VcgeGDV8P-bd2COEKJGX&Lu43IIcDCwTSI^3xHCZPh8`h3L+1L+#J8zd4oAw{7bbrUp_VW$=J34#H>l5k;T<*IgfD58Gs<Zj>5^yqQX1|v@wbzgpUahn&y*BW9YHfp#jb4RMa=W{zH$Vu<Wp8<~W6o^*Z?WE{O7OtNWI#?`g%2P3{rG6`$m}tc2x<dOXz8EXsX)sO867NeG`+r4nZ24RQfQjQS&Q?fs@((^zqsLu{0E{Z&`GV&9?sw`)B?62OnbKo8(uF3zLxheUK62oq8&v0UgL3^ODP350V|u%oYYAR`=^EOo!S>LG1%+N2%0b+wFDrGD|`$aS*;7Zgc<Xf)C8dJ&H|sG$1)+vMm>n2(*ozEmEJz0j1yTrWVDmP6?K8qYRzquh0`{vo`_@DsWDa!<zopTmY$=9)mE`8o9zsJ0?`smq>|_lpRdLTY2on#+suze)79T&!FM6J4hLE=^WR7}i17^QNSWTBw*X>oh>^!6dORot${ws)1ND-eqc<obb<SJe@<Px%fwE0}0u$?!T>m8IrHSgzN<U54A0jqoY#yrD+w;{}@(-LdR>oKf*|(OkiiFZ=eqj|8bbEo4VpB2?7W_~j7|u4QLh#o&Un};1_l(}!xe1s`KGy+Ayj9&{vl9}{MO`sC)MXU54uT9?4E^MDiGnC$4A5eY4HAt9_0e*j_M3l#wZ6-uot<W&!`c{#!I==83a*)W4a_NP52b{_Bv~@t{e|&({$jv^)ZNg9!Jz|bvYHGAyTJD;F>$}P@&?799&h9jo>=oB@z^+RLm0zR5L-#amnP<fSrFNY4NUN!wQe39QoSfJ!W>{%lSU;=HlA66YmkVqUQ!H->!ryWBmKRUCP9*tw*p7C%GxQIM4q~;$+hh6YE9OfP#hR}mq%G&!K{x^gqs`dl*Z|odQ)+*8ZDR6i1OYbZ6dp+rj+um`$KYy5g72$f;`3S6zp!#LLY^eA>Vmxt!~Lswb2ASs-2}|02bB(ke5<Nd#7lWbZ<gfQOMZ0Ir9%!hutQ*6G?)Z`Jd9ksl{gl3IwWm6+|qujO7wYqE5Ry9eA6L0YL{K_SWZnq*fXic*TwPKG}XjwqX;3Y&CHpQd#RP2t7U4(iOX2*{$7)qewDIp&K0mGhFvwt!gx`Tp8tBHgArjoAe9RSqp-6+E4R$yeLV<UCI#y5O_}vKDdCzeKPwR`+pHzLN;}ilD7jPAHt~D)jpQa?DY7My2V=Y7plzfzWx0Z?ovD~TFMEA4(N$t>#Tlw=;#1L_gqG8LR?YTYHW<uC~Z$^eI;uYOY7>rC!Nf!gcJay<~Tz~^LKdECdK(Y@~tICxUE4MK;nyJ*<g`dI8ox4Azgw?U`Eg#*l=a`27+Tmrp0{>74dT!3)tMK0SJiaT^Maj3xBx8eb>;FOI(y7CC*EdIQY5U*KhKDskXyFtcyW7n_mt57>TpjCGGk2udb|976V8E=%bvzs+!NHN+n4;ba6WOwIpo0w9#g~e$#1X(Z-tzmj7e{sTVmvCKFi?3>Ya0hD38p4UhrnG`T0t#99saA{@<*eQ3|=AoL!t{n(lSldj_&>~)*;l91AX$-Y=A*mN8(ppM$2MR<zQmw4Jzb?R&QFQGk1-0@t6{Rv^^zCR-xi9=YOLRlabXL#2n*{1t*uh%~-$z$-!+7*fi(N8x?gBh{V^&4TjH?o9{lN~NQmBOqUe2C2f*fmj{cI(I;+ykP+u7>9P=c1T1seiVvOcsMBll6L_@Exp51(l^q?6ew~S3^r%X5%{VFKK36bRAwbxnlDn+VVpHqY0^GN3;xIs!34nqH5NX;$ghX?ueGU<{ma<EEF6Zon2t%r2+Me+uafYyc=3PhFdJFC|f}Ed=PnbPP9I4W$?$3pFV%LSBJ+-Nrw||Hk&+MV5?WNzeb%hVIuacwsef^U0vq+4`yDr1}9cQg2J=$>#~;7E6CckD?AMoU`extEzr)#RnQbWDjql)VWsDN75NwS(sRt;j2A#+kSkM$V=Q)TyU{?&2P4e*NEk%@wo2Y?iIN{rt#x9CX6E?HI8a%i^ZE=CmObv7Fh3|UvAV+HmolTRC@?L=gQoV-nL2tKx5B=Jho)lPdFH}Sxm0`+1IS6oQV&J4n{5uKmVr)bot?UVm_A7pb5hDaz`o!`0!E2Y(TtaWQNZs%BcUgq0md)Uq->W;+T))dZ)Lv>S?+}u1(GfBCJ?wR&H<DE&>HrREkQ4n14;(yq;qE`3h=T#V?%PrFA0SCC^<XJ*ZFD{h|`)gT0XtZ5SUCED)Lzo>q0Gay%qKGE+3|bzKkZ+ynPb3pk8wd@cT4PKzdFQAyP71gU7tUw=c)mvE8g+?u?Y^HJdDlLc!nC<(_CVPj>rA`FhtLJ%tpW*Eu%bLEFlktZ#Bjtz{FAY69pt2h7Ns<jNg94&)JK2SH8<G{f<;BF>pfYHc#f))#b=3V{8jHWWJAW4FffHpr|hu)}P233TC0c6a+Ha4YmcXw4}GjwKlz=9*(Q^K?i5wVV}n`i?i&Gr{xBFKn@08k`$qME7zH2+pI)?qJj<5g+b+MXX_Vp2i^TTfRV9o*i(q6>%dol1(JORtxu3Ys$pHT<#H;3Zu#pn6a1jMc9OhaYPey(^k;XGiz}->FuekBTOFB=4M4}u`r#BB?qR2H#6hBnbl3+JnetS*@7EgRbmS|rkkH#wReffebQ^n$0PKd^C@~DJ?DByCg;A3wOp-rfa%2WQNfZ(OL{-u%xDS5%hvEc^kAY!&;UD5#KOd$v~$G;6e{n)xeu*TNuI;*E{=k^uW>xw=R<WP28^2Ie|ml#Wuaun^|BCpEv_1yDua*B3GH)kxj~(2ELT~Hl8H>th<$l$dQ$9If7%q8AT%Q_qFkv3I&2GT9iWaBEbhy7+Ng=Ys<Kz&*=f4j?wHK58G4F}mJR`FVPYguE-(g`h%7lnS0Yxt>)C~;Xto11%1AvOw^;v`;0-^@`F<G^u4P(wRGoJG$rePZKk_Qo;1{f^<x;U0K(wlPU!Hg76<#u7n;GbH*>8Iq2v~z{9T9yfk{erf0}e-v7~$FUmAVrFWnsk_x|*(P%mgjz=f6!@UM$ff^QVW~9?lT{l7<&Af-}%arQ$cu(}5Q%`Ek6d7sbLLVhA&B@+`J4cLC~2UmoR4zClT%HpezPot`RPtlv!E&&!5UH;(INHxqvk;PhUaiOij`9{P6;kD-eHQnz+yBV$bf#bB*WLO<}Aw`$Xr3ml~qA!fZ+@e;^8R>x&{Wxt{^ld%&ofXA(=-xB@0TFvISP-&}KKG?827K}@aJIv{^*Q*Zsm5cVr3A?qH)}@!do}kfQu*hvTkOFFjSwc3oE?K{+V$kF`<;u8Sn9c)xS<MpYsdMZkU?K83!A!Ti8QR0GRCehYnj8)c+FGc*s~ly*Mla^7kfW!Ga2pM!hUx}3<jGktX_IMwD)gti*z+$O%)s9u71MKgSpG0YaC1$cCOJ6|Ne+_QScBu+uqQ}2vfaAX-SZZW`Lx#9EQWH~aWxD|6#$r79bVg*!%c#0mAj-NC(D$RgSN3WB#UkJN*>ETDMWK-LYB_oJ~bDxq^bgW2$1OBE2S?o0HqHn7&G(0z@8qqko1$ya3IdaF5ZG`XcKTBLeiw#**_gyN|DO~+lyim#%H8Rh64|#&%e}lHC{>yC}0>jfgDWLg?XwIT=4$kAJBqB`F>iPUx2-yQe=goui3*i$i68&<2NqwsEKICCUd;*Z(y#(DgzD*<JyIcP1vojJT(eUT&u>>EROorUCE;Eyr&pc-LcOxQ3Ak2)ardL{LeUmNNy4r_4Jl|y;8pcZ$5dA-qJY3%#|M8&Bt|Lb&z*qnELguh%Vh7RLTd0sl|1)<=fe+Y<D8}URa$vK2(C*oHk$6U+$n;n*5Dt1wjby<jl({5(OTDWpR%D_3ho^UNwN3M{799wO2c5!Tw4T03=0(b8=9lhuy;}R|2zsET!^f{l*E@r=wYF$g@FK3QKx;Uxw<g6ROmt6wy_Sutge(ug{@yl)5ZbN{^uu>Gxo$Dv=y*GetDES-j9luBfqGrid+IZ>d)~kDYW()=ljL74aR`<UYehG$Ut;2J6JmqTqB9R7hcje1SGuQI|eoEAb1)t#KyfJg=>%3g8z@%U`Pl7K@<h%u}<p)>LGp8VwpO*s+#f?`F%6I{dZ^qBbq(VFjDtN?I|%OUH@{6MSe)SRSs|w?vFrRATV;y|L+?b1S0hCtBPvCtWb&o0lne=r4fa2$YJfo-?hlM`3!5t@y<!p}W-ZRTg5#b=Zr~km)%L0S|5`>Kx3XuXNU?%d??oowe&xeF-oeQyYB)w+u(U9a6tb1@<hNc;%%e<nO4zOnStUTjC!;-a@AVv3W8p5_pZM7j(s4d08U$Qig{mI3x3-KM3grU&<4hYUHLw%Tw9qS8TLulHy_T4dm{JjI$_7ItJve^j#6c>2bdR*Is}w1B-E%-O$%Px)%ya6p#K52fHKby%dR-OU2KdC`gxwf9k5VsXQ(<i_eTDk164h>3S?f-yKwPc7&@_z2rGZ`AX3_A=ngnKvic(lL#Y0E%cE$ql`OIKZ>dqt<p2dMd0|%3JjcBE0ej~by$!>_>u||Fr%MEjF*NNHWFYra-(Wl>4cr^HA+V<ARE_<^O76kM!3B<9C&>z+Z}Jg{$Y97_sxMx7MF3xB-No*<w_-}x^Oja7jnANu}2;e6}=u^t8FQ(xyp#G)m7uzA{^cdLMc-Xv{W25rX3T!8uRH3$@9Qn9u*Yyo;KPYfT>r`(Mli5Y4-aBaXs_E8j%Me{!$4wX17n`m$2{4Mu4?~L!n{4f=eS|c6w4!Yv<2fdcf-U<%21bErX)60PwI#V(v#Taz}@wE2LpltPGM5Q1wIC1yqwaOG@LARdcI}0xS#yPpO|r-?ZDc)?{-4a@V5*`V5ZNRx^Po=dEwq8S3K5I;V4s60c_HFWpJU%(15gJz%38QUgatSKkH_jP$F*Yv8r)_&#wm+UT(^k8Pl@t9A%#>saB3rvUp)hp$-fd*_Z97X><gUC(?sg;JUd9yM|eeGfJImT!UEFW4uh2w$lY*u8R+mlYTh%Wn-y;$bINTcxe1daG6|R?rC4+#hTjLA2YzolM=5#CBk&*unB9rh<N?)VnMxbUK#?i{%E#wh6V};n7K2@atLbwc6BU*~u{W1MpnUB6YYm){ngF2=id+R&6%y04fqGVJ38_S%dK5-m>KCZ>`AoO?b{cErqw8JRoVnYJspx)ne2o3fZh$PWGk34{Yk-5NvC4D159Y*_s26U#S!2Q45JU#fCQZDLjii>0bs_&Tp|eJ<ngxd#4W~HRm33S!tv*EQCcn<aDhqJ}?lp<U~&!;Ypa!>(VuA!dae(u^Y8nUIT^={>~-hBr&X56xy!U44%M=B+3mrbXVg_@1YIq>NSRe6_<M^t(mZR?bQzOpo1yWXRDVDm>g|It*z5GA{FoqCdc}KyUi=dlO^0-Fn1KoxnIzjEHZSfr!yo7#1j&2GvS~L=AAn@^{R_wZ2BCrW}}rE2+TmfaGr`mvfEt5%&92Os0&=L;E#4>F5nawn*<F|36(aXt8HMaHRD4%lvEsA@?1x@CN;c}n0!Z}AHrE6Dy`chHeohM37nR#Cl?{|5`&zKwcJg(4A~#0AUCbyX|K$I0$;HAzBU1qxj=hm$=|aZX;=5^ol8fnzjc?G!2v6f(fji@JA7#jMy5sVI(n6ei<zH3Y#So3c{E?f05qGzQ6#Jn+=j2PXQnD19kW5u-|1fpF>d1EyX4NtA~Miv4R;Hj#RR|B%BdgQyVG!9D*rPs?i+Nb0drw14hT=fsA;uJ`luyn*`roJk-)Kq=DhxKzzejbyka#{2{)wK86qb&yh1)XxcG)`h!na!;hP`52I;k=BNbQhs(&slHkK!_Cen!%wN_ctdvQCUWp}1QEe2hmb`Z#N>*54KWXNxk7XvRAB`w{@nVa4?M->i3BvuSp9~$m0nz5$z`4(P89y{-65t_M%$f(KQ2RQ%>E(cx|&+sfyr0qj@_oCUhdJVziuffIl;2K6_Oj+(KTRN|0r`2b|b?LSjPJ0EVv6?JFC{JmYjU|~wxhS#O@<inzsV_$LZ^>I)j`!okC$<+1BCh=keGJBVjqW$o3z;iF$6C)R={KNA^qx29&=3}l*BWjUv;GxYZL)2=RAV&Qi5}_U86Jp{DqbV*ES-dC#KrRm>z<X#*-*8uc4XhQZ^Wp7;Mt>2=o%;Cb5im)41>b;bI9{)r3R3H$#w=k>y~QM2DJr-keeF-DB+O60U${2$uUrq5KQ^O%Q5QAwWX$8r~w=tk`6e49uFIqfee|Xb3>aWjSc9)gL?xNSQh4I@{h?j5b$*j>NyQTAk{sP><Q<D?7vW(u&`svh_B5uKMVz^=h6ErWkiYk8e9uZlV`O?!7oi4<2RrTUb9Vs%k>K*K=W~O3LE+tV5#J>EP;i(<=-UaY+vdSd_-uQ&13B_@;#UtpS6?N4FhqTOslCHZ0(#bxd~okT*)Le++(l=dn-b;R(vc6>{*ng12M@QgfAjabao7W<HJS6$ADQyfJTdWfl1dNd5$(&DzX{Ebn;&w#PEy%lDT&~;c=|WFe=TM1|hXu<ns`ha2k2%s;7#Fy|y|6V?EfCRxh4T!z%p*4l&CVaVhQ%@9GR$P_tt?@46gEKX8I>F_}rdb8n}S?P&+cWZM&oXF?n6oCe8CG=L^&R2!zy!5#+(BgjX(SrB8J-gJDTV?2W&N?Fe~ODEy*E&TekfpsTqN!83?_79jiF*u@-do8ouNXRA6{uBaT>ed3fUXWX7>kCmrg5X8X;SeUI8uA2YC;L%NzLvor2k~|gbS4@BNb#79H3ons<24Vl8&__%NRGvfaa|&cB)O9$Yn@}CJBv=8PPcfd+ZZDQ%Nh+?kYr#tJmH{Fagqn5hAJ&LqLjE?A%7alv%tu1!B?i0pO2%@x_|(V!h$AN%<T$5Un8j|$=(npmdjv*IXTE6fDe>R^pv5!McOM_7p`DdlaX7Bc>OGsomVDcQWg6HI7A*^SO9*)5y_6L4?y_nnp0gKtAL2+NI1m<=I(_LTi{TN$?5egpbAqHD<?HeW)ZDZXy{z#$4_)XLy)>PWkr4|!Y3+5N$#cVZpdI!Uy8NyLPzbGc@t3~5+xN}RjwPa5-0^%Qz6G5QQhfNOw^4U4@rLIFbmmG*TB4llYleuZ;jwh|K}iJlX4F*Hu>}gmPal7MHW6KgZYh#dSwf?q|TefTOct@=F6FSCaU9`GsJiky69i{cq#@AHy{KMN{*vp={dYIW63CmW`SxQ2P|y^>}>2yGI0lxarc-5kV>l#H2Pgqw0@KVkYxa(i`1KPhT(&~C^+H$2@YI4odF#WSs!1Dpu6?Rin*Cbx8!4rhMwCp@~63xz^cPt^o#M7l$=^VGkyeV>zIqGZwCOd-4QAl!y=7t6G)L|?oGyX!bQl^fq4Ry+JRQ_`ps*&4m)!;<c%chR_1;3F3L@+6W8`OdH%{sAUfk^p(QIK_$4vqUK{K|=J0T3_Q`CJhh62n_jEG*|4WI(!zwsRBPEqrEUV2C47P=sv&Jmi2R|PM@cZgXk+?$Tp`k-Sy-2NRybRGqU=Bod0N6n;OveU)g>zv_>mU!pFcw9MYWl*^+n6ACokzAopaV_P7C{t9WyMcVy&#I+DrO;Tz~HjUfPgwFG)C+e1y)m{R9hp2+2Vb#+zuKK^((Aqa+b-Vc-3^<B0U?6A+9z=+Dze3FvXpApY_o8;c!Z8C#*uomf)x<P^u*tbpA94yC}Y?HJ#?iT(er0f$g$)6+<G8vo);<d(`qW`Vq=uvl*TV2~#b1J;~~1i-gHl;h#}Ne_zsV$-6YCD@_J*;jx<RmAf*G0H|AKXF&Cy#8U>FU<?Z<%{5&BhxwQ%L|XxP)T0s97L-pHX7vClM`1iphdUEsJT42UHps&|d^LX?C~kN7EJY6EEGHC2S0o6r)*@orYAzB0vdYE8n6cvAPMAx!=i)fP$Nl~O7V#eMc8YU#ga^nFhMmyG(=t_4fXVbiJ|5t)SlQ;JCXI$BCipCWn57p%S)1pRRoKPeTmmu$0RcxdKHFVI%3=&8@FOjUGHaJ67f7~($}#~XJ5{eQB+|H{^J|2Jf#7ICqEV<Y@=X@6Ln#hJW#Cd-{+;SoX`YM(*pxf8=8(3`7c}!8k;rs>TGhd@cauPKx`N9{Zh&z`Te%1p92iMv_C1+yllEFFdhEr9KwAQ=02>7ff$6zUf*E+Il6|mGCX<XW+G76HhDk`2Tn`@z{qmGEUACFr982EEF(B9HgEm5Ql3Xy+FdFdgVK%0R_NcV<;<3O+ujXso`g4YUb$#9$L*DiUSX5L44tGc*Oef@|6xP@-ha_4f)L*@#u*exeVXobf<tEtmj_8*FA;~3+#4%(^<Va@u?G_T}kR##+_2ifOdX;ueJtOhkhF)9QmmCEW&4)`I+3n9zPMjq0TMY&b?@D3&iB4kXF<C!Jbe3+U6jTk8PSeDO$;AhV*ENeTc~`)OP`L|;;zX5-g?@fZz)~tetqNI|GEYit%IE-(A9UqwR3JMiB1|8Y?4%SIM3$VLNwWe->x}iT?cY$=26y;})HV~&JYdfEhpf!#yE9^UZPKh)rDk@Q+38?5q6EH%oC|S>`uzNf1xMTq+J;J7nVxkWSQFz{g58ml0Km#Q9s9%V%HifZvCXCfp-X7Baav9l3*oiMr2i0iW&M{stwiS|oCcEBkdM8T<mjbGauN7uK*+u1@1Oob?w7v-P7DU8y)w7R(bq<*-=my!<fL2(UCQ7PHK%1r`k%gJo241{j0C0B`2|qbk+3?T<*Q=bP$r&dS{SyVQjGwYof49?`pH<pLIH$G)acqY(hYv_A8@S88+7sA?qXTI4p`;wey`%UIHQ@-lTb$i4za514<Hb>i9?j3r*JM9I;1AZz|4~&HEFM+1HMF5GPqfboqnh0=LlTXs2+fA1N_~3x@=_cP+PjN@9`=~XbT9Roj54bUQ(Rv&SOU=s*nZVkc<yYN-xrrDCYoUw%*-!DqB3spTJ%@j-?sm<q#Esm?Lo1RGXvB1>5(mN+4@EN0x<C79gqlIj&2gAVAc8(SAJjy^WE`8qVYEmRSLS@jSdMThXLYFVmt7IDt))Kp7ogk!(<daXf=DI{Y*tZQ1j<A=oYrPXV9aLv<K!n3k*ZX~BJZDbyILWGVWPMx4z96$X<D<W-;Rwy}4bbsWVga57uApSM;5Q$vdICc8R|gkWNlK{?1wxN2nsa}`{&0*3Y^A4{8#6;E^8Oi5+6MipBY=4K?9iiC+%8Iv&@?vSh@`;bFaB|qhITm@tjc!||NxuiU^9zD*mCfxL`O}rvnus;ub4iuf6WR)Ddl`cvZxI(L?Qx;>if@+X>X<E%3XE|Y@JG7+FAAk%6$|%<I*b|G?jM0!0qhxnknn)n~NxPM(rxvL&35w`RV)S+b9lmbS_Bs=RSc_1>MAA20dEeKGEGZfix^+UXta}`zFS5{V+i^?}CWJiVOd7piUU{~0#9Y;r<TV<!vnH~-mnE{Cw^-udy#@8TNwri{Fbwa9N2F7CjjJUUs3YK1CluQLa6Rg8OoA>XGXmf`(1WTsNZZ~#kvR)m!rgT61v0(m7)+0{hN7x^ye>BZc`8>_t7y{m04*KR#B|KoG*eT8*J4E`n=$|{*I*f3aVlX@K@KWB)sdZum0$YBYsUBQ1w!G9<=eQlZrY?ApAmWhmx6kBV#Y9FYCfd?yZq-V(1c>2z(J%f+-H6LYK?d`<p3$Npy0?p@wt2NkmppF)p31Hp#XY-3#t2!>(g~<2B^JOIjB*pcKauw-`%ZDV{>I2;-S@wl`FGV%Jx80=H(N-(7U#SU_{fJU~+WlAzhPItv+Nqr0gZ*1?U$?;5})(<TP7#x;&}u4i|K+{F<ni1?6$g3B^k@dHU`-aY%l1mH=t3ZbFbTzGKT`%EsaeAB<fiK9-m2UcW-(IpIH)c82LTV7xYn41In-Kb6Q8q@N8-!r}t?QzBuPvJOJJg?wiwhk0w&N&xws7OcF2Q_@PfZU6^<1hP)?0V@{fsx6+9Se&*FX8i<=pEiO!KHe}&SGn{>7fbVOC0OKXRDQ;|wq3WzF`zk@wVqvr<4A;DiihQC5!Quw!a?iNG|nq^?YMY;xb`X<355ZG@=Qqb1Iw@?)fLv7gUjB)05`bZ08zNcC1yq2q`N}Z38MrvsJR@cv2~_^a(F8|S#qiZ4W4j+fexj0SU09b4j{;Q+-)d_omn6)(8A5^@d$sJQc_d}L;^#uMZp`$3r9nU9Eu(s^?Kh&@|1=SjY8<RNOyHPDKKT-BeCD*QxMqw0u(=i?k1=hS)E0eLRx^eV=Lee?6B@gGb>bjf*xc0$TgSDLIPzYQg^uE!{H{ea>XhreOM{p3>f1C1F;29tdw(p01#7U6fsoNJz5I|$AF|bkRvLd4tb=2&5`xo2n-kZfxW?Jq9pH8SOHPgr$wyW-S8buyUAy3B<XtOg*OHVcQbaN-WU%#FblxyVGb12;YyeyLuNaZSJ^=3`~4{S7UZH^nVB4zqtYb6t|CWt9!`-J4HG*4M&#con(q@k&qH9`j<U<BumCW#HS@?|5&QJw$sUxWM!<%FdeCyn=I3>1=%vL3Zc;)^G@qC74*>051#E;JIFri}T_nLSkV(R`NvC>hEJ|jBGMoy#J{>!YS_BMPhEFytn_Z6UZVrd>U9;akpsI<J=zH7YddFab*wr)>3sC^xY2&@TM7tvwppT96G15jiQC7D3v=|Lfd!B9WWY__=F>d&TXqtj?VxCvWI!r4(iA_!oLl-KtQZHJ|0vBTd5^1vDX#EKa@o6<Ui-N>-uV@BR>Eqj5xnH2JIXgA&-)YHKCU&DtVwQpLE9s+dH*#ooEH@S%0p{fN#~>uQ?Ur#3kUA;?f%t)bu4tqSyDhr9menb1H#8tJVMkA+=#VMyZ_1<M4DM34S51-!rJJhGqrK1)giIT&4BaqqJiFbCElCgwRV+ZRl)K<2%#+L7LXQvnpb>y;f1b?E$<}C}fQIrPRXsGcQw53aOrKtp>!jJL8-~s<^a@y!m10}!rZNEIbkEpy^WRHY1l=8zt%7TO&d#J&y=;h@|6;m44f$s?+LLWDCH$<Xe2vZbX%tzgr8`$6h{-nPkl-1IH2HJb;+}9Hi|<?7`!Z@}<%N}M<R=4nYoE8j`_H@o2VRj9!T')))
_V10_EXECUTOR=make_agent({0:_V10_TAPE},dead_stock=False)
def v10_replay_agent(obs,configuration=None):
    return _V10_EXECUTOR(obs,configuration)
v10_replay_agent.telemetry=_V10_EXECUTOR.chassis.diagnostics
agent=v10_replay_agent
