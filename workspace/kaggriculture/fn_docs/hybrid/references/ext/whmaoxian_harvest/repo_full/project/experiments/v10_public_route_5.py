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
_V10_TAPE=json.loads(zlib.decompress(base64.b85decode('c%0o`OOKpKa{MoI?t}QyuI$^0oE3>3YJ}m?#F`KU0lNzW#`+-pX86B*I6eJ6DkCEztEz|8p4e#id|y4X@(~%C_33{v{{HK4|M=T)7ytU{;-|~^?=OBnT>Qtc|Ml1ZzW?I><3E1=?LYtaKlh(MU3~xHFTY&=`1al9^~K@h)y>C?!?T|c$FG07y?OoN)!qH~AKzSE-v9gU>3^0#c>m_=>Zi@06#nDq|2ynP`S#VHKm4>ALo(j?SJ&6;h#sE*=I!m(h4_$6^Z5VGP`>~0_WJcN_se$o;o+~Bk!(h}oge>leVO$;KHGNDt}kC*p*8z-@#D?y-J6H0qfZ~N-rsG%l4}g*A>YKuAH3KNX?bb;_Cs9rWMtkjUR}2P79W3Fy6s-9!y*402lW2x>h=9^-(6kb{CIJA?l0HlI&9?&y!UZ7X#I{K^oW}G{^|37@7^2V5myYZ;g5IAdv@b!-gtG{&h-7whai=$IOFyBczJhqOJ<#|_US$FkTg>%92VovalO|aJWgi&mN=BtH^=AK_xrTgdqGR*+q`Z+%Fe})qP{+pzRwi(Md8TzZuWKN+WUJS-w|GKul!z9hmDVl&|CFZ_RGuO`W#&1Q_(B0HhC|T?{qC@4gd*t^VRNk`q8Tnef&Q(lg*FF;_8>JuQ+|!$Wrsw@S``IwLChkkpJ9t4G!VueJ?1kNqbChuCK3N-Tm^XtJ}M`*Khy*;R%WVoB6njXSjK!?;w()QX@(qv?!})NQtu)R0>}t&pXm~5x!+BK=PrlZ*P9ejwydS6TQZ<exAJG(a*wqyR`m>EqR>j<^!4^)dj#h#+fEx9_K2jxcK9HC#mKhuAk6bji<-eTU_qt!*Lmj6vWj6PU`%fN5>?@3&(G|Mfh=QrIQwYyUj`453sbTi{@SirS&4Q4ViN}_%v-+$WxeuSFn1~TOP2Xt?3-J#J{75RP28z{x#o8C^`-x03>iwVkmvLqUb!NdbFmIBFvFYB>Q@A3ao`?{>I`CjQD859x%O2->6kqd~|d&EO0<Rm!WD_%nf~v7GiFP@%Uuq@2sHLI<zS>1;@*qsvbPVQaT1reXr#)Z!T~Dt!Lo;>C1x<BDuUWb@<-j-ClnD{_6JjFW!D{CjsKqh|g?Z&^Zb)e}LtJvG}eA66^@(o?fvCICHC;H>~T%0g%OK3meO<I9O}(o<-5c4XuNtarKtR$B7ZYq7$OZ9=-c89hviAW{Dt(Qr2w)8(5N$(%`>(zc0EB1AbmRv_Bfq|JUvLtzSK%>$kl9YjXXJG){^=DbKI>g&yjpt++Olz)S(-2(-tLj|c|Bd_?56Xobdoxzp6v9bI(g(NvWDPw?P%&|B*%AtZ0qi(CZtKh1qY?qf96ajiHK*XdD4U+!aYFk5lyTM6icML!R$$+{I%fRrzW5_%xd!+oRb8pA<}nM(5yJeKu=Fiu#uQ9c`PRX`$}>14j<$ZmnS5Fn%KHE2t6$Ez^>ieu-m{_ovi%pAuGU<l4>&O~El|E}OrqBltQ;7j|K1u*_>UZ(T%Zg-Ob2{Zjpz+a*3P#*{I1pq+FAmkn>1vsMFymB;a9*7xT0LwoGt6`)K;%e|X&0Bzx+;3x?TU<K&96G~lz8~TlC^cTDUv#=fP4*W%-y#a^ULof9qD5)^@<WR5o?)SYlYAQMG8%Bo=V8Fm9|RFHmiI~uM|p(Mv0Y!#=G+ekHf(u^ah+SJc+jD1+{2P*2c9on^btQ2kQAeHKKBKPs+fQ1L1g9fZ$HfC<UJKOo9efh(xEM&G~j(t4a#O*KHyKB(OHg#3Be>x!e~<)U^s215*+aE_1wh2)Qmod?T(i&{g2$go8qq%%g~b0Is`k={D_^X0Jhddh|gHtGxFpng6#3-oJERzGBIQ$d*bs3z2|mB=Yw07V<F7i8CwD=9#cH04(hh`*s~4Ts|}kp<T+1%f+3%SHCcLWIFcUb(SeKl{u~G5Q;+UNvS$?O>?wHICE!e?6pthQs^lH5#Fv79fWud7K&$tDb94XCA3p!;vl+V&zg~yUWbhvdVVAj3bhO1UozX22-48c6@2?a-(ffZzuYHl>?VvW0<;k?hWkG7MyOc!`k-!;Pec_V1PC|4b5l^|<<&@14M|*V>fIGkvg<Cvj)v~&pIQcB#S%(C|kL`HdWHjC&nqV+%kJ_DTTLd^87^B!_JSziciQ(|#a-_UDkIo)U(kRG>jx{9(nOi57N;OAUpLTDfbV5unD$HOdv3$!_ij<pyqA+0Pw&Uc2nVNei>G9$zg;pw@w6OvxVQ9n@%6hC`ZdTDG8pQ-(k3j)vc1Kzd;t1zN1sMK?85)fiJA&zr$#q`33QSRl{fqX2i6COGH8Kc1Ha^SUpm8&$$A@P!ldEB<Bd~voOq<hIf$3mlxiV^4$nRN{i&T6IrZZbew0xjiCj!E|KOpGAc<R)rlL5{_Bp}BR;5WS;ZCKJV?J$xymH|t<m;F6hRvs>aTnJ9K`vkmYGOCG?&w*z5o~FNs_d#d#0Qx_Vw3ZFSB4x{$R}h&qSY`!3D9RhM6cBbp4C9b+ttTQ_542hcy;u@(BEgtf&%yEYv;F8m7E*x${tq}8n=oZ8|C~?i+gkb*iVK(w{2kb=I!Uk4Fo$&u8OX}6sWR0n$8irS^Ud!C;{iE-Ik#NOCM}8GW+ciDOLR{DG#0Z*KL>PJflDcS`1EF70pm?*Y)}YaN^08l?35CApx}%4JlGiouaDc;#S)JK0?r3OcL7qtIC3-k2LY*!0Nuuoh7z0S>^))i`+!BBD=l#0_*>6fBK`avAG25mhVYA6w`8tj92z10<!$lcV1}9;Aw>sf$x63|_=k*335LY@<C?b__PCIsKNPU;ISf+90-eLms7+ro3PAS$E8rB6s1kaff?VK~igQ_c_xAeFj|odS;LgyEkB2sr&1Yw5-9JnWb)wfJ$O>{T7`iE<nU^}6p;3w-V)y6qKOdh`l;HUiZZIi-O2Zk_SzW$X^)mnz=;W6)p&O6vN_UAXA6-d`9EtoDs?N$Y(sZSjN{Iwg8Ly&Gw4Mo3V2uu>g$DJJml^}lP}L0(Wtj-Bl5A88(Qk(itj{vpCe;F*ZY6Lzp%f3-n*|B5P&5S-FYz?<Gtu8?B+DF<rg%sh0^DGiv?ZO#LF%hKoq9S(0@@(TMl0V)A#(Jq&9S-_0@{vr99Ya?#vRavJM&`Xgv0t-;KtD=_8@E3ml0!^Bd{f1$I=J}+#6sc&m%0#AW}XXOjr_P5fL=XwI9AKgt8NvC5%7X3ZZI?Qy`N9cA;geX&*{?WyLHh0$0^U=z8t1Vok%i)ubXVy(XG;MM{jemZ8>yJc%zDVKN@@<VTasQBRdMKwAJ?0Q_I2MMk~O;~}*Df^{BQM%_kh)RT||P>O)K;jatT-<9@DK!nc|mN@IsJ^ynePoxSZ#$BrFq{6;+Q*FnBfS2j!M8JvyKZ_#ACBI?Hu}(QpOC4xf+)PA<DCB;Sq{u``NZi@Nh7}+zZ+_8AdHpm~E+PJEnxF-~MD*1fr#Rv;tM@?ph0*@X?Gbmgl&)wC&acV{0(r`NQ8yC>nsP!o!%w$7Dd}Y@$XWws@_dBNVh9>Bd0176f+Q5-31iwNT=5`8os?3t5s{=|PrBqNiZ~|1JLF=3_L<cS<qN@jjDil=4={et>S)T5Zj^~MlY$itSm55^mUW^-5mP9N*r;wIIk9@Ap&5*?Dmu_$?PQLKkr#T&Ct#J4cBKuUc~y9!lK==if#Yi$;zUdc(oq{3yC;Rl@mVh+@TjuzF_tfeJz>bs_%ht0)gpL?(tuqA-f0dUL*1^cm*g44<KS6FeLWpvw3u(BQeWr`-Rdu`Q@(kSu5-d0jL*3X`yE6Bw=1K1ECDe%n(>UV+2gHN@o+Q|?Eyi$4rk_&ESA=KqK!AiNGwCa&~tVJMZ+HmP8scKu2S*9B=1yaBsZtQ$4jijrS^&U5o}+)d;^CC*3{^(qTx;kPl<(;XdyO9M&lAJ6vrC)g;io4JC0N_asW@9<B5UTTwn3!`<bAjpV%NYbXIR{U*zD&qp^!bl=tN~OfnRKiRDO6_vSum>{gn}NCyLpM;oT2rnu1<Fy>WrNM^L&f#gEw=kiJ>R2AH@r`SXg+6iq4<P+%V&Jc7u6F64IK~FMF<)RV>k%`Cnl*8+@go|+eP>jX2Db9|NKQ1dU%90a@nAW^FJUUi{<CS4I&!#k)Wg6LWCWs4@DBkC^4;i9xO56bS^SC*!^mXC`G}PEHGGf4i3O`#JN=*V4_I^x_7(nOJ<XDipnqF|&cIADe;zr)G4z6AR$e9$P3?T+OU2+R)a$8-y6$gqH8n?34;35@xz#c3S%hHKfk03M*oSeT_Cwe>3SsnZ`cQ0NFkHkx6SLYZx1RioyV7CzZNGHIZHGw`re=pj!j>Nl>ahVatAPj%qp`HCxPPX45TU<H9dO-NF3APb5{4U`^VCA9&Ao0xfwbG!|(hl(mvO+0tucPJOOp2^$p|DyVd_>nFw1lk$6|8YwMjX&|RmoZGa$3x82tou4iGEZ4Wjx?m)C`E=8pOjK8pyyFCB?uQ;uk=jLTMw?u<J`AhAlAV=u?(1g(^hRIDfa*T_i<lb8EnUuqe-=fEU~6QVIeXo+wr^UE=Z%LGx)c6yf-2m9Bl7yKIs9YED@vXl6f#59%Fw7AJ|<5&TMLSgzlwR4?VIK>P-{cJW76zN<b5`x+=uSmfy-$R3QU=N#Gu#^a<NlIz5XgX53Uf<peuRT=~$>4X|U?H_B1oz(~KzUpc4g0jx6g(mAsa@CGDl0p_Y<m!hXz$M7_8klFjmq3#bj`(NVvj^Rv6}xU`IwK-uR*B<efH>#GWjrOp4kn8PTOAZ(nl(j9tI8xf7sCgWZ2}1{Ua-rQA{_gvN}<%dv6CtRV&#J6Nj!y`il#6%_=@uO3}~eYnn)|IGPr6BP_H$RD-v4(eZ<P*gKdz^H+8O)RG(xk`fCm=EJ+p)C6$_n;^-vwmPgPPC$&RS?^vOxr(TX@{jOpGw)<CTBgjfCc*Z@$7o~z>JV)7(Q{Ws>*p|VgiWMd3F7K2D<{6wJxH5AZp`!X97!KgspvIjcoXM^p09v2;0!E)%f=1z3u>jt4m1XOf!`#SIH+xAAFG2EXN^@jZtnh`F?kU(}FR}^8rx$>MiZhFuX~fyzUxpO#oDPS%1wgyT0pQAUV2vw%Rt^Q&!kY{TYqq0B&~SPWj>qvsM}H=`2YoLDN&9*$Y3Epg8Z12v!~_S3On9<TToVdoxdch=0)5E+8z$3P(t){d$ATD&pU{J9wUdQQ9uO*VIQL^zgJxuT>6$z|-hp-!pV#Bc^wD4XN{D#>HcO?OSdd@T-SqdzYF)FZgacJ-Z$c`%MX#AW`Kks;>qX{t2aZ7@kDZ{qKL-M_lp*P>QgWGFOHiVls?@&<SeaffflNjK{w$XK2T5ircAn@JAO~CJA*6sY(8vd#2nFI^6yZ()1J=uN7y$996%2rgaRdu3C<3LEyDHP|Ixw&n1^`EL&@&R?kw?sInNxZ|#_x8{ICN&kSx6q|=P?j$WGDkx?7X)Ra}x$g7PC2sIAKJ(1y5P|LiW8raha~dlvd4`mq5rqWSm0at-vfB(zDZ~A>jh_;_+??w*86FMhfUJ1XHjJ!YELPom)u5^9pj-U4vKeB#9vk)Xib5@B;!g5_7Hw5$I@~kb;43H2hLkCsI;Ya83_GHli^C8IT4>BYjj2l%aqvgtd0By4eKJXXTOv0!7wn)S;1NH{Ni|<@CQeKnx+j3diis87U%N-9!%+P~mJh|M5nIEM60wXr6!YL7Pruf=>j&N~lV-aEmW#M8ujY`8_vtRh|a#tU|YgK+Dqy#ibRsN(wa*S33DeQ2V}?LvE2GDC$03=uV&~3)~P{GsD|`l*cU?W3&>9RS6VTfC@@`=@m4o$Tc?Y1^`V_qW~PDb?|<?Ie{{^Z1|a5OgmN}0S97LvLdRhU!l=16!ny{Up|v05r8TI=~*keCVE*rN&&z|dj&lrC@BU>gh6CqeADQ<Ql<gK6q8C3p>E@GT*w#pu?%33oPGTz6vSeDcZkMQ`n%3O2$uQHbStaS$%TKG0w(-#=p4{&xJj27f?KS5eA;CV=mj141u-B6*rw5uOXq?qTR)<>nvCxN6dd{lZcOYWY&2iU&VgHq0Ke;@Y{0I9nMs2%g5m)l#Pa1<Q8kS}^53vnZe6jCOLe9<w<FvN#oSW=?-g*=plZ&tKz$6rp=a2&9h~dftWL2|D>~o+moN~<v;h7f#E4O<1={BU4_1Lm7(+nmOO{C=awXLv=<+MkZ3*hI^(2M}yub-Jc_>LEyVCh0s6vvp%((q3x6VS13H)Yq^R22^6fjek5fK!E8AwVe0WGWU!^bvD?y^{{*5bpPEbc2oS_4@KOcu@XG;G&F2MV8p0!Z2@HH>-x6iwuaoL!*k$d4c@IKT$b|F9KJ)a0@_16Yi9#pjSH(AwFcr7gsI#9=A%?KUYGfCEE4lNPp<G8>Aft@<0)Ouafu<oeAef&m$#gG7R4-eQC8o`2=u1k~T;Y-lEw)le9P^J8s+kecA=<MvBd$iw=uV;~3Md8*I`!61wt4a*hUr!isKwz0s_4iu9G)JaGuJM@7Syucr}I9h>>A`4w4wzH!oe39#L)}vz+Qg{=7fB`Tgnz$%%PMgzuck}M@?&e|93d~@Fy4pw#@WJTcmQVqHj|;t+Qvw(14G=T(Tat=W=#ff#F`@shx#0lkwfpe<B-}7?tjd$#k}em?_R%d45;s`f3Fv889K{;!jostHqAK_|Wv~phI$zM$q)TiRo0U7*N2KOt+aGnOk`Q!K><WVH4xD;xdlPlrezlC;AkpT+oy{ReP0_4i*DE3k3O$AGQYeI1DTm^&9T1nj0|uA510<bzt83O?2BKB)MjMueCBj03Rp6VapwjLW%c4{k-4h-#%ncTu2G%WWAe9%=AmtDVA$1%})z`#GIvpz73}Y>zNcGa5I`AYaLll7Q>@pp~P!?ezAC4D6fZvH?qbef`NCF%Q;n{CRgT?fHb!${;eK$1b7GtqzCqM$%RirSL-4phc(}=i)hGkSWV_@Bd)I_Hg&0&C|eh@eWP#rvT!=XY(LByN&q#(+UrE&fWA2&K1B*kFT1#krXywAGwTigjXSeeo|M1Z2u3GOa181EJ`jp-osF4H=PsOT8QpHLsukajrFN$zy1@tP_=uN*t0JM?uK;q_m@XqcE?*(4LX1A`=F`gSH4X4)a3bvZPPS0TrU3Ufk`p*KH+F`L+-?SF&!`*nSLiHUp#kB3m)`skYSew!to2Jj*+tlY<?lxgrjGm$H(9bKI@(d>ia&KMJ5b}V1$2J%i#w<tW~)l)t(p^t!)i&V)p^Bip@)Qv;La-~^=bUkw-XN@L<9YrQuDpCXr)<k`KN`aU}SpB`(c}kR9THQH|ijtsds%+4sCb^^n>pVt*LXdko>fKYCTGdE;ZfIClm@}pjAUc(r<BIDLu_v&M3vGh8pdh8h;GqU}#DERL%{LJA50yeZsoOhjul8qqX<&E!J`wV$`Mf?kqzb7Lv3;4Xf}W0YJ7X7<oj|wu;&A9%h30XcYQYC@PLd7$`Ce`K<q)k-8u0Gz_9dKW)Rz+LxyU9m7Wnl+o}b)2tnMZI`Js+>j<iO{zcR9r9RjkeygY@-bu^k)XT$6LK`XR|Nn+sDkX|LJs68-OJ^Sr*K9roYYXzco<POygLNm+Md0peJ$_PfUb)x2uekwc+O&LR_tR_IP>3zbY*GRj%V{WfBi&*c_juu|1?C~5J6{ZA$$$k}Zu}j^{;_6yK0$$<x2g{nje*44jUw?6Xk2|mgoZn@YE0A_3RH(gK@FF@|UB)_4z(A{dQSg2S_k+5<xdXy4>KsI%49;krPNhAiwZJy5nEDM!L$`lW7%FQ3Qz31DmCQIg<u<i&Iq@(cj>Me9JU2?o7y618)ELOSh6Rc&=$dM$IESbd$Ic%A1Wby7_9FRDIv@(vcw`FEVzi6M04Is|n35^pYNrve$cP4zH3~_Yh~c*vk$Kndh_RQHp&Z=8*gJZ;sNl~N2RSmi*i$71ly0eHq#(GC2nK2P6`466(vjDF_ezFM4gj#6+S_<cn|L9b**Y#KT5W<1v2y_gZZ9G`@AsBl5C)NV4LtuO@`6>AgEhUSR6Xz&_h&o7P4M)joIqEwWVzOEx`ln>z-j^FMar@`1H6?fONmtz64-XA?Bv!`zKW`!*#%`T94=A$^t0HI!7)CEM91vTr4~J84GfbmLx=`JB$|v2u{fM|7|Gf+BxLIv55);FC%0*(WQ@~ha7dc?AWof#SB3Cgod&klR5aowoi-pLQilPjHc<{Kk)nX!S01!dDBmYW<UqQ6;IGy|^x^NAm>fP$rg*4QjKL3QpmaPZb`>lx1W=lrZTfj1FVd;j=^o{N3At}Mlgy#w8-+Q@o_I5n2Akc1vJEVW+Z#`^Y#Go1djkSe9CjlLyIBHt&JiDF^x7YhVm%q8T8D}l_5#q!I5`K`&q<=Pc?B{87^Cq__%wic5Risxta8f{Pay4l`Ggv;a+HuwY`Bb>S1>wGR17Taksf-3Hi<eC@lk*i@V{rx#BTJ>dDM^!MBT=RJ?a2Z^4e2fh2rkaN{g&!)@$|pOsg#}6Yc51qAsaS=#w|t1M*4XY0YU?GJVR(E4sB1uWETDI9R@g83qm^AodtfdW^C~qWE@JvRVQX_%xe=!}=dE_BKA8bF6HCffZCDYQtD%Hlv;-G8og(8@0Jt3!b1>8(8FLT46$>nTUh7_^mfs6^%3ok*B1zS8jgKd@GI7u5%)65i9Kc;uB~p%-VvSAL3yb4oWxHe*?LACN0G8vUrZJ94rXW>rSL&FkXFLTZ4`(W+rg)drE*=_Kqd{Sv2mII~hl#ltWiY2Q#L<4J~?PJ;v)iBvC~~IpKB&x)2qJb=j)jV+Qdl20G>EAq;7Os<{ZzU-T}Rp5~y(xs5i?;nf{Ry-E#Wl~qXSMM(fG(M*X5cC|?1iAkU)8B0Q+QXl4}$vDn0PB=nn;d@jz>=yt6tlXznN|9IdcL*wnZdqW<LQNzJE)UDo5FXcvV8W>xWSX+G8-s=gQribzB^>2-@kP$ljfQzl;O9WhQnp4_fYLge_6_!-U_?2<Zp-!1G*2K(oW=pD#%BphMG6$~064f&S~fZbo)12n#M~pKf#ll(trhBbCJs4pbwKW#MSwBXO*mH>!;+4#;e=qlLq_)dCW0_hhykED^%)*uQUylViqHU9a-&nO*>}V<#)Lj@HNVcM%QLmxdBhJWu3!X!{AZo+JouoK&eX1TLN@2*eK=EUlhD{e#$5H#HXth`d%h5d=`<>pnbvhEB^nEByBob_4jVY}#vq(35?(YLK?>MAvf_O>D}aM>CRKC)Gi)KG`FpS>ffq))he$xC&VM-*349{b1(Cg)Pl$jGbF!x_S3t2CG7XYPsEarWqH3LJImE=nVNPk799aPmFB^*u{AC3ALRdu$Zn#PYO-1O@brt+{Ruu0e$;bt~Q0FvVHW`N^wP{6yE@miQbxSN#oYp2>rWRMKJDU3c#@wbFW5qrBFk}H<YvIhqfeO%-1@XwiXa#GtPfX)3jku&|#=uwwB`fbpOA;RZ&CRvN5CjsiM69s@3QX|yUrf3bMwQZ9UdAuVVIjs`7Bpp(Q;gkFmaob;Ua@(8yP4I#aYZxRx%8OxH&S^TdW`7OG0K%W9-SA-9*s3mAuJhD)miM3IJtp}5$_Q)N1+GFgzge&=ha{c-0C_Z)rdlK?IckBt{db6)Y@v)leLT;L|_gyVVQ!c<quh77z%NWbA1XmeB@wK{KCA@L^TE&IE8d9puh<6`+KSgg@vZlO3Mu6NGo7(LOMyw98_{)f(*9i)X{TK^1e4e@4VA#Wr_#0{&5)<V)g2bRgm;n5vHCZ$t8Mk59tepH<Zl7Kxi^0f<Vs#Dxz}4=@p-UT;T|fR-8af&+1T>@Y8A<0$J*W{Q&)g1^>l9IJpnt<v5xEAU{V1bW(N8+3W?7Lb_uqf#-}kpHCJ}3P%b?goS7}r-k=#hO4i1L<T7Apv;Ha7luwUJ*t;ctcA>06z3~9i%?0jxrZZ6EU7d?BvOL>QO+q@{*xm5<7NUh^i8~}1sI}@V3uDcy^sjt^aVP=>`=IW0-Olg5BSIB_Ae9R9~rE8h=KE@DOr6GqcN6ZCDt8g0CfU8ouv#|^CSGq3Wo>~5<P6iyOPEF<=NU5wH=2+iU#U_!+?R3P*tGK#A$JI?97B)t$y9+n6ib2n~xPqzsV_n;3uR?)2ob7Rct;C<oY@>5J0pjj09NSIQWLCpmo+>`Gp8HsjOo(LZ6u{eLl&NG9Az?O{S1mRI08?f^o^P3<(00=AlAtl~+ADoZaQYATl>FKy~ZYY9N&1T+A*;a4-8UkugiO!UyZ_RZ4W|(po9h<Pm*LDpQsNOv=~mjuSv%%$6*?@zfHp=3K@KZV}g1_f7K!o_2~ch!);OJ_u$*GvH*$1NK0HNXTUlqKonmL@fd$8viPDN>DGYW^X73uha|3ln*4-U<aVi>VkwE#vmXOt+|i<n|K&etAiW~%C2S3#DAz3Y$|=|@%eW*?=J6dE)M^qE$3OP!WbUpfuJVhRVomJyaI(XoP$izL%)hmPkQt8@&_~GW>Pk$89(8Nvl|=7V?b)kfT<~!nQ7ugr!Qmo(Ny3GyK#wM+zL-p=`4_%B=R}Qb|AAy&&z;>ZzJx^7fEdGdg&Wz#ms}nehwSMnvrkI3nB0!=Hcrx0c=Eb(JO+r{Tb#VsbY=HRo7G@-!W#xiotGu;!(pG*3D0`bvFbE>MDRRTuI88EA=_Ya+^iikg&w1)N3n5lB`Z7pCb|D;TR=%iYS2@wFI*#qQJ;0KuJmp-Qwv9@F&+yh3jdt;#<2(qy=aw42FI(xpk5W!^!90!h=b<3aMc-OKs367S)QRjFjj&V!>~LClCAj%4=(vq#!{|(or+mv>zX8LnTpVKUT*zKnyF(pbgq!%Iw3&wDU>Iw>*t522H%H%7J5P;}hO_2JTA<e&DsrNAQEAu$n#=88c|FJhbo#S8Zo-!i2Iapt;vAO(onk^7qW3WSzB#F~aMf24P_ly$B1E-+qa<!~jYjMpm*`MDxivUQLJW%Yw)-c5#Q}E!mAV3`E7h+S%A4U8z{fIudRRBzdF}BqS?zHX@P-IXXz0S8v7+$@qH?Y)-Z%SWA)@Q_P+5ThXwyVD#Os3|dm_pSivQ$h0t7z_a7{P#%SkWg6olRLM?0PUPKqRW;N3KQ#XZ`7TPZ(H7#<GDy@&$pLO^($?`(*~D#(Wgg@VImuPQ)UXdU@uv?w3c}H5LNfsou~Tdzc#0^n(N2O%NdoU?brt5egZ-Gtf}x331`D!*Be}>^BA+c|MYO?YFuZ}&W4KtOPe=1OipK$TA%?pgkw=q2+Qp_h*iEbmxB8Gog@VG0dJ9*z%PGd)VkuST226#8T|mUHc=XG~U?+KBho3NKphU%&Bto5%cak+HZI7ehgO}cceHNR(uX)-oHyzzF=iG-Q+!+W%Z+mR*zl)8_zl!pz7VQalm!FkLlU5;p#oQT*HMres&cvi4WQV~4%bz|ajRp`pO(?_~Zy#}Hc%@}h*gqd<=g^4VkRd~rrV`EsGD1LVSi@J!qZya#=(a+!VVTn`%T+_!N|GK&Dp)Csrft=U)kPX}R$}Tc?R0R!#3WWHCUI^MMn`P8zF?G@aHh7!?Ao`kP9~(^RY^dlYT?y9U@fDq)Cfwk_w&x%ZhKzJI=(Wf&gloIVD8?Tl$m^)nITO*Ip)FiUjC~=J_V2D1^S{8B#zaM5h|j3vM?bTK7+^X<+B2{#Bqbj(&htdyw|*7%84*(#Z-H84WVEP-lYj);fRzDG%T>yK#{9{O#(<_@XDUvq3xv8!Q5|a6WR(lgC|m*-EdsP%u)OlOL)NlrNpMaXbqxtgd3NTh~wa$Vx=a;HqK=;a@|HznYhFG@DdNZHLSN!m!TjWY+n3ggnkv5p%?_+AM00F3pCku)`=X@N=Jh2-%Y$>8ui49ZHfyw)H*O%p}%EkqZ&@tFuNF5i80XD`<P8{Pn`}xvAd^3jPF<kDYd(n4Z+veq>lpxN^IMz)1Q;l;rp3n$z0KdmQsaaBDrww99t&M3?%+_lE|Ul3AS7UHvqA^;8a&!A+<XEm$utnYc9b0j>%FC+Z(POT^UJ6XG{~=G<Des;}q)y?rTK^saw9JzA6b>dDo2Sf&%|OvJZ3^DcB}L1JejWOB@Sp;cQhBBhRNa)~!m@03*#*ejF_A>kSI0JbbK+?7*9<un{W@>_t!kn2dM<kiFOkcI_@9{2rJ{ch2)S?eaP;^TDYFvjE1L2IPcgu>^aY(Vk}T9rzAp|D9gLQr3|)trgZ``&^7E3j<YOlc0<_F+PF@+T6y!X<DB!&`h1&Htypn!o$iuaZ_7$?x1HvHH}w76K^mo_Gm^KmcBqwSj5g)se&sAQ`}k4F^Wg@5Q*I?nKP`WVj&u!4@=7{&w_@dojeF#W6N@hHO42{cX9UJf@JCU%Sedl)A*nF2TFyjXtf-+%SKZJz4=mIF-V=-0{G(PJc0XJVPW@4lR_TB=u}PRSOlb|%zb%}W_&6SmR`Anw1Arnj=t-JZ*97f9b&JHk{d&s)}bvWg1qlb{wND3g>to~l42Hd-(x>Nl5-=Z|5|1<>rvfzPimId3i&{(!zpo#k>SB5uxlBMDKlhqNNO`~Aew~Pi19fXza4|2w0fAphCY!8SnIf(Y1$Ee`K}ae@Nv=E*q!@OVikpXcd#|yz7PGC6X6cz&$|8R{|DCYetZ')))
_V10_EXECUTOR=make_agent({0:_V10_TAPE},dead_stock=False)
def v10_replay_agent(obs,configuration=None):
    return _V10_EXECUTOR(obs,configuration)
v10_replay_agent.telemetry=_V10_EXECUTOR.chassis.diagnostics
agent=v10_replay_agent
