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



import base64 as _b64,zlib as _zl,json as _js
_D=_js.loads(_zl.decompress(_b64.b85decode('c-q}v%Whm(lKd5eYcHfKik4<aQ)NrAWC|qJg&u<t473M581ziT_Ri>kA4w$Zz9KUs@|;_gd*w1k*1hMICo?iK@{g0>fBxq$zn%QYS3mvq$H{;F{Odn{`SsKPoV+`~zCOAA`m2+_|NOsy`~2^p{^uV*|N1|_{Qmj3PriNs*AM4EzJ7cD=H%nQTwLxy{^#k(U%LC3cUPA$-(TE(`ltP?-T9{v&kp}M{Mq%Z-R|AzKfL|d*I!NF;Pu51@83<oJARw%-J3V#huyu&tJhb%6X8=n7U^}regFE+%MTx??dJX6w+`<*9?S3zUw@_ieEcrxxA{CQC-%+x#V(rHpH6<fyt;XHH!b+%es_Iya;q&suocqfe)y&B?8WY$JG_DPT7~U4UW)Pa7b^^ZMBZre+{5or_RGT(&9+7G<NLFE_%bvJa232IdYJa{n_iqh41D-BEYHUm{_*p-zTLgK{1Ly{^=|ia_?54}+L&kS`ttpB!h?nB^e%7>@L8YE^JG@$2k_%RpWp1R=x+J$(+kE2c0NXUSjZzD)^YrZhsPdXGkRF3Nj|J;FwT)F7~TiY;PjD$Y3VVuOY^8a8yu|N`SM^L9(eb6;pC70dH%EF+q}HGd^dla(UZr^P?~(vvb1gM=t2_iNAxmBT8%BVH?yxk=DIw55x$4fuovdI_~__fe56D1Ctim8kHqXllRI9_VKDZ0UtGR<v%9$Y@ZIj}=JlJ`|2ZGbd|F~>T{2dw2U~H+hN+%AIg!yBjg<IVoBSW`xx|i`<chLeckb(vuRFLoi^&KaNH{We;g)XKX8xq$`yXy!Jgjg{B@beBRO0EtuU6Tp<HrSV=-p_|eJi+ZX!O~TNBasI5$8-S!HQ@<%-st3dOZ%c^p3;%968vIU6GzLeD@G2O7;Lw>)|WrpQ`ax!$a2nGH4D5V=>-H(z{Uu6>ZtkO|Lu%`mb|{K>jxDhs`#U{B6)m49kKd%Jy|1dx-7dHny?lZ3Mq=9cQWy8SUtRLDbHL%h2XVz~IPb%iW50o9lRFc;pbmlBNS82hd{!=#%J&7%rIP@Qq(DcpMI=mcdAM#o#6yo(XL{ei4E_1RldO)!-r`I4~1@8y#wVb$<1ie4a%2F2U{l&s*+h;k?Q+PKOv{b+@523ZFBYabwn`J2v=g2&~CdAVJ5YoeDtt>|r9VdVO<szW;W2b@f+$`cYUm-VuWZm`vOf+bN+5b9ZF!RVa(nG9xTdJ-ifz{n;dV?}E<jF#FJL9sYUrR)=-!{W5T3;M)+-y8TriT&>_uF!H$0tH7Wt^xoZYvDX{HllCYtf^6?Pp{;CPARgWxz0i+;uJA_lX%j+1d`QK-)!A)12ohZFBSt}NYWhY&GOk>Wi8KgJ!@wyrEyj&K1ES&K@WTB9;vo@Sk6bt*d}-qDfUm{zN3!wV@ME)p?Aa9tbBhqLfZia8UW&N|_M$;N3SFT%1va??M~`fB1IQ&w<952%t=|3cE+7Vji_Ky%DfXNAhRY~xp7bb%SdcrTPd$kAnjq}aR}aIRSfEjK!}p;(&6!(1ehTy%+cE*NGg?P6@`s_Yu`<P85-EDJHm7;6Mtzp%Suf)={i*PZ5+CbjQ^Myq&{)XhTEdm(0y2O8dEWp<$UdYFtP!+SEOF*ogG;)Fx?`sw`o(G$|5^x38h)iM9$@4WD_~*aL19a0+iLW<QQ$H+T5S#n{5m1!GW!eHW!9{nmg)=A4#LcqxhW=;g5a|RrZ(dvC6|;|AWgj+7}#Zqtj#y;mpr5|3u$B^Vy)!rNx}z_mC*XS#7%70hbt&w6t5zMvVog?IKOsla=_69YtM!=JPakTg+eop&#e>d()?OdX%nIGWojIr{9%F&+tr$bz!~j1(e)VF5MsL31z0JMhf<xZQVyNT7jOHFm(M~To3gkq^7hT3CQooMzr6=xf(K3H(UKW~XpZExb$L4Xv*8Bl5SXkKq70`PMj|m$u(CrA$9QB{gF)*=x59=IQyM6rW5?L&U?S5Q4LIek^(?$VMwYKr7xa0-1Bngt`b;PIGI*P8#L&J&j)KLlITASE$ztSJ3`k?ofK4SQtOn&H+loBGXvYV21mVxK?J%=))ww3Y14&`bj_^vUQ237c0D(^npMRx1Xi#Xyay;af%kGNAu@dr7{gY4i0uVp<R4)%HB=n9`9o6(GR!!V@4#DQ=6`E+;LBNK8BQqEfJw2>h)OhtJ-wv)>NS+BI1MyV~J~%2gLI8g@o!gWUB){7zsdst#26Oaya5d0*2Nwf<Vk|KGT_1MsM}z#*ujoRGKNvffIftFRN@Pl{cNqO}SR9Q9Cr^4TGbW>3BrP#ofqY{HDr4b29sR?ql`<7-CfcHK@$kna6l-5SQ710o2Xa&ee+3Ety>%l)w)b<M(|`avTus8P%J=a6YYao=4w%I0gXs}a6t=BdtlV)}&_xGXA+#6KZI^%Ik{QR^zp2&2hj6sS=L>y0dC!LbV3qOqKFjEpf}O6et7EmhGp4%`s{J)o&p~1di;5g9sY)aOQLRz?mR{TfkGqM<{14~b+P1ruEwr~aakN2-AmfN^B{+;!SM!~Qs}=k0Tu&vk!`_6r7li5P<|Jju;sz6erGS70Iml9SMhBr_>VbzlSv5!FyRihmllIqU%T4wtw`n`D){8+aB&79k5wka^87z3(uACOZTH()KnU2PEEJU;eWD~&>7Ky-l*G4r(2zM!oZc{~rus2~v-so}A_h=x(97c`GwKT#(H-HExpa_(U^8b>YhL)Ihb`ad-q3Rp-5gX5DPG-;7I)fStG>PF69L7rv6Qh7f%=fD@p%x0)Fjpu`H_QaS;h9iNBTpjNXwhmh*kT@mA;G*#Pmat=@^>g5CzO+?njB1{0WPHB2~^uQjeh-PO{%*~G3+j#2#u2KQxme<>NaUFd7{_U4!5}kM_X<faht`ng@Bqe4IAYDjv512X%+|j`1bXiAMSIn$_4Mz<^(oGshD*1+OaGV7ZbK`2|_JtU=1^39W+r?4H1`;HId4lN&pnPVwa2=;41YFdRNd@OfCN^l><D92{WF0+>x&H<On5H7g99n$O(_C*~ttymeE2Fz<^gOgbKQqWJ#TYK=J+M<@F9i{z)ekzVSw3C5kwPnVLR7>nNr8Epk318yw;<Q5iF0eKNjB$No5k(T_?G5$-@5{8)4`_ibT5E1LB?Uc<#DvvRE7S;%H4saitS8$p3f#BRF(A<HI|mZm#KIp#N)Z_jTo8OLq>_goCyV$87iRkf%YNem2w(6%Dt=n3nUzP#3SMdU~<TSzvQ{xEziXf>!*-azl6X7p-QzXuz^H!tnBWsybNNHFzLLjx0J=jT>5n2eoF-4x7e{SpgIXSNZ&Byy0zSo4NvX=JhygKN6ga(3B;iP)J~9<MS+VJIu5ByeXxg}x&26cEZtcw7yl(0Ctb!f~Ocwz&(BS^yM4G_=~MsLRI6L1>C1YWTdpEtCXRqDcWz^Gdb7GnW?<<?Q4sD5bSRQL}}lge0YvoaO&0;D@InfTIo*lv<<^>8V`|6wZj`X~SF*Eo0+=fvD*#QFPUmEa_G~Z-hR0Sfs>>3bU`VFnP!EXaNFmOu>4P+?ZVo)Sn*03qjGWgf<js+!X{xS~ZBB3h_5Yt>HR&r2s34h~P6&B(6}^qH-Q~^d$>e3I*0{or@;4HaN}}zm6!t+ml_zDil6U?|t491qzcKH<7hm)<*gXI;8L-M)E)Nv(d_aZ!b=s?0&D53($cg|AgG`b-FrCd5P5hUT97YZloT$uM=){?=S`L5ZrPkWT1hjLYKFxjZ`Cdhut6EEQ&UtClN&}4(FR}L@*+p_wWa^?=NCaErw4tYf9rb2>(yM>G?4ssC`Lo#{KzT=~<e1E+yU<LaXxO<_Z{5_#ZV+rGLohxn5C+GUs{ABMWPUJ{*i6h5;3u3Gd3vnYm~ST6WYe6mgCSsc380pu+hSd#g^DHfSU?U;CcbA;AHFzIG(6R87$5l$S!y34(NaIFC9uNZs&;{kWJenYpInxjCjyYS>`nC0O?ndm=D_`Fw`sz9+eydC(y*`lyTZA`TVFff8G!p3~)IIQ&J{^#rUX1p7GztB}*~|6eex22&1>n^R8V;E)yzv~GMS=|K6z3O~)+LY@)GnV}&}4%-4mpgV^S%N$ZkcFRm7ptHc&kyltxM-NZe9BxA9<TyMe4#VPTD~x;z(G=T|0N>^MM;6u7mPE<>%95s`3WI^z65$CPeC)uJIox7P^)3pT?nGH4t}PC|;^Ul>NE`?4+Q1JV-FDM|n9pO<k~n~Y(baVHgOO8bJ-9I@)7^c^Jv%trcA@nqN<2l(EvncRiExbbM9x!2C&&ggB3V29YX<1jzPbcsRP`H2e@#2};*~sgx3)eA@|(ENRQ`)_`&aCrIBedIZDP^zvQuf*U0Do)0o@Myo$++imX$3{lTIa=coq_1%x1fOMXidgMuaZ?=iBu6W7oZ%+Gz|O1y!iV3;{~Srnk@3R;fNNFiOy{a#3Y3>ZA1!z4#?A=F`x?X}`;eqxq+L^Q96+m|R?FrO~J09(Ji!@Z_K?BLZL7USv_IB5#g@CQyL{;zPuuO_JbT%GGtLzim+5V<psRYM`-&KWxjmGf`YCf5D0^vC<q00q?*|noOu4NmVY#mr{~VYOixgucCQjLk92j3O)n0DI7EF=9N$t;|x94$;vM))@zycg0K{(V_e0Ks;M#H=Y&mBu{OP}#-4?n@bxLK;9wBN6?O3fHMVDzGZs82U*D5P7DxY?nhE%I_`V!9wOF^VT_GpmrvxjVH`cX}Xi6tHSsGzwXf)V*0F_;d!Wa!9-&O2>6EH3maP%bGqp?7=FF?RUi7ca(+iE({u!w1zpt6A2ToUH17QfYKs2pFcRoIt>)ih4Y`skup6+Lymn~}v+wfeNC%C!+8#-<{Lxs2g9#N(i>bVD4@X|5KtE2K@zjRw)60}5x5nT>7}vGTgoj=2}Yh}gV<>pQ!}IH`@Vp;>;FH{)!e`XXN^?@Qg(8glLr=#<?Z<57|!HpAWcdZfpPsB1=V4bEDn6erFxmSoRqG#PRd8$wu!olTcMVQ`RbwnD!MCxtUx9~Xs}Hijd-ib3_R%9WX)olsgEbRKyO1`%c`{ut0@=IHukkqr$wFT~Adem`@f7oN!rKjsb`3tsahnNkgb(Fn$8PIgCVE+$86!NJSXtX$jK;%^<JtD}<~flj*G$+G#>rl>TF$KYZFmm5oo%{Fw8h&M=zMrdTL#1{n#9HVVQ!T{itxJT4x;w+ZL$xLvRl@MmEPMmw(@NZgL9prVR^o%mk4(?90*E%@Q4#dP&%{0Zwe%b&`mXXB+R(f*IgLwMnwmX+E1KXZFPW|_Kq%%g_i~fqBFHa|PIGtHzE^;1U{;6Eu)IO=3Hu_%viO|cT%d$cPpCgj=B>y`nbxOs@dCE8dDQPCpN$$rh-^SKMmvh$FB)K;`EN>e(C<oKy%r=U@*F7Szmb==CB*6qK_)}MET;zjGFsj~{)rSOR#$0d{K<*;tOE5u*)q+CCs*@|ArH}9!QFwV3I$ebInRc7vRrSb(9A8_TJsFvsDT9)IqbW3)>(R@_|KrIh+Awa<@;Rx(DkV>3^<hFYx1)kdjN!<{Mzxk@t1>skUCf!#gnz7NO&fykO#atDI80^^?a)<-RL1Lt*_9Y+PjT*tv2{hoWI=Iq-tnJD3Ew8@GLrQQr`2dP#R!_Ngeiep8Q>S&>BwablDi1ajjq+*_upf0lwB~Y*os7{&XWNQSKHpU^_D$szbTkD`|+wc8lqwu?6ob3<bz+zol2wWB?Qr&Aya}AYO{-VmG(V~_Bbgm`neYJB~a~ITccQ{suaok=iyI-#$Htt5XON!O`tCZBb*I^FgUgH)MHHTbc{tu8p34J!ZEDCEH#>+g4qehd>yH61YLnnw2@Jl-n5XCb7+MKIEAMpj&NBAt%i+6SYo`AwW<gNdq3x1(S)nvG>vnsY`8_&1bWiBAb!C{xD|8v@wqWWc?_&}NHOZw)e4d1%+#WNlb`3ZFpQeASh;zf%1emH3!Z=On|gswT$%3h2P0N+v{WUvu3|l6zgCu1JG)q!6yG!OW^L!al6?uq14#}s?t+0}sHERi$07M#PKRs8Q)u~}FuOeES|rwZm~OWa2_jOo{rP9%Xp~npOGw?;Yjw~~akiR~wycSnioZdn(OmJ*;Ii=yq}pYYos?SBn><<Q$YtdjxjWzQnRviu+e;GxVg_d=5xsl3tA8PD0+nH5(8B;G2+K1a3gkpR@Xf3*Rq)5BnmT(csOaS3QCx`hvU-ukdZ>brAa4?pxoQ<*A#Td*!y28rOq>lTU}ELuKICW=?%`PH^P%CI6h2v3Dj>&s%n`ACH|O$cq~<OfZiFW5@PO)_ycv>}_eo+NP_$-<xX_E|XCEBqn^F0^u=ch_pnKSO&mF*pr;*{RjrU;We={7$Daa#t<i=&g^vs^HMqXyUykOLe=@LeBkfP*zuVl>r<*zN_e@upqOADD@tjy$&lw;sZLwf%benQar=6B%;wTY~in1?VlRf`BwZ&H~6-MP^8;*JSsTOiYQ?Jlqr-Bzc`rwGm$4xwhfa{nRzLpTNVPvo>YJ5FK0Wt%Q4h!4P;Xsl~i6jGZ=tVB(+OZI`t9>Z@hRZGyB$@XU3$<V4(bMB}xEMz4@%4x$XVMWtU)PrUIh;yXgw@H&YOr_mfw0pRBxMV;E80LV<rjbK9O|d;aCOXKtgS;Jtq>bm7-OBgKHsf77waqrl8>S@(a8OY4mZ2{q7c*v4pr4gNPZUY<?y4SvKPdK(*o1{z%VJMXL!2y^@-C~Cq2h9FbdgcCWT|>pE#s4*-Wct&P6)7fL=6?%+p1C;MM-_cb9M@~rSr%*%<;yBnvJv*x|;(r6X3SCnuP6Onk|P&h$y(fa7G{C5E$VHj>IcjxW;`}qJz|jbV^F`S&5)2Qq?EUthT&DEI*=wMtE*bCDBAQ5-viqZ;~SKw`ghO@-v>ER>)a9LHSA|!;sn&rHdWcOO{Hhb^b}l{|nHdF>yB-al_FHPitBj3j=AYND@02t27CrM}ZqSc#$SWR?@LKGj^HRZGdr_v;;Z2&-{Z^s*0Ab%$V!BWU5Shp%)rjm$dYmn?ssavKkyh#y8VhRmN+!m!uB1rfnACTaKBr47Y&#R+x<sd+J3mQlo{@cGT_*(Lq+e>HvjbxP0HXol+<vWa532qhnn~`_`fe^7>Y{1lg&`4Jm@T(x1Z+6f#I2-{^><fJ|shuN`ryZ3R4(aDUXs(XL{6rPf%70a=}{Ax0>d14_la$Lr~vCL3#7?n)1WRN$rgv=P^px+H*qGarkUq>xBzGKRrA+vaphZBeZHcjv%a93cdw2~MO|oJ_8bMrkUZ2y$OOhu4BmQ!5uaI)rsq3oa}8+DY|!>*!c@EtB7?#1AQg+c@-Osy=4O7oxjvK2!-`aH_4#MuvxKJ6g(+SMx*kE=kC&)Q6z`BURmXsy{RGB&pxq8`2?`+RI+$3m0heG9Q%shfU&bq%bF2v5(7tb$J6D?u`CPf{pebvzKBh3}3U|Nu0|gHx12Eu!cdhQLsG^%W5+TQ-Px>rGy(XM)Beg`%1Du63c+Tkx^^tER+h<g>+;lfnwt_J+a2eELrB&rmhIPRDXIDIYX!NSf?4%yVk1Iad6g6f=pLrN-VyNiy88mN8KI0@F)-Hq&`BHa3bGdfH)c;TScmtISx9*zMWG@8eP`cE()<4^i7~&?h4ckyUuSJ=+qmM@_=Xq#mRE1L`Bg$E!%^=+=Ewd7K@d)31CAH%#2&#t-D1}x}RG_s)2)K+X*~kC+NtT#f)~VdbBt_88EAcUq+N3i6g9g=TpPH2^y@4(qNHdC5a_c^4zAtH2^MHRoThJ!)z4~p)o;LY`v@)>)HhvhRXo4yT>&MQV|f$;kS5<lDmUq&=MLDe1`4?7npbBGb^kJem%Deu>;Fh(GAl3+vf<0-(iUCSIoAuf>*p;gP~5e3^fz{L^QT|lBqS}u4H6_Yio7470+&6M!je7VJerEo9xZ3B|jlF^d~xh))^^dhrr&_%I0bhzc?5W;_*d{R)84cHWPf<L`0ausRhXQ-vLO>DT+sxJ|r0~TlsJ@tIzs!82iZ_2G++RB36Fi@UOSGZG5Df^q~g4?94u{ZNMEuv!LtXsmO5bRtC>1=n8s~+Fo`Wb}$By3#w1)-W0tg6{wU7880~Acm#ZE=!z|t3p~GVS2T2b2T8en!d%QE_HHGsxiG<Ars;<2kG3vPe(5NRYPm{SP~+M|uvKM|w4PO}LiPE2e*L{&R|!ozL%7#r@FMFm23+W6C-ToSc%)IowcOP=DLZ~x)D%380_sAATR2;c7m4FR1%b=85drAdlQ0QcO}sxu-p<QZ&`WkgRd*Amcg8arWYmq;J9_M`8V-28gi3_*xWqVLKt@AnApWY)hgD?W_1TCFhMkNET@W5?{b8m%>eTU;uM*O%TpM|VV!_VzBJg@8+-%D$lAcamT$h2RRQs~*ztIWBw<}6r3bU6qEsfn1uSqeqAN*_uNrkx1+)&vRohk@pWpf&h@{j@Afa=`)Lgsm_x4CUl!4-T-SCB|)YMwhX=`3t+|6S2olhw%+(v{p~QX?)hI=gc_Cs*7=q4TtUTXKv`PH!a0)C9oZ-d31sC=n&?4}m!6eCz~5dMPHZL&wdw5TT+kFVq{m({J_-kFKSdG}#VSutt*rzTlt=uY{nWasksv<ic`uaMmo>qrTSLH$hb?(sUkj<rPiO+@Y?jSoIK?80Y3D-pcR~5pM!2+ab0elUh?Ld@6ClxuFEuR`750<drU!IW2O~oS(>Cdg><Veow@sNHV%otR?`6Zu*BLOAxs!b<(Q`l@(VDu|&b^ik3B|ee{%`)B0BL(p)dYK62KinZrLV*cTx>mRy_Rg^4(_-mhBSn-$U&vH=YJU?3Z<dM1=`p-Z4sw9NLjS7oF}_Ih=pkM}?`#FmH?fTO7pFs!h{j+R&BJ@uG4AKcT(>afgBArK-W2Mk#hDylS9DXc_e8k|<}lxGADyq;8!6f&M%%NOr<nR|d|B`CR1b}g5~r10qBhwhHW0f8g+%e(-mA%av@JOWJD0Y}fi9Hy!zrnyPsG7<#TFjJ+W`KRmq-PPsG_ZK&l%YFOh>1ql<MvrdWGp4VDp$hoHv86XllAHxdOX$>N_0(`$i>jKOo#<~+InRSVXmz97vOBTFaqW{;`^zVn0g!@&-b0|XfRc}vZ<lGTO6gY4?&*H!z^kGS>vVcxp7DZvRrOlQ$rAbo=++{?eX0e&j9tQrLV_=CH%wJSCAHGPYbHvFuZTj4%$q&aBG=4mEXL3mOv@T;hML?SUNfk}cnaHHdS@4^ov8vm04D|ul=0{HMwSw{gOF#@3xaAyyO4Y&;az?U`V#V>cS0fXquDW*$-WBYz@ow;<Ci-cpHv8HpQpVXQ3`naY;&rth~@a;OadchQviA^Cm1v;oV1*Q*-_J%zEGf?P7viZn2+v|cWr4$kTj@EMN68_66>{f^;q6ZsPBNw5?gQLsX)bv@QFF5G-!c5QL)Z#qBPi4c~2ZmA$|Dn{QA0}dA8ij&lG@j^Ctv2b#QHy{@jyGsW;X-J2ndxLLZ7?VqWc+k#0A_bj;An@C0sdO9ej&m~;`je!rBZbQ=rOJ2i{3w|NrIEs|EvbV@zp;IA3KSRvBsXdj7N_;4|heo3ilL*%2I>KYA|txjif>8)tx3=uvA^Qvym`#+^>5F|TISBw%zok`7mZ@NCau2e6ONwX%%4TUdB@kI$2m8=L#!_zV~VfkaJg);Vwq&p9|O^WLHo#Cl?ePhRRl;qCQL0(yo?w5cVgJ5BVfoa4Ng(kyaABL7n#6~7gC*@fR_n_{lCBz1{7Z1m%Lf1`FxF~5=<~&Np<2PnTX_TxBKnRrZQvGzTD|9O$e>k4_)`H=<3vh4*wca#7Z!eW^|9tEMI}6#n#txgDw;8JU5aYyIsmN3l)hROC12X@@*{H<nA~BZUPdwipGVa~|pmMj%s)`VxG<oY#ohEnijj}SM@Fik%FdL?HB2be+oqC_KjBdVKc)<C(21R|$(<NeEhnxJgxwENoSrg8JuRoA_DTDs(*nK+~yi@$+jRmKF!6>xBHZ4<cC9&8-(OvUIl?k<oTI<SQR@&2V#GlV;vHV)^%$y~82po0_G)<ko_XUt=bHYV~qUM4P)~K}rAU=yn%XEoaJJ@e-P4Z~>%z&v#>{s!s%pd1iA}Eu<?s~+Kkrt@EdAjZ6N|IvnuwhSNfF!_Aq4EWryJ1wQt-6vT1DgR8cFo(%Ez5Q2c#wYVbhKh>c`(s1pVl^5%Z2qs!mI$t@a7uCGcWF1PM4LKv0|W;Te)Jt@z!SYaWrB{0$S>woCxRBg|*qSYs&@Pp2^b)U>@T^N{j@n>^h)8q1+#DU8&}In%h{aHy^`PM#ZrxaOWM^)yXf(FXW_NxH9ZHy5fHMXeEY6!CMTK^Z0&&`!`1^E5JW58W7MUCi{z9$*97c<Cbhq{H>a*D{oS@7x1t?GVYmls!;Snj;KPeEp!`aj;K*vfUL6|C{bchJkczvxNuINabhsr!d6j&V|^U8S--srl7Be0;99UBXhggD=CR?~x>Q~-{E<0t4&>7S;<DqMgCR{UJ_QtvKw5XkJL-3$unGlOf+A*K_F-eQ_!@N^^)|q9v3QG8>1V1PM0kh*yQ<7(X&d80?V13BTS7#jN;Trc(G!zqZ)_zcXsTe~(XSbUu;ZTMH+IY(>O;_ObvY|Xr&i_ZkiKA*P&lcIbveGi<W(Ot$ka<59nLlf!Q6O4wMhrJ_{BQKj!FQQQamvIjgwpVyE?k*cHD{9!?#$Lq)9ZNt$1~K-AetC5MPD2yddFHN>nKc3t2H-%mOtm9F;_`wNDyqJR6y2BtKu~N0ZWRn8auz9@<yAC*G?At6U+%?L8n7y_eMr9#EL0)lDF;(Z~I;FQ^-0*iTURA{1DN)q)C2+Nm2@g_OUS#Y!~9zj(V4(<5D<UM&Nsyzbkp0i7zOgp8?PF_L6Wp<u3hFu4aykLJ*GLOz6+2J`aDJOhB}3)n5J*g%aUx6>Iyau0$oGnd2d#=9LT9^2bTmVOY!qli^&w7()8@Huy@kyVShw1`#PPoKbPFTwHFUL;ywA6KQ+x<UaE?8}ILqS}Q?Ya?PFEHi3hq`qY4aswlzoG(IBMH~Mv==oNr&2~=`akjFWGu0y~^=FQ@=&ZCubn_4mIZuI%So7j2sH;(!nKcNiv%cLKcu$?&ni3p`gp2Bf3h9O;;sK@2=nAY_zOK0${MwL)%&TFnwq%RhZOqTO1tyS)%;RMJ@^t%28~BWv+e}<a^sO{l?M}26<f@B=lO_1hjSW$@T11$q?K&+&l!Q7GI>waNJV^9DxOZE&RL(4=ox><Wv5n!ESNs;Xk_ig90;>JX+X+E>Cu(bOak8Yl9wYkqKabH4gTxOw9{`?ZWLrms_en*KBA#MY9mud~f#0tK>{TJ&tWew|+8URN94!xZ=Uub}coK&9QkKf!yljZ=qVfB}YfG5+am)z2B9&meNjCwk+N{0H_{8Xf%&Niy={iHzU9&Mf+CDud!uoOLFLpDY_@7y5ciRJEmIZZPAxj~wE3skgW&JtP6?Q}MBt^NtR;5vrp&e^;ymMQ)&%+J!*K+}{N&vw+tH)7+tBf17j-XW6dJrrGR7$8go2@R&luFM#ij8IW6DPjHJ*R48IMANl7MigbtSbIis++*<-SH;s8cjyL{*2(95M1r9F<ucG8#W1ULrWrt2VMCz9ALJpyL2jCjqeqdhUWPdqJ4{)C^-~yY}_QL46=6O`9;<wBK$>EIeSHicDKF?t%pX6?Pu7~0cG9RXmz`)M4%z6nlOR>rhyDJOFIz=b-li2y70Uu5rRCDgFPGK`Ot1us!H11nBnf}J5^$yZCyb}SEZRhhd|D@P&=-QU2@yRx|cRo_*=;!Sjdvo8uJ0W?PA!RS3BY5*)PQ;b?WC(KVe1#xsl;GEFNttM@l-J{Mx-H0X%44lXtE>B{qT>sHssZKoD$JrL>=UsIU*MK0bLhA~(7)tDySX*r?M6QaOr))a#L!>?$3*`cho8)MDNS9rE5x(A<Tc@dk03IHdSfR2~S3%(T5&q=PfxN<|s7+#6<n>Z!;OE7+|<r^J~ic%YDu5L_>zsL^5M4GyQa12Jxhcxo+zW`^Tk0F0?_GgGY;3Zrt&xN`O_MPz|#XgJ!iB+8IWsGhgLd~ii`2y}-GVW(?H063>+W$Y1|1z!Qnm1A)55A$B*dOMa82f@9!c#Ojm(*>okidLl&_eV6QCGT9Soy4`7>jNdimPaugWN*;MkzLpw(rpM2h3n}X-AtQdYN?jj5N#w)#<+klMDdtIv1t?aP|TfBl-yWbUy^f#%e9k57*VuFnv-PtYOO~i*<wbAD=3jogu?O?9IeCZgBdDYG%tUQ*|vo(HtO`_I<G;7A&%bg$H9O@Kc4R<2U9Gz8i&xl8yzz9w~VqXrR}cDDbcLAmDxmIuz)7gE&KeoFAH;l_iT?($=t{V@GG@{FPtrTzGQ;RWJ*rMtR9V|Dal7JXbL)_CGG|sTOF_r0Hsdl%Ehm2W^O_VTe?96_%m-6TJ!iDCYB;NBB<)5@LSr46R%I^*YjFfllbSpJ&9GAC&;=!wRF@7>AhYBj#gpRmSOf(3FW9&F3445r51gAudzMtFwRs=+X~gRdL<{*&pc3Hvd8NE0)IK0{Ad$Zux-J45HjD=0a@<5ir}TK?CYwm2_?m%T!TOlbm0I2ZQ<?GxX!L}V9}eBc24jdP;-<wV=TNS!@0GaNwPsDO2V1FEfm>$$UEScX%07wjpBv#>N9<1r<Wdwy{@u73-Ovn0@O)Pej%EiP)kZ%wWp^l?~!ap*zh9i76OkS$Juo4Iw5p_)~bQM#2`nB8Pc@?Zb?;-FTlVWY@mSaJC@tl;g}(K4=sH9^yzs#q^k=a;`Z;zYB{Z}%PddV3*wsb9-~-JfCBWY)h?n;xJL>_vCO7fY73V(GF!cMz32-`yS879s1#@C9dp=~<aICCNCEV|A*F^M0>|JX8G0h|q*HzvZ=m1+nY6pst)z5GWl65O8R9Knt={$Jvd=Z@8sOM;1XCD`w9T5j>v~4cmJ(#~+P?ha%-97M6mBsbh?zA?h)cj;64sUxgc$vdMuPX7_?a5uLhk{^21bfFAIu`gS4%~VGMtjI#ke8|WHTLkL-fh#4+P^jgM7;{699&_FHRxK>Ts>mqQg0&uyEotT6**|SdBIOP)t{M88b7RW4HsoH9XqGZ|0v=>?RoKrhTOIcgf$hI82rEeAZz-AD)T_NnXA%w)rP^P`!S|`DmnBUt=%_jk2yU-2Ta|%)G~>KEd&KfBMVsKY#keKTiJpZy*2r^y%q~&GQ#ePCx$BZ-4*4fBtrNjNV>e-n@Ff`*8j0@=o6D{OaxQ>iWam^Q#|rpJ|ofUcLYE;?;-icb}iR{EK(Hn-3S~-|gm~XMZ>Q;*T%+um1-w9q!2')))
_T={i:t for i,t in enumerate(_D['tapes'])}
_M=_D['meta']
MODE='fixed'
def _router(obs,step,st):
    if MODE=='fixed': return 0
    shops=list((obs.get('town') or {}).get('unlocked_shops') or [])
    if 'route' not in st: st['route']=0
    if MODE=='shop2' and step>=144 and not st.get('done'):
        best=0;bs=-1
        for i,m in enumerate(_M):
            s=sum(1 for a,b in zip(m['shops'],shops) if a==b)
            if s>bs: bs=s;best=i
        st['route']=best;st['done']=True
    return st['route']
_S={'hand_align': True, 'weed_repair': True, 'sell_lead': True, 'budget_guard': False, 'room_guard': False, 'clamp_sells': False, 'dead_stock': False, 'terminal_liquidation': True, 'front_run': False}
_IMPL=make_agent(_T,router=_router,**_S)
def agent(observation,configuration=None):
    return _IMPL(observation,configuration)
