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
_V10_TAPE=json.loads(zlib.decompress(base64.b85decode('c%1EBU5^|`a{Mp*JP+oFKF)6xxhD~~(h^J3ge(w(0H0yNI6ugKGw#2e;_h@;cSc4;X4k9)<DNL2nVqi6%F4=&jLiD!f3N=imtX((*I%#x`KPNlFW$br`gpqfk6-@l-~Rj48=qeO?U!Hw^RNH&>Ge-n-@O0v=NCV`{{F?y)#>Wx?T4$=laHtSx8K~|zIy-i-KY0Ie0Tlg)4yMwKUx0Z?RVGLZ-zf9eDLw_r_Cr|zx>PlH^Uf`@xHyjxmic_`S-tjeRq8&UZ832M)1x1*Eg?z{v@q;??3<1GJs)l<Fxpjt0?35%o*(^bo1inH4@NIS3lg|z5DL-JkhHU*KgmAZ^_5Q#m`sl;S0|;L)t%d^J*{ZWN6+vUcT5bSN!?(fu~ij<1)^b)PpQWg#yn+?=4b%nB@7LD5tmA*RMYP@%Ps^w?AB+p8A9P^KXB+8Qkt!P<+crpGN(|yXC>gz;=(nezBL$+uQf4n(X($Fpv)~-d*330c7((D+1D8x+J@qGbI*7h)eJwm0>N;PrLt(VZ!mV^7Day-k%v!ycLOOOCG1IWePtNdm%Mky8{u<vMukel?aoM56|YcdE{WtJw1PB%o_cAG}}!nN2Nk1K@@ZP*@O`UJu_DKfN9yUEZ4Zz?(O$ledZ58fOd3zF;C*amXhasg3g3`{ww}0w$7iwG(M{!MYLG^56MrT|C|nfea7xH^20B0Z*Hz%zWe#l*LUw;-@N|U?F6<9nz_q~-#PrG?|zb@0%b9OXfd+8Ate*wG8y+`@}jno@NwzetA__ZCl7vgcl##uo1*t{|Bm5Z$Mb6E<v&fH36%AIh~C0^gNdHQgBXSv%j54S?>~O)wH&o=VWYx_KQ$j7V;rz9$(!q;2gcN!`0gk9L*!IeAGiK%Q6nDS0f)fqU}cif8VL6LaC}1X`v*>R(U!?T-%0%*J7rce8Pd@{Y}f#Yrd`@t|M<24_rF&0YMKDyeAlPw4v}aD1Z9ag;X6x3A8E1CAXFTDVdXAGw8x#&c*GxemDb-}TqU$<z>iN(alMux%rhV9>&YS@0M<ljOh-E)w8^0f-`5d1JPX?+x{h!urG<2=AP87Ki!P-<_JH8b8}j<o-@Ul|7l7Esu(}e9jX%2Vm(7znO7ZsH-HQ+3T;JXOXnL2+z#{+*f}Gau#^Fa$8HF{51qXP+gL5^AAp8AgJ`7PWNpErSmY*)j3`}PE>vhn}Blh86&ozjVz%HySBU0-+Qzy6swKQCu{yZ4!6)>($dfxeBodf@H;_y(vESzS40Jn~&ix2sAH53dudD`Au5Lljv_K_jsu;kPQZ0V&8V7|dwZg3n#fNU7Z+1xHxvgF!;m>`PX_n}XRoCc81K%RETzXm@IJnj3lq?t}Y`*3toTq*9sOe#fwHYTnMunq`lb;rO+HxWu24CPt(q}T~<CPp>u1NN>#3DE>Y2Xc!;_vJ>k6vqIBK;r+j(uqZAI#42;Ap|b9vxuRd>(7i*T87;T!<2Bcw|85=7QRqfP5SA*$ZNlBrJz&C@{iy~X8t6DlPK$rQ!2J&{i@(cq9;fn<6<sl${@iiHP5v~VxW*A_O#?`uh~_R(IuY93`h~Vmh{<1&>tSM2vE(s<-rr5G6#CVH0NQDz-j?TFODe1LUhExPxe6<8@P=1ZH>bIVD`({^&yvDBvu*PExkgP)Q%bC2zDlJ?@^bWOChB<?R<-UJQi0(C%S<?06MNuLdbo(p1$DVB_O##dSH_}K|~ZZ(w&H40`qkwU;^s`;8@}Cwg_q{42!c&R8mS9Jdn+64QKr13}e6o-!xdixri`0>E=EF5Mll>zO{6+B1pP7E6=4r+se%yfeR;quhN6Rgue__Q9eea>dIqW!Gh*Y>(oR9UI{Ki8+c8f#6>QP0GP+@MF)`v2Tp)^HqDtl!M{==q(?{-tRPmejiwW!l8ogcybu7w?1x=v4oR-gA6;H_R*Gf4Sh7I7Kgf9Q5WSPbf3fOSK+XeYbghU!P9+W-oP+8RCqec4`zdVLg!E#~V1cK~5N8c^9t9!O0PCP5)&VzXaSGIa+-hqB6ZL&N7^rFY?pfv+QP{JS92f(m0<=iBXkk1AUQEwU2K*$0^>WJ}Zf|dXqcEKA&y`P++^evhEX5q{Ok^G@&~yiHIpYlH-|`6zs2}^YVpIS(LS7G?GRqL(knz7P@G7Gxfo&CafMf6{jn)sAnk6C~ol%sI0%s`dH~=nJM9LROx4xRkMR8qHLz76^PX+8m(}3x}y}f;VUEE>I{MSE*)kaBTHvaXvD2$St$b+M_ae3q9D=6{ccA%MrRY$B>lyb?Gu`^n7K2%l(P@498&>8O}!w!HKp=xN+fbAFuI)H_V2{bJ`=UWw~eZL`I-jbyFZu2~RcUY|KeV~V?C2^}d&$|Gc3b-oa4;b?!d=+r0b+)EQ2vS=L2zMRIZbeoiG5)PAqXD3af@*=dF!ss_eH&2k5V3wdV|5V<BWQw>c35#N2ulke$~Vo>tDQDEU0xtvDxHGgSqC1Jg4Tv~29#MaV8R-$0}NVRd<)VzMz_t24kRJ&GO0G2%Ojt4;2&q99IQCLGc`pw5yjB~5kN-g5z~@ZW~WdP1&$09Py3}8E6b$HIV$wEP?!K{1K`JAje#Gp+Lb|(jD8On`2wMVfFYuH2l6buCE~I}vN#cG>N--ucPe`(prxlYZHP*^DA(#3($taJ3dYE50tH`FejGyvk@32a<)P6a93)*SZk?UZVZB0IH_%Q+7_yiuMIKCDLWc8|QBp=Z<>$zhw0w5tZZ!qeP%9)qE=1<m2(6G$Vxa>`hy%)$d=yLMG64eH+bTJ>2wGlGf<l)8B162l80vIvl2K6#6=zO15!ozQv{+}?IX*E;>lRP`BRSLfqLw=(KgY$XnGTOOEs&s<miF_>deO9T^ylJM;64X!?ZQE~hZ%qW`sObWIipr%!A>^WFDe0^kTyR$j!UyaYGiqNM*hdRR#8ubI$tsJ2}q7RIqLhi*mJ+>XpQxs4H<ZCg@7A1FfE4@kRjmHUZc+!H?JIitWYAs#;~I~b3i-Zlp$|NBB;U@GFQus<aRHh9SviM0QLb124Nw_?n4cep4=8G3Zk-!(5!Fpkb*<!59pQO-(WJi%5(iOL<ZKHEZ;84mDbi=a9$!Y2Z9>dni(ebgCBtb{%-Sy0$B#qc7{VM?~#sFkhHIgKR0Xpfq;sw5_*+0g3%w$8hDn#2IWV{9q_n;Vy_g;o1LkS`7LD4mJud7x=Y+QLGHVtNl;LsNi%c%pO}!4qvJ!$n%35Uk(S5jG?$8u5oAY*u>qQpe0jq7W!`{Wkjft&RSwdU4Zy$1bR2G#(7g<TW6}9~ho;d?OF|yFt0gi0gi61WHW2X4Qv^TnyRsr2uuFe70qpkNvEPyWUrmT@@ttmmIhaj=qZh>jFvv41-ZUD)41-1;y!e$=9`J-3z#UYyZlFITXuqd!KR>&3@+v{n#RT5jhmsYIf{;e<#_G)MF5Tb&LbYEuPIs_g7J**Ts>8*JLE89fwD9{{+7pB<e3A*nipl_l*|JCANIoRiTC988fpOq)w!=Cca(f_aAqi+3j3Kd^mr=^guJ+5*mv|#_j!^|2sbsLDTqy^Oez>bex3CT!Ep1|tAa2zcfCse*waY!Hs-=wz159dm&k{aLfKr)P!*W<Rn*z(-n~e}oiN{PL@-DmqTx%l^0d#tj{n;On6Mzd8{O8p($*YLY`W!SXFX14GxP&xH6JU8eLsS+k)l_a|DW<^`HYV7TJ=nbVFpP_5b$~BT@yAYsRivx>j)2Xp=uNhAwHY*!2#0wI7h&XpsJv0m8b!K-1k~^!;+=r!vs%@Hpn%8j&|et*;ko7_zLRI>z~GqmqQEADX3Kf=d1A2K9#!tx2|gIfgFHxc*eScSh6u_y{=B|`HsWM;sbLWckE97FA)MoJw@H|rvD&#atr7IPXYwaKBY3kA%T=@VHG}4!t2s2lF{MkO;o@HPQRXOq=xfq_k!x&nkc9|9Ot68QyKCTD#G?kdAM&z;+I&{yRA@+tT#xiZi)8s?B$%d`^o9YR6EHMThI}P};ZlAS12IOuOH@%$7C<y`6GyKw;vhiNK*|UnWiU@iYU;~-j@*A6l?}lrpoobd$|P(i4O8R_K6&0QV;kM-hp%o2$eZA>gJBWoe!;Ct)&o6A|6q|zT2Kfzxl$^|7IVvcoHWhoWLT*&yxr&%1~n;1=j4hRLm|iiA=FHwA*TqAu~Wfh0l@>#%Xgbh1c=ziWKxfl5RJWzrV)M;T}4J)Qf>^nBBu#qQj0}E73A<nG_!l9MGRJ122@w_60IW`E-y=Nk%v-rDp4fSuW21L#l&cd+uYp%juUc^(Poqc7LN{Oi2|cy8^R3QnpavB2Km=Hv1m@EPNpCP(V`$1sJh!9AY>9OTGM%>%a?4$4GBH?OT6hM)+zWRCl~b|luwgXpNu*2mbOIjjA;!pE_vBaw4e-A%3Zcc+ls0(*M=@Ei&{EVK@bY;cL9qq8rAyOB9h{KDO1IXO1x&uYE$_v5;g<Y6F^7Y(gQmC1A2|&Kp^xu8+`px*@-o%C2Erekq@xw<|ub64(QV+I8io!*`hws($$_udj%xKlLN-uR%b87v1>b#0W<faLFJynj!t!VV`g(`uD3nsg$PJWaoZ_amogBLS|?Y`wZdbh?=(#XCC!5DqooJ-WtYIbp?1)O?vQBX;WCxzm}IUFL}K~21ggTAAxDdvEOZBG6+U}Y7HS8T%SwTEs~Ob<pCfEfgH(oxWXyoTDX%Ee;kZK+q##DjT>bY`kS$aYKNBTkiS&ov%<u}DFZ&#HhV%*VC_pGPaNt%$nns^ZO6-9O?36zhhScd-^W<~fd{Ok{jF&Hn!aN)V_<p>^TO%G{eEw6fB&<Xl0PV)mrjNckvddobD-m2V^hr`1iLL0g>0yA><A5Y^1>!Mi01dmiwFERUU<A@XYf)QVf?e2JipgwLgxcjYzsJ%Nk^#ZdiCH%bo$zfySz)r->5aJcB-Av{E_>~v8b>2_mV9x_r5V%S47g5nVj32H!w8H!Q(IrKu$jwlIOKjJNWyPrcKkm2LO5oneL-XfVV@Yy%>^CEctn(wL<zH@Gu>kq?n7WBwFXxrt54&)yG8Y*{>HSnR2q3AADy?J-Y;lble`Ka^guxxAC70NOVbD{4%Z}?7&a>Ggh+t4n73>}Z?q#5>_!DaIF9!|3gn!f`ab2F#rV<znYSUry(;T?RB|Q54kIWB0lPl84opMgS>jcWynEs8^|#+%oxV0uD+`MSkvC~X4N2D|Veuf<Fj{uGNp=W$oD`=KTQ1fJupMHg%xgdMyAV-~Fpr{tavCHUjlK<x@%=g>hC3a>DO~zRk(=pQ=3@Tdj#4!tQsvxKj!=B=(DVo$B`Q$?;G$_=tuMr_0-Okz(t(jhd+~{b1UD9N>awHP&dG9zFFPwJSD%;(nO>c<ydo5gr#y4ZKxjvftW09$q7IV<RPbl0)6y-UVH<?7Lm;uOxKS8#u536(3Y3d`Au!B_jM8Lrx^JW{bt1g}Rbj}UDqSX9E;YfkR)T33s<$DgIMXT^Do%g~5cpKTEFsaNs<aDGS%IfXR3uuQG@{(y#eN{t&z3klh1C`XpHCpJcm-J`@E0VrMr;WpVSov61PExS!YsNn1)K<8+6>0V`|WTjhifeB(V!#(ihV;b*=(z-4VFafgv&vRCR~7Ki}ogqV*ol4hVc1xd2BjIxj>`A;^+vYGCfM-SaKkY3{e6a2G-O8)P)EoXgg{<1-ofdo{HTkMprr1!p|PT13;Mlmb_Vk(?!W1z-l*3dn7ZZ5pUrq#Vd$1_e3TZ=%kLuWsYLo9us0X>BMcLegL$&fL$S&_XGlaUiG^7qa5=BAQRflh`#cW(@NyX;uca8X!UzIT#jblw1Eo$sSu&l9Py_q3Y!E|EMV1G+Z00}6ipcd$zVrGrCdATzPo$z;hXEbyC1=>0?`RF2^jNLkfve&j@R<XATUu3uXCvdhms`FEOZ7GWl*h3TiWXVxwaa-%tcjhNSW8@=exbW!D=CriNv_tjn^mJGu`SKWkZ42#A>?KHaGl$$JiAzh>wf{<#N$^6mTBe6%912eGupaac%P%0STBp^(2sl>A3}JZg?9$HXYe&aLXh)32I3ZRoUtQ9kFVYA_xCP@rs}lYBFq(@ksYb9i^tNqT>g@d|~-?L`t$>2;U)o%=q1}da`nkCK!+l7B=gOFMybei6Ko=jTR9;U4>Vzc)<ukbweGViH*fhgDPgrsciY*7&2jq;r$e!{8IxRdv1-7CX1}Jbh9ErPsp#>={7nUa8ev2<*i97X@+_Mjru(EN$`zpU_C(qK96$4^1h193!F*Ytkl#CD7U{yA{#4DRmc7T!yz(ERfgM6WmXJz<TlB>2v|gS@TIsM+JPi&NxPK<2#e6)qK02EAy=q^$d{jnK#BTL^sX0pqHC|PI#TiA1(%x@g-&&NDdua_e%<3ZB?5+%Vpw$?MPX2F7C=ZG57sPl(p3sy&kCRqcZ`;kGEw#*rrya_hWQneDP0#u1)%mn?gz)e28S&_nDC|%g$J#Rfx#sbiQ>qT8HGES+y`KI>dkZ^DTjS6g2w}d(-rzCFWFRx>5Q5EO_@EF+*g!8THegG%8EC(gPmUc7+Fdrohcyzn>d#zIR(<LE=0fCRiHG|IbFCb3#+q}cR6$5A-<zSyL*f!0!UvMrbIXvThh{(o52M_lVsA7sKswtkvL{2_<m$NleDlr8hO>0?YseFOZ?AqRm<dU(IXU7g~>7%9Bl3Ou;>K@>apaMpPu9kaoz_q_8r{mlmHMuK!gl%V-qC+5m*}fWUAcKEV7o+qNX8f)Yfcw<d-<)5Cv=OnP$gIlY`N;0NO}5DjYk2L1VktTOjusjY)hw$mpl5qa~$F2$bmL_1;K)t@T18;6OWs9;auwpRDhd2!d3wWHcxwlP`Lqe*#Ei`lYNC8l%yV>AZ)iiZYN-M*^rkL=(;ch@JrQ$rKpQ?PxDh9Gb+Wncw%%DMgX4XWSjRdNG-qy$PRY>zE@?YI`_%TWaS-y`xL?6)}E|X{Vz309(Z+18$7;vzTp95_^mZ6Z`B*U3@ZzgES5j%a&nSvCHNF5^zmr3>tRwCjD2!;6=4#hVl}}AqM6uY2XN%b__--A)CRC*&HFca@MtDa2JfX&{@e!%46MmE}a@RjkXdteEP)ULQW`?L;>NFt!}o5&brSZr+h7LIP)eU_f6dbN5`>QAscPh-00XE{UR0QqfoiihV}qXK}s^>_A8Kc;#-Fs<wzL;f7I@VQ!TD<a)cOyRlppJbhaW@&AB;{_N`(4R#1wLV5Fr4DJvqXbXeix=Y@7+G$=ry&6FJS%`VY_h3K#@j$yvpG3^w<HEZ}pgLr*qX9+Q(3T!)gJoC?s>SrL`I9#K;3)hGGi$`zRiH?c@0EhLbbVTrd&Ak_#gpImC9lV!9cP=ngXrXz$0Z?8mJfrj|zF)hZP$u;}QTH_d8Rh4|*~Q!G9oi0oa%pUg;F1}8m=Rh?_C;*pl#XetJH;x1&I=x|7XWWQ)P0|OM73&y0M;lOm6~Gn6CAFBx{w+$pt%B)VQ6R`UzC7-3kw||k{Jmx6&;!etwvaPI8s%C9~cVg9RVhnFM0q+K@HLJe4t;dR0W4NfLL@KY%}<arwh}CSl1t)H&m^}V(K{LmJafU?4t%Sg&JHS)<e5Sof;?XWTyR^C5Qzg>LH1P^T+tX{li%ls<cWS@m!Frl$<H{Pbe{USQ^Izq~ZF>IW<^p2iB!XGtz6uX*@a8#jcN(%S73vG!>_+w=z1yRN`0MDTM?Sm=vjetl>EB9U3Pz84c?=9PCP#$riYBar5Y_V!)?%OJCeF;PpbQn`Dgncgui^$Su+M7p2``={yT%$(qpZT&Hvt;vAT`RVI`0xPdK$5CuasE3pN+J{V9C{bDmVp;xcJ1?p<MEQv{QbqoTMcu061;SW&6z~atD7pz7P3cZWqP*@~=76L8AMJ&_<U2Ni_36N5~%d98l6^sjBsc7@~O)=|bHMv=l4^EX4L=GbX5!EgX$Kd@eb2;k}vjo7wKK~ilv(XYi?`s$bcvuf72<!)SrEr`w3I}jP0Kc5&3Xv>U7YV^q$_qZPV#Q_)J}N*l0e6$YSTvLai)j&`&hpRiv954clL|O+)fcI;^V)bZGa&ERl4W(HZTu{ni=t(ZLoyOID5`l={uLvIlqr`lBXZ*r;U{4qk5C;ebmT)7?u3n0gEX2As=XNT2=A)bc^l-S4@Mm|>_7nak-7<-gqYUEKT!)3LLf@E1YxqU13g1LG7zT^{2BLz`MuB5G_3Gij`j|}WXBFs8Q}Nivh`9{x0NymaXF*q15Rd^ku1RjoyOhGnlj{zreWAA_m!%`XUwVuCZ-4ntyhsdCiu!_W+0Xk#3x~x2+X$9pbND{M&;cU(hEq1WLy;qaWlv$1X?3ie$f6FSbn0?no=tJD;TRjD8>#*Ogzn*ou**l7QkCxtD@|xym5n_qmWn^!{?bRV&0QAnhRWLO${HWDj11{;cjAQcTtVw3@2Gw$M|bxTABIiFJi|0iq6d;n<0p7rySO!0LfPd5R#rfz@Wj+32cdn<@G2|=%|WA5v=CKpy;AX^oKK!szlFN!M9)bL$6Lj`Fyo93FRMX7pgra4XV(vRu==eM2Aa7{5k-Oa9r)Yo1SDuta)Htn;(y$9{8r)lOehdrkZa`9Q71QLo2Hi$=C?-g(N6~P`}r7x%PIqDfOk`Fc2DZ@0N83D$&DW?L-!PR!DC)yJSE2dd-1#A-dl-g=UNPhj23rkLOK^BzSgGc**s&m>cRqa>hF#oAXXPX;^eTVJ;hF2m9S;naX%hi^<{ac0MBJzgA~+ua@wLp;3Dt|7vIhLVd=%6U;(($kV=|2+(*H*;JAVL-Z5x9C@lN(%7eGT0yTlL9$hgz*q9#-jU{>ssr%Bh1c{^K`N~fF`J?#^}db;cN!y)znT5`G}cI=x(tF=ktOJ_i$+_Y3|pgKX|@h7LfMd5MNkE&nR3X~(~(oy8!LLky25`3`V=XCt4C@B@`b1pNIEd$BELdXovN6qBu_1~_g$K4Fm>0;6d=YO&_si{bb?^ZK*0qq@GP$2DOmgQ@G7){WQBp?+=&H^P}5nf#4R*13zm82-8xr#VYJ;Sd9@ZkvnwAIET`SKHS;`cxP<z!cdG|UnT>(i(1Ie$B#LM8o4ear?_aLR_1d8`e4=kkY!ibNJ<9KYIT`tJV7Jxc(yP}cmM+(@#~skc3s51Uk*mo(Lvbp+4p~1HA0h~Xyw|s1_}QeMLE3{y#4e<7DU;@M#3p(&(xeL2yK3r!$sdE9<c2G{Qzc8jMJs2VH-Ts*u-^WEY3t+JK^uiM8Z3UQVYIVJAuV5y3)6K`C_2efAL(wJ_fI$_E;z>N2*<TV45vW_s0N|&J8jpN1(<?JfexkvT5tB2#hJ&v;gSi-NTW0rp`@$=>Cf>!o)*d+1qN(F5W*M*v={6M%?K;BfZYc{a)ww()NJC`ZUF$%uitJ!Q;#Doly)I!U_gjlfD+?l2P`Q?5lP(ui#xI2MjHb1k8Uwcay%H9KGgHM9(O!psYD=DQ2QVytPZQB#3Ekw2IxA8%mIrh&TJ+fX9I;ja*5le=r@QtcM$Z6i7i#d=0gOG=D`CJ7;8K}Ehmn)a7UN-n+I49xMhlPxxKD;juX?0L*=i=!yU0jhN9w7IL!$}T~3bOi#)5rfbSgQ1(TRnZU|oYr+Evdh)HXTQuWyJf+PS*uO%kG<j6k|EEp+izho4<XtZni-j$pevr6D5LQ9dOE<z6&PvrpWLTZRt0Wl25f`=)1ko^|nABdy*2;LNQ&NlcU@UV$M623_kCbkn{xE*k#aqq09Nzf)tsKlWt5!xwTGw}3k8=xJhPkD9Ch9sPXgxH*_=}0S&LR1P2nj{##T)fLXAoS*0rw5pxD(-@>j%2pTz8M<7qFc)fEpIaBN5K`%*fvR`qY3a>w@dK8V#ziU=bzP<%;9qQh%spo6?(A&$DBwwo>17Vl=}Z*{bp6i`C=YCCIkd&Q-a4S@s0-s0#q%KD*KdSJ=KahfCk;a#WXw+^@69@28j^4<=~5QA0*h_D2IsPpZoj~tJy@P#|4z>5;w2eSC$=O!$^=cs290OtKRacbRSrbhZ*$NE=$XgO=)FUw-HG%CCn~sllX=TKbi0~DC~9tVlAgto9s4L$M5xt>g^L1tT=djrk0hjF{)HvI_BhGF5Q3y6p$zrNLmv)2&F|rp`4%Y%+OA@Em9%KVLbrY29K^E?Z?Y<2_Rx&C?yj5?EAi3e4eyhFTDE(Zzvr>klHu%!n{mDoGlVEKr;#pfHDE*zanfRP!CzG?eS8`$%BNBaW5O#171m0Vp}8lSKFp}mnC_C?gS3l5Ws5jN|f0f7ansMMP)n)@U4`|N_Rj3U;(m&@ovU0NjJuh-<oT@1EP3Vo+1?CC}<Twvxv4x$@7uLq)*O1a@)PAZBUA;Rp3I9Fi1~dqQn`>=}<Y5Dw}|o5rAy>#kRjT1%$pDrnDA_nMoUbjS2MqBT<MJ)i2*SR6N79LfFm&UWyC-E;VDBhRgd!axPG*6?Uyg>?|q=4HC%1_ENboANECh&m8zn8Pvn19Rj-C592_U7`|yITm9{Pk(0>W!O0zfY|KdC=Ya>_YLHZ;Cdtw{RwTn*frj`Gu`qb86(}~xej@h+j6@HoU4)Q5L+407?4(i<H4WHtL1I}A#}^oxi!hONI8Y_ubn6t8a+eBLD($0l<(MKp>CzT1cq{RLImj*xYdJkcG^b5~NBpH^hg_lqsvwV`<uUuaQxvjK0rLnGMwNk5DRE0$M0z0&(<_8PG@=I8jUiqG|IXYPJa-NfX*oP6Sr;~VJsXaZ6aX{0L)$}G#~kJePO4YeWb%cQaWjukN~zGz#crkx6cBNUgC6qUmef1cmWq`<WmzY>XTg*rN>l2-C@Kn-c}MTDoJhXMdpQE$7@WGOK$a2=aSG#|5<Tl+k9pc<eBeS^$2U5TBC$&I<mmL9u1>sJZPPSqfmr5th5lpKq4~_C40OnmCks{D`VPA{zt%I4$$nBS3|kHHbf>}4kyewG6xGQ?YJ(_X{BZ4=?+TbKA){QaD|rF20-_Kn6nGhjMs6&s2<cX;_#P<o(g07feb%&oIdKcv?FbZFpq+&pSEv)GABgd%Go!$E00AXyTZC6c)qh;zZka}7dbw>JAjOWIFLvP!T|~o{g7cB5c&S%Uk3EPB@$;6PjBHtQ{=hUa&+*G8-9jdr;8MgLDe6LM(J<90^a>s48S%$1d<`WVlL?eD7@?W7l*p9vKUp5A1yjb&kyluRwm4#~jK1d&SGX6XsL)c{K_-*;-m5WkWv1H4slfPvnRdo4p$ftGFD3COW;NSBL~Ve5N&s<yAUJ3G1F@=YU?~nyu^IjcJ`d8kj}Wjm@rfx~fy=YER<5%`8^zSIUCK@_a|84y(4y1Y+AFwp^7aQhs3R8%5S8e+*!Ok)TDWGfK}<Re;u)gb9DH%HZq_*{)MhOC*pk=ZLQ3O6Z)-)CKU(EROVDR8s#nl}N{J~Z)rW7)NMhK!^g;=5Rmw;Rm_*v#F*(CT=i4mmXi|+#_lYLfCE+Abm;*OeG%}fvlZZ4I;|WmgAa~Jnv~kv)%(PgxLc)2WfrmnJ%UjCJk$KKzMESf`ofdtwBv}>|IV>#z2a9}igO0XGt)+Fc@J{mj5Sz~1DG?JkyD_jxkpUuPHCrYirK#x469bCI84to!<}Gd$y^A%Zy<G(KA0Z~fUa_|L9ZCn@!w~FCivbAJ0}K~>$UP&wgt}fCi&ta@0%Q+C^TNTn1lS7%O2Rwr#d8Dvge))`6})y;0+W`CJE-&__|PflN{W9WhjIMEqGk|0tU}9G;zvYGEZd@Tm9*rW!2dm_Qw(ZiVg-+wD7e)i8xe%sTs)wi%&4#{)>u0|)R9|SnsDu*ft53?2`Tt;0b2sIxSwl;Dgd1a5USs&c5W6z#VJycSzouv6R27y7+GjXE6qUc&AW9^?&||9b2#||WQzP!z-9vw8xd4=2~~ekWg9d_%V}?tUEn()eh$w}dX>}<!;swXaWgTs3I~CASsudPnJa}MkzJ7ka-_B;#zdOUTW5@j-aa7CLvj{b&>5s8l)@BnS=2{a9syLKC}-XgLM4!`POK^c3lQrD`~=m->21X^F-Q!7C_*1QvoK7K6#)=aU327-RFgnd!Qxb=iX1}o9<_5V20sawts9Ee>iUi~JB!D0h;<O2hy>^0)z0FA!uJprDsus)ElaioOd>&AaE?;$1!a<iuO09Pcg<OLl3*PX@rZ!)U}GFOPzB9vmX!z8pB!X7!7z4@R2d-NDS5xvDcwf;Sn(f02Imk~P~+ur<D)5kMo4pX<yl8p;yv*hnP}JJXB2a{B_Oa{zc+m*bf>uhN+BadgJ@&H66Z3-ljj06wgc-$-D-m-zc7UkgS<f}RT<CBOSRsiooCcuqb!PA0f`YMbQd(SC>l_kQWI{I9_+Mr)f3B@02zT=GzaxbLe1tBI2NQd>6+iKvSI?K5V0tf;Kd;V6vip|LWI|Sb{%zq1lCe<pDB+_JcniHONefvu>mTm5L&l4!IeNqxVVtWr0D)|_vw`0pNz2~6O#>yx_rCOJ(UIn%C<K(N^l>D(z2~59c0C5UO;<U3N!|kB{tf<#d7X{p+Scm%{Ed2X(s+*=0e}#fWT%Y%~0U5a7769iCEhZmfYUGs7WcF(U3@?L>JWzY!H*XwPr18a0$&YTRE?fOf3c;hndxHJVdg%b1`j9vcV_9H=Rbl2-o2iF;0AZ&IkX2F3nCTHO!mMzeaQJa)i>Hsn%RZtXA`pz)8_e$`f9DGgzs#_5jN{BmZhTbFwQi7@o|B)1$3*o16+nMQ)`O<GVH(i&59-5N@RQNGN#A%92EgUK@pj{v=5dAwHYHn55{UmkEwap7Qh<(WUG%g{-w6rR?U?ARwz$`9NU%o6chDodJIl1aZ;%QU)rm%av@K(cwvggD6fgW_sEI3lffP8hwUp1{Mr}F~xRx<V7`CvJP^654*S?Ku&ipf5l=!;Nb?(oVt>1^igHWi|G2g+B$|6XelZiFK!;7!z}99tC#Jtt1MygNtxuqpt+8uQ<ACKFs|Z>W69SV)q_;S28*Ft;YsopV^V*1?M4fbG<zc=vrr1Tt!N_e<KI92AF4+I>i')))
_V10_EXECUTOR=make_agent({0:_V10_TAPE},dead_stock=False)
def v10_replay_agent(obs,configuration=None):
    return _V10_EXECUTOR(obs,configuration)
v10_replay_agent.telemetry=_V10_EXECUTOR.chassis.diagnostics
agent=v10_replay_agent
