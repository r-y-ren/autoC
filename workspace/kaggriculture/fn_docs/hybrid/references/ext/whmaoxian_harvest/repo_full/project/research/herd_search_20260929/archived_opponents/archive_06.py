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

# Archived public-development proxy; not the author private program.
import json
_DEMO=json.loads('[{"farmer":["PASS"],"hands":[],"market":[["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["BUY_ANIMAL","COW",1],["BUY_ANIMAL","SHEEP",1],["BUY_PRODUCT","WHEAT",10]]},{"farmer":["PICKUP","COW",1],"hands":[["PICKUP","COW",1],["PICKUP","SHEEP",1],["NORTH"],["PICKUP","COW",1],["PICKUP","SHEEP",1]],"market":[]},{"farmer":["BUILD_PASTURE"],"hands":[["WEST"],["NORTH"],["WEST"],["PICKUP","WHEAT",1],["WEST"]],"market":[]},{"farmer":["PLACE","COW",1],"hands":[["WEST"],["PLACE","SHEEP",1],["WEST"],["DROP"],["WEST"]],"market":[]},{"farmer":["PICKUP","SHEEP",1],"hands":[["WEST"],["PICKUP","SHEEP",1],["EAST"],["PICKUP","SHEEP",1],["WEST"]],"market":[]},{"farmer":["PLACE","SHEEP",1],"hands":[["WEST"],["CARE"],["CARE"],["CARE"],["BUILD_PASTURE"]],"market":[]},{"farmer":["PICKUP","SHEEP",1],"hands":[["WEST"],["PICKUP","SHEEP",1],["PICKUP","SHEEP",1],["PICKUP","SHEEP",1],["EAST"]],"market":[]},{"farmer":["PLACE","SHEEP",1],"hands":[["BUILD_COOP"],["PICKUP","WHEAT",2],["PICKUP","WHEAT",2],["PICKUP","WHEAT",2],["BUILD_PASTURE"]],"market":[["BUY_ANIMAL","SHEEP",1]]},{"farmer":["PICKUP","SHEEP",1],"hands":[["DIG"],["PICKUP","SHEEP",1],["PICKUP","SHEEP",1],["PICKUP","SHEEP",1],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["BUILD_COOP"],["WEST"],["FEED"],["FEED"],["WEST"]],"market":[["BUY_ANIMAL","SHEEP",1],["BUY_SEED","MELON",1]]},{"farmer":["PLACE","SHEEP",1],"hands":[["NORTH"],["PLACE","SHEEP",1],["PICKUP","SHEEP",1],["PICKUP","SHEEP",1],["NORTH"]],"market":[]},{"farmer":["CARE"],"hands":[["PLANT","MELON"],["WEST"],["NORTH"],["WEST"],["NORTH"]],"market":[["SELL","WHEAT",1],["BUY_SEED","WHEAT",1],["BUY_SEED","MELON",1]]},{"farmer":["NORTH"],"hands":[["WATER"],["PLACE","SHEEP",1],["BUILD_PASTURE"],["FEED"],["EAST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["NORTH"],["FEED"],["PLACE","SHEEP",1],["WEST"],["EAST"]],"market":[["SELL","WHEAT",1],["BUY_SEED","WHEAT",1],["BUY_SEED","MELON",1]]},{"farmer":["NORTH"],"hands":[["PLANT","WHEAT"],["CARE"],["FEED"],["WEST"],["PLANT","MELON"]],"market":[["SELL","WHEAT",1],["BUY_ANIMAL","COW",1]]},{"farmer":["PLANT","MELON"],"hands":[["WATER"],["NORTH"],["CARE"],["PLANT","WHEAT"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","MELON",1]]},{"farmer":["WATER"],"hands":[["NORTH"],["PLANT","MELON"],["SOUTH"],["WATER"],["WEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","MELON",1]]},{"farmer":["WEST"],"hands":[["PLANT","WHEAT"],["WATER"],["PICKUP","COW",1],["WEST"],["PLANT","MELON"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","MELON",1]]},{"farmer":["PLANT","WHEAT"],"hands":[["WATER"],["WEST"],["NORTH"],["DIG"],["WATER"]],"market":[["SELL","WHEAT",1],["BUY_SEED","WHEAT",1],["BUY_SEED","MELON",1]]},{"farmer":["WATER"],"hands":[["NORTH"],["PLANT","WHEAT"],["NORTH"],["PLANT","WHEAT"],["WEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","MELON",1]]},{"farmer":["WEST"],"hands":[["PLANT","WHEAT"],["WATER"],["BUILD_PASTURE"],["WATER"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PLANT","WHEAT"],"hands":[["WATER"],["NORTH"],["PLACE","COW",1],["NORTH"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["SOUTH"],["WATER"],["WEST"],["NORTH"],["WATER"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["EAST"],["EAST"],["PASS"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[],"market":[["SELL","WHEAT",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["DROP"],"hands":[["WEST"],["NORTH"],["NORTH"],["WEST"]],"market":[["BUY_PRODUCT","WHEAT",2]]},{"farmer":["PICKUP","WHEAT",2],"hands":[["WEST"],["WEST"],["WEST"],["WEST"]],"market":[["SELL","FERTILIZER",1],["BUY_ANIMAL","GOOSE",1],["BUY_ANIMAL","COW",1],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["WEST"],"hands":[["WEST"],["WEST"],["WEST"],["WEST"]],"market":[["BUY_ANIMAL","GOOSE",1],["BUY_ANIMAL","COW",1]]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WATER"]],"market":[["BUY_ANIMAL","GOOSE",1],["BUY_ANIMAL","COW",1]]},{"farmer":["CARE"],"hands":[["EAST"],["NORTH"],["EAST"],["WEST"]],"market":[["BUY_ANIMAL","GOOSE",1],["BUY_ANIMAL","COW",1]]},{"farmer":["EAST"],"hands":[["EAST"],["WATER"],["DROP"],["WATER"]],"market":[["BUY_ANIMAL","GOOSE",1],["BUY_ANIMAL","COW",1]]},{"farmer":["WEST"],"hands":[["DROP"],["NORTH"],["NORTH"],["NORTH"]],"market":[["SELL","FERTILIZER",1],["BUY_ANIMAL","COW",1],["BUY_ANIMAL","SHEEP",1],["BUY_SEED","MELON",1]]},{"farmer":["WEST"],"hands":[["NORTH"],["WATER"],["COLLECT_FERTILIZER"],["WATER"]],"market":[["SELL","FERTILIZER",1],["BUY_ANIMAL","COW",1],["BUY_ANIMAL","SHEEP",1]]},{"farmer":["FEED"],"hands":[["NORTH"],["NORTH"],["SOUTH"],["NORTH"]],"market":[["BUY_ANIMAL","COW",1],["BUY_ANIMAL","SHEEP",1]]},{"farmer":["CARE"],"hands":[["COLLECT_FERTILIZER"],["WATER"],["DROP"],["WATER"]],"market":[["BUY_ANIMAL","COW",1],["BUY_SEED","MELON",1]]},{"farmer":["NORTH"],"hands":[["SOUTH"],["NORTH"],["PICKUP","WHEAT",2],["NORTH"]],"market":[["SELL","FERTILIZER",1],["BUY_ANIMAL","COW",1]]},{"farmer":["WEST"],"hands":[["SOUTH"],["PLANT","MELON"],["NORTH"],["WATER"]],"market":[["BUY_ANIMAL","COW",1]]},{"farmer":["WATER"],"hands":[["DROP"],["WATER"],["FEED"],["NORTH"]],"market":[["BUY_ANIMAL","COW",1],["BUY_SEED","MELON",1]]},{"farmer":["PASS"],"hands":[["CARE"],["WEST"],["CARE"],["WATER"]],"market":[["SELL","FERTILIZER",1],["BUY_ANIMAL","COW",1]]},{"farmer":["NORTH"],"hands":[["NORTH"],["PLANT","MELON"],["NORTH"],["SOUTH"]],"market":[["BUY_ANIMAL","COW",1]]},{"farmer":["WATER"],"hands":[["NORTH"],["WATER"],["FEED"],["EAST"]],"market":[["BUY_ANIMAL","COW",1],["BUY_SEED","MELON",1]]},{"farmer":["PASS"],"hands":[["NORTH"],["EAST"],["CARE"],["WATER"]],"market":[["BUY_ANIMAL","COW",1]]},{"farmer":["PASS"],"hands":[["PLANT","MELON"],["EAST"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["PASS"],"hands":[["WATER"],["PLANT","MELON"],["NORTH"],["EAST"]],"market":[["BUY_SEED","MELON",1]]},{"farmer":["PASS"],"hands":[["NORTH"],["WATER"],["PLANT","MELON"],["SOUTH"]],"market":[]},{"farmer":["PASS"],"hands":[["WATER"],["PASS"],["WATER"],["SOUTH"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["SOUTH"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[],"market":[["HIRE"],["HIRE"],["HIRE"],["HIRE"],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["DROP"],"hands":[["WEST"],["NORTH"],["NORTH"],["NORTH"]],"market":[["BUY_PRODUCT","WHEAT",2]]},{"farmer":["PICKUP","WHEAT",1],"hands":[["WEST"],["WEST"],["WEST"],["NORTH"]],"market":[["SELL","FERTILIZER",1],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["FEED"],"hands":[["WEST"],["WEST"],["WEST"],["NORTH"]],"market":[["BUY_ANIMAL","GOOSE",1],["BUY_ANIMAL","COW",1],["BUY_ANIMAL","SHEEP",1]]},{"farmer":["CARE"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["COLLECT_FERTILIZER"],["WATER"]],"market":[["BUY_ANIMAL","GOOSE",1],["BUY_ANIMAL","COW",1]]},{"farmer":["NORTH"],"hands":[["EAST"],["WATER"],["EAST"],["WEST"]],"market":[["BUY_ANIMAL","COW",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["EAST"],["WEST"],["DROP"],["WATER"]],"market":[["BUY_ANIMAL","GOOSE",1],["BUY_ANIMAL","COW",1],["BUY_ANIMAL","SHEEP",1]]},{"farmer":["SOUTH"],"hands":[["DROP"],["WATER"],["NORTH"],["WEST"]],"market":[["SELL","FERTILIZER",1],["BUY_ANIMAL","COW",1],["BUY_ANIMAL","SHEEP",1]]},{"farmer":["DROP"],"hands":[["PICKUP","WHEAT",2],["NORTH"],["NORTH"],["WATER"]],"market":[["SELL","FERTILIZER",1],["BUY_ANIMAL","COW",1],["BUY_ANIMAL","SHEEP",1]]},{"farmer":["NORTH"],"hands":[["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["HARVEST"]],"market":[["SELL","FERTILIZER",1],["BUY_ANIMAL","COW",1]]},{"farmer":["NORTH"],"hands":[["FEED"],["WATER"],["SOUTH"],["PLANT","WHEAT"]],"market":[]},{"farmer":["WEST"],"hands":[["CARE"],["HARVEST"],["SOUTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WEST"],["PLANT","WHEAT"],["DROP"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["FEED"],["WATER"],["WEST"],["WATER"]],"market":[["SELL","FERTILIZER",1],["BUY_ANIMAL","COW",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["CARE"],["EAST"],["EAST"],["HARVEST"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WATER"],"hands":[["NORTH"],["SOUTH"],["PICKUP","COW",1],["WEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["WEST"],["EAST"],["NORTH"],["WATER"]],"market":[]},{"farmer":["PLANT","WHEAT"],"hands":[["WATER"],["EAST"],["WEST"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["EAST"],["EAST"],["BUILD_PASTURE"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["WATER"],["FEED"],["PLACE","COW",1],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["NORTH"],["CARE"],["NORTH"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WATER"],["NORTH"],["WEST"],["WATER"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["FEED"],["PASS"],["EAST"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["CARE"],["PASS"],["WATER"]],"market":[]},{"farmer":["PICKUP","WHEAT",2],"hands":[],"market":[["SELL","WHEAT",3],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["BUY_ANIMAL","COW",1]]},{"farmer":["NORTH"],"hands":[["WEST"],["NORTH"],["NORTH"],["WEST"]],"market":[["HIRE"],["BUY_ANIMAL","COW",1]]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["WEST"],["WEST"],["NORTH"]],"market":[["BUY_ANIMAL","COW",1]]},{"farmer":["CARE"],"hands":[["DROP"],["WEST"],["WEST"],["WEST"],["WEST"]],"market":[["BUY_ANIMAL","GOOSE",1],["BUY_ANIMAL","COW",1]]},{"farmer":["SOUTH"],"hands":[["NORTH"],["WEST"],["COLLECT_FERTILIZER"],["WATER"],["COLLECT_FERTILIZER"]],"market":[["SELL","FERTILIZER",1],["BUY_ANIMAL","COW",1],["BUY_ANIMAL","SHEEP",1]]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["HARVEST"],["EAST"],["HARVEST"],["WEST"]],"market":[["BUY_ANIMAL","COW",1],["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["SOUTH"],["EAST"],["DROP"],["WEST"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["CARE"],"hands":[["DROP"],["FEED"],["PICKUP","WHEAT",1],["WATER"],["EAST"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["NORTH"],"hands":[["NORTH"],["CARE"],["NORTH"],["HARVEST"],["EAST"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["NORTH"],["WEST"],["PLANT","WHEAT"],["DROP"]],"market":[]},{"farmer":["SOUTH"],"hands":[["COLLECT_FERTILIZER"],["EAST"],["FEED"],["WATER"],["WEST"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","WHEAT",1]]},{"farmer":["EAST"],"hands":[["SOUTH"],["CARE"],["CARE"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["DROP"],"hands":[["SOUTH"],["NORTH"],["NORTH"],["WATER"],["WEST"]],"market":[]},{"farmer":["CARE"],"hands":[["DROP"],["EAST"],["WATER"],["NORTH"],["WEST"]],"market":[["SELL","FERTILIZER",1],["BUY_ANIMAL","COW",1]]},{"farmer":["PICKUP","COW",1],"hands":[["PICKUP","COW",1],["FEED"],["NORTH"],["NORTH"],["WATER"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["WEST"],"hands":[["NORTH"],["CARE"],["NORTH"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["NORTH"],["WATER"],["WATER"],["WATER"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["NORTH"],["WEST"],["HARVEST"],["HARVEST"]],"market":[["BUY_SEED","STRAWBERRY",1],["BUY_SEED","MELON",1]]},{"farmer":["BUILD_PASTURE"],"hands":[["NORTH"],["WATER"],["WATER"],["PLANT","MELON"],["PLANT","STRAWBERRY"]],"market":[]},{"farmer":["PLACE","COW",1],"hands":[["SOUTH"],["SOUTH"],["SOUTH"],["WATER"],["WATER"]],"market":[]},{"farmer":["PASS"],"hands":[["WEST"],["WEST"],["WATER"],["SOUTH"],["WEST"]],"market":[]},{"farmer":["PASS"],"hands":[["EAST"],["PASS"],["WEST"],["WATER"],["WATER"]],"market":[]},{"farmer":["PASS"],"hands":[["WATER"],["PASS"],["WATER"],["EAST"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["PICKUP","WHEAT",4],"hands":[],"market":[["SELL","WHEAT",3],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["BUY_ANIMAL","COW",1]]},{"farmer":["FEED"],"hands":[["WEST"],["NORTH"],["NORTH"],["NORTH"]],"market":[["HIRE"],["BUY_ANIMAL","GOOSE",1],["BUY_ANIMAL","SHEEP",1]]},{"farmer":["CARE"],"hands":[["COLLECT_FERTILIZER"],["NORTH"],["WEST"],["NORTH"],["PASS"]],"market":[["BUY_ANIMAL","COW",1]]},{"farmer":["WEST"],"hands":[["DROP"],["WEST"],["WEST"],["WEST"],["NORTH"]],"market":[["BUY_ANIMAL","GOOSE",1],["BUY_ANIMAL","COW",1]]},{"farmer":["FEED"],"hands":[["NORTH"],["WEST"],["COLLECT_FERTILIZER"],["WATER"],["WEST"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["CARE"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["EAST"],["NORTH"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["SOUTH"],["WATER"],["DROP"],["WATER"],["COLLECT_FERTILIZER"]],"market":[["BUY_ANIMAL","GOOSE",1]]},{"farmer":["FEED"],"hands":[["DROP"],["HARVEST"],["PICKUP","WHEAT",3],["WEST"],["EAST"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["CARE"],"hands":[["NORTH"],["NORTH"],["NORTH"],["WATER"],["EAST"]],"market":[["SELL","FERTILIZER",1],["BUY_ANIMAL","GOOSE",1],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["WEST"],"hands":[["WEST"],["WATER"],["FEED"],["HARVEST"],["DROP"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["CARE"],["NORTH"],["PICKUP","GOOSE",1]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["CARE"],"hands":[["SOUTH"],["WATER"],["NORTH"],["WATER"],["NORTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["EAST"],["NORTH"],["FEED"],["WEST"],["WEST"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["EAST"],"hands":[["DROP"],["WATER"],["CARE"],["WATER"],["WEST"]],"market":[]},{"farmer":["EAST"],"hands":[["NORTH"],["HARVEST"],["COLLECT_FERTILIZER"],["SOUTH"],["WEST"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["EAST"],"hands":[["WEST"],["PLANT","STRAWBERRY"],["SOUTH"],["EAST"],["BUILD_COOP"]],"market":[]},{"farmer":["DROP"],"hands":[["WEST"],["WATER"],["SOUTH"],["PLANT","STRAWBERRY"],["PLACE","GOOSE",1]],"market":[]},{"farmer":["PICKUP","WHEAT",2],"hands":[["WATER"],["SOUTH"],["DROP"],["WATER"],["EAST"]],"market":[["SELL","FERTILIZER",1],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["NORTH"],"hands":[["NORTH"],["SOUTH"],["PICKUP","WHEAT",2],["WEST"],["NORTH"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["WEST"],"hands":[["WATER"],["EAST"],["NORTH"],["WATER"],["WATER"]],"market":[]},{"farmer":["FEED"],"hands":[["SOUTH"],["FEED"],["WEST"],["HARVEST"],["NORTH"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["CARE"],"hands":[["WEST"],["CARE"],["WEST"],["PLANT","STRAWBERRY"],["EAST"]],"market":[]},{"farmer":["PASS"],"hands":[["WEST"],["NORTH"],["NORTH"],["WATER"],["EAST"]],"market":[]},{"farmer":["PASS"],"hands":[["WATER"],["SOUTH"],["SOUTH"],["PASS"],["WATER"]],"market":[]},{"farmer":["PICKUP","WHEAT",4],"hands":[],"market":[["SELL","WHEAT",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["WEST"],["NORTH"],["NORTH"],["NORTH"],["NORTH"]],"market":[["HIRE"],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["CARE"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["WEST"],["NORTH"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["WEST"],"hands":[["DROP"],["WEST"],["WEST"],["WEST"],["NORTH"],["WEST"]],"market":[]},{"farmer":["FEED"],"hands":[["NORTH"],["WEST"],["COLLECT_FERTILIZER"],["WATER"],["WEST"],["COLLECT_FERTILIZER"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["CARE"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["EAST"],["NORTH"],["WATER"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["SOUTH"],["WATER"],["DROP"],["WATER"],["NORTH"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["FEED"],"hands":[["DROP"],["HARVEST"],["PICKUP","WHEAT",4],["NORTH"],["WATER"],["EAST"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","MELON",1]]},{"farmer":["CARE"],"hands":[["NORTH"],["PLANT","MELON"],["NORTH"],["WATER"],["WEST"],["EAST"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["WEST"],"hands":[["WEST"],["WATER"],["FEED"],["WEST"],["WEST"],["DROP"]],"market":[]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["NORTH"],["CARE"],["WATER"],["WATER"],["PICKUP","WHEAT",3]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["CARE"],"hands":[["SOUTH"],["NORTH"],["NORTH"],["WEST"],["SOUTH"],["NORTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["EAST"],["WATER"],["FEED"],["WATER"],["WATER"],["WEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["DROP"],["HARVEST"],["CARE"],["WEST"],["WEST"],["FEED"]],"market":[["BUY_SEED","MELON",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["PICKUP","WHEAT",2],["PLANT","MELON"],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["CARE"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["SOUTH"],"hands":[["NORTH"],["WATER"],["SOUTH"],["SOUTH"],["SOUTH"],["WEST"]],"market":[]},{"farmer":["EAST"],"hands":[["WEST"],["NORTH"],["SOUTH"],["WATER"],["WATER"],["WEST"]],"market":[]},{"farmer":["EAST"],"hands":[["WEST"],["SOUTH"],["DROP"],["SOUTH"],["EAST"],["FEED"]],"market":[]},{"farmer":["EAST"],"hands":[["SOUTH"],["SOUTH"],["PASS"],["SOUTH"],["WATER"],["CARE"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["DROP"],"hands":[["EAST"],["WATER"],["PASS"],["WATER"],["SOUTH"],["EAST"]],"market":[]},{"farmer":["PASS"],"hands":[["EAST"],["PASS"],["PASS"],["PASS"],["WATER"],["WATER"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["PASS"],"hands":[["DROP"],["PASS"],["PASS"],["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["NORTH"],"hands":[],"market":[["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["BUY_ANIMAL","COW",1]]},{"farmer":["HARVEST"],"hands":[["WEST"],["PICKUP","COW",1],["PICKUP","COW",1],["PICKUP","COW",1],["WEST"]],"market":[["SELL","WHEAT",1],["HIRE"],["HIRE"]]},{"farmer":["SOUTH"],"hands":[["HARVEST"],["PASS"],["PICKUP","WHEAT",7],["PASS"],["WEST"],["NORTH"],["NORTH"]],"market":[["SELL","WHEAT",1],["HIRE"],["HIRE"]]},{"farmer":["DROP"],"hands":[["EAST"],["PASS"],["NORTH"],["PASS"],["HARVEST"],["WEST"],["NORTH"],["WEST"],["NORTH"]],"market":[["BUY_PRODUCT","WHEAT",2]]},{"farmer":["PICKUP","WHEAT",2],"hands":[["DROP"],["PASS"],["WEST"],["PASS"],["EAST"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["WEST"]],"market":[["SELL","WOOL",6],["BUY_LAND"],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["BUILD_PASTURE"],["CARE"],["PASS"],["EAST"],["WATER"],["WATER"],["WEST"],["COLLECT_FERTILIZER"]],"market":[["SELL","WOOL",6],["BUY_SEED","STRAWBERRY",3]]},{"farmer":["CARE"],"hands":[["DROP"],["PLACE","COW",1],["FEED"],["PASS"],["DROP"],["NORTH"],["EAST"],["COLLECT_FERTILIZER"],["SOUTH"]],"market":[["SELL","WHEAT",1],["BUY_ANIMAL","GOOSE",1]]},{"farmer":["NORTH"],"hands":[["PICKUP","GOOSE",1],["PICKUP","GOOSE",1],["WEST"],["NORTH"],["NORTH"],["WATER"],["PLANT","STRAWBERRY"],["EAST"],["DROP"]],"market":[["SELL","WOOL",6],["SELL","FERTILIZER",1],["BUY_ANIMAL","GOOSE",1],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["FEED"],"hands":[["EAST"],["PICKUP","GOOSE",1],["FEED"],["PICKUP","GOOSE",1],["NORTH"],["NORTH"],["WATER"],["EAST"],["NORTH"]],"market":[["SELL","FERTILIZER",1],["BUY_ANIMAL","GOOSE",1],["BUY_SEED","STRAWBERRY",3]]},{"farmer":["CARE"],"hands":[["EAST"],["NORTH"],["CARE"],["PICKUP","GOOSE",1],["NORTH"],["WATER"],["EAST"],["DROP"],["WEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["BUILD_COOP"],["BUILD_COOP"],["WEST"],["EAST"],["NORTH"],["EAST"],["PLANT","STRAWBERRY"],["PICKUP","WHEAT",2],["COLLECT_FERTILIZER"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["PLACE","GOOSE",1],["PLACE","GOOSE",1],["FEED"],["NORTH"],["WATER"],["WATER"],["WATER"],["NORTH"],["SOUTH"]],"market":[]},{"farmer":["SOUTH"],"hands":[["NORTH"],["NORTH"],["CARE"],["BUILD_COOP"],["EAST"],["SOUTH"],["EAST"],["WEST"],["EAST"]],"market":[["SELL","WHEAT",1],["BUY_ANIMAL","GOOSE",1]]},{"farmer":["SOUTH"],"hands":[["EAST"],["PLANT","STRAWBERRY"],["COLLECT_FERTILIZER"],["PLACE","GOOSE",1],["PLANT","STRAWBERRY"],["WATER"],["PLANT","STRAWBERRY"],["WEST"],["DROP"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["DROP"],"hands":[["PLANT","STRAWBERRY"],["WATER"],["EAST"],["NORTH"],["WATER"],["NORTH"],["WATER"],["WEST"],["PICKUP","GOOSE",1]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","STRAWBERRY",3]]},{"farmer":["PICKUP","WHEAT",1],"hands":[["WATER"],["EAST"],["EAST"],["PLANT","STRAWBERRY"],["EAST"],["NORTH"],["EAST"],["FEED"],["EAST"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["EAST"],"hands":[["EAST"],["EAST"],["EAST"],["WATER"],["PLANT","STRAWBERRY"],["WATER"],["PLANT","STRAWBERRY"],["CARE"],["EAST"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["EAST"],"hands":[["PLANT","STRAWBERRY"],["PLANT","STRAWBERRY"],["DROP"],["EAST"],["WATER"],["WEST"],["WATER"],["COLLECT_FERTILIZER"],["EAST"]],"market":[["BUY_SEED","STRAWBERRY",2]]},{"farmer":["CARE"],"hands":[["WATER"],["WATER"],["PICKUP","WHEAT",1],["WATER"],["EAST"],["WATER"],["EAST"],["WEST"],["BUILD_COOP"]],"market":[["SELL","FERTILIZER",1],["SELL","WHEAT",1],["BUY_SEED","STRAWBERRY",2]]},{"farmer":["FEED"],"hands":[["EAST"],["EAST"],["EAST"],["EAST"],["PLANT","STRAWBERRY"],["WEST"],["PLANT","STRAWBERRY"],["WATER"],["PLACE","GOOSE",1]],"market":[["SELL","WHEAT",1]]},{"farmer":["EAST"],"hands":[["PLANT","STRAWBERRY"],["EAST"],["NORTH"],["PLANT","STRAWBERRY"],["WATER"],["WATER"],["WATER"],["NORTH"],["EAST"]],"market":[["SELL","WHEAT",1],["BUY_SEED","STRAWBERRY",2]]},{"farmer":["CARE"],"hands":[["WATER"],["PLANT","STRAWBERRY"],["EAST"],["WATER"],["EAST"],["WEST"],["NORTH"],["EAST"],["EAST"]],"market":[["SELL","WHEAT",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PASS"],"hands":[["NORTH"],["WATER"],["FEED"],["EAST"],["PLANT","STRAWBERRY"],["WATER"],["PLANT","STRAWBERRY"],["WATER"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["CARE"],["PASS"],["WATER"],["PASS"],["WATER"],["PASS"],["PASS"]],"market":[]},{"farmer":["PICKUP","WHEAT",1],"hands":[],"market":[["SELL","FERTILIZER",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["NORTH"],["NORTH"],["NORTH"],["NORTH"]],"market":[["HIRE"],["HIRE"],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["CARE"],"hands":[["DROP"],["NORTH"],["EAST"],["NORTH"],["NORTH"],["NORTH"],["NORTH"]],"market":[["HIRE"],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["PICKUP","WHEAT",2],["WEST"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["DROP"],"hands":[["FEED"],["WEST"],["WEST"],["WATER"],["WEST"],["WEST"],["COLLECT_FERTILIZER"],["WEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["CARE"],["WATER"],["DROP"],["NORTH"],["WATER"],["COLLECT_FERTILIZER"],["EAST"],["COLLECT_FERTILIZER"]],"market":[["SELL","FERTILIZER",1],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["EAST"],["NORTH"],["PICKUP","WHEAT",2],["WATER"],["NORTH"],["WEST"],["COLLECT_FERTILIZER"],["WEST"]],"market":[["SELL","FERTILIZER",1],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["SOUTH"],"hands":[["FEED"],["WATER"],["NORTH"],["NORTH"],["WATER"],["COLLECT_FERTILIZER"],["SOUTH"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["DROP"],"hands":[["CARE"],["WEST"],["FEED"],["WATER"],["EAST"],["EAST"],["WEST"],["WEST"]],"market":[["BUY_ANIMAL","GOOSE",1],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["PICKUP","WHEAT",4],"hands":[["EAST"],["WATER"],["CARE"],["WEST"],["EAST"],["EAST"],["DROP"],["COLLECT_FERTILIZER"]],"market":[["SELL","FERTILIZER",1],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["NORTH"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["EAST"],["WATER"],["WATER"],["DROP"],["PICKUP","WHEAT",2],["EAST"]],"market":[["SELL","FERTILIZER",2],["BUY_ANIMAL","GOOSE",1]]},{"farmer":["WEST"],"hands":[["WEST"],["WATER"],["FEED"],["WEST"],["EAST"],["NORTH"],["EAST"],["EAST"]],"market":[["SELL","FERTILIZER",2],["BUY_ANIMAL","GOOSE",1],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["FEED"],"hands":[["WEST"],["SOUTH"],["CARE"],["WATER"],["WATER"],["WEST"],["EAST"],["EAST"]],"market":[]},{"farmer":["CARE"],"hands":[["DROP"],["WATER"],["EAST"],["SOUTH"],["EAST"],["COLLECT_FERTILIZER"],["FEED"],["DROP"]],"market":[]},{"farmer":["NORTH"],"hands":[["PICKUP","GOOSE",1],["SOUTH"],["WATER"],["WATER"],["WATER"],["SOUTH"],["CARE"],["PICKUP","GOOSE",1]],"market":[["SELL","FERTILIZER",2],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["EAST"],"hands":[["EAST"],["WATER"],["EAST"],["WEST"],["EAST"],["EAST"],["NORTH"],["PICKUP","WHEAT",2]],"market":[["BUY_PRODUCT","WHEAT",2]]},{"farmer":["FEED"],"hands":[["EAST"],["NORTH"],["WATER"],["WATER"],["WATER"],["DROP"],["WEST"],["WEST"]],"market":[]},{"farmer":["CARE"],"hands":[["EAST"],["EAST"],["EAST"],["NORTH"],["SOUTH"],["PICKUP","WHEAT",2],["WEST"],["FEED"]],"market":[["SELL","FERTILIZER",1],["BUY_PRODUCT","WHEAT",7]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["BUILD_COOP"],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["WATER"],["NORTH"],["WEST"],["CARE"]],"market":[]},{"farmer":["SOUTH"],"hands":[["PLACE","GOOSE",1],["NORTH"],["NORTH"],["SOUTH"],["WEST"],["WEST"],["FEED"],["WEST"]],"market":[]},{"farmer":["SOUTH"],"hands":[["EAST"],["NORTH"],["WATER"],["EAST"],["WATER"],["WEST"],["CARE"],["FEED"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["DROP"],"hands":[["NORTH"],["EAST"],["WEST"],["EAST"],["WEST"],["WEST"],["NORTH"],["CARE"]],"market":[]},{"farmer":["PASS"],"hands":[["NORTH"],["WATER"],["WATER"],["WATER"],["WATER"],["FEED"],["EAST"],["PASS"]],"market":[["SELL","FERTILIZER",1],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["PASS"],"hands":[["WEST"],["PASS"],["WEST"],["PASS"],["PASS"],["CARE"],["WATER"],["PASS"]],"market":[]},{"farmer":["HARVEST"],"hands":[],"market":[["SELL","FERTILIZER",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["BUY_PRODUCT","WHEAT",11]]},{"farmer":["DROP"],"hands":[["PICKUP","WHEAT",4],["NORTH"],["NORTH"],["NORTH"],["NORTH"]],"market":[["BUY_PRODUCT","WHEAT",10]]},{"farmer":["PICKUP","WHEAT",4],"hands":[["NORTH"],["NORTH"],["NORTH"],["NORTH"],["NORTH"]],"market":[["SELL","MILK",6],["HIRE"],["HIRE"],["BUY_PRODUCT","WHEAT",19]]},{"farmer":["WEST"],"hands":[["FEED"],["WEST"],["NORTH"],["HARVEST"],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"]],"market":[["BUY_PRODUCT","WHEAT",12]]},{"farmer":["FEED"],"hands":[["CARE"],["WEST"],["EAST"],["SOUTH"],["WATER"],["DROP"],["PICKUP","WHEAT",4]],"market":[]},{"farmer":["CARE"],"hands":[["COLLECT_FERTILIZER"],["WATER"],["WATER"],["SOUTH"],["NORTH"],["EAST"],["NORTH"]],"market":[["SELL","FERTILIZER",1],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["SOUTH"],["NORTH"],["EAST"],["DROP"],["WATER"],["COLLECT_FERTILIZER"],["FEED"]],"market":[]},{"farmer":["WEST"],"hands":[["DROP"],["WATER"],["WATER"],["COLLECT_FERTILIZER"],["EAST"],["EAST"],["CARE"]],"market":[["SELL","MILK",2],["BUY_PRODUCT","WHEAT",11]]},{"farmer":["FEED"],"hands":[["PICKUP","WHEAT",4],["NORTH"],["NORTH"],["DROP"],["WATER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"]],"market":[["SELL","MILK",1],["SELL","FERTILIZER",1]]},{"farmer":["CARE"],"hands":[["EAST"],["WATER"],["WATER"],["PICKUP","WHEAT",4],["SOUTH"],["WEST"],["NORTH"]],"market":[["SELL","MILK",1],["SELL","FERTILIZER",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FEED"],["NORTH"],["EAST"],["FEED"],["WATER"],["WEST"],["FEED"]],"market":[]},{"farmer":["WEST"],"hands":[["CARE"],["WATER"],["WATER"],["CARE"],["NORTH"],["DROP"],["CARE"]],"market":[]},{"farmer":["FEED"],"hands":[["EAST"],["WEST"],["EAST"],["NORTH"],["EAST"],["PICKUP","WHEAT",4],["COLLECT_FERTILIZER"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["CARE"],"hands":[["FEED"],["WATER"],["WATER"],["WEST"],["WATER"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["CARE"],["WEST"],["SOUTH"],["FEED"],["EAST"],["EAST"],["WATER"]],"market":[["SELL","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["EAST"],["WATER"],["WATER"],["CARE"],["WATER"],["FEED"],["NORTH"]],"market":[]},{"farmer":["FEED"],"hands":[["FEED"],["SOUTH"],["WEST"],["COLLECT_FERTILIZER"],["EAST"],["CARE"],["WATER"]],"market":[]},{"farmer":["CARE"],"hands":[["CARE"],["WATER"],["WATER"],["SOUTH"],["WATER"],["COLLECT_FERTILIZER"],["WEST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["SOUTH"],["SOUTH"],["EAST"],["SOUTH"],["SOUTH"],["WATER"]],"market":[]},{"farmer":["HARVEST"],"hands":[["EAST"],["SOUTH"],["WATER"],["DROP"],["SOUTH"],["WEST"],["SOUTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["PLANT","WHEAT"],["WATER"],["WEST"],["PICKUP","WHEAT",4],["WEST"],["DROP"],["WATER"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WATER"],["SOUTH"],["WATER"],["EAST"],["WEST"],["PASS"],["SOUTH"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["NORTH"],["WATER"],["EAST"],["PASS"],["WEST"],["PASS"],["WATER"]],"market":[]},{"farmer":["WATER"],"hands":[["WATER"],["PASS"],["EAST"],["PASS"],["WEST"],["PASS"],["PASS"]],"market":[]},{"farmer":["NORTH"],"hands":[],"market":[["SELL","FERTILIZER",7],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["HARVEST"],"hands":[["WEST"],["PICKUP","WHEAT",4],["NORTH"],["NORTH"],["WEST"],["NORTH"],["NORTH"],["PASS"]],"market":[["SELL","EGG",4],["HIRE"],["HIRE"]]},{"farmer":["SOUTH"],"hands":[["HARVEST"],["NORTH"],["PICKUP","WHEAT",4],["NORTH"],["WEST"],["NORTH"],["NORTH"],["NORTH"],["NORTH"],["NORTH"]],"market":[["HIRE"]]},{"farmer":["DROP"],"hands":[["EAST"],["FEED"],["WEST"],["NORTH"],["HARVEST"],["NORTH"],["WEST"],["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["WEST"],["NORTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["DROP"],["CARE"],["FEED"],["WATER"],["EAST"],["WEST"],["WEST"],["FEED"],["NORTH"],["WEST"],["WEST"]],"market":[["SELL","WOOL",4]]},{"farmer":["DROP"],"hands":[["PICKUP","WHEAT",4],["COLLECT_FERTILIZER"],["CARE"],["EAST"],["EAST"],["WEST"],["WATER"],["CARE"],["FEED"],["WEST"],["COLLECT_FERTILIZER"]],"market":[["SELL","WOOL",3]]},{"farmer":["WEST"],"hands":[["NORTH"],["EAST"],["WEST"],["WATER"],["DROP"],["WATER"],["NORTH"],["COLLECT_FERTILIZER"],["CARE"],["WEST"],["WEST"]],"market":[["SELL","WOOL",1],["SELL","FERTILIZER",1]]},{"farmer":["WEST"],"hands":[["WEST"],["FEED"],["FEED"],["EAST"],["PICKUP","WHEAT",3],["NORTH"],["WATER"],["EAST"],["COLLECT_FERTILIZER"],["WATER"],["COLLECT_FERTILIZER"]],"market":[["BUY_LAND"]]},{"farmer":["SOUTH"],"hands":[["FEED"],["CARE"],["CARE"],["WATER"],["FEED"],["WATER"],["WEST"],["FEED"],["NORTH"],["SOUTH"],["EAST"]],"market":[["SELL","WHEAT",1]]},{"farmer":["PLANT","WHEAT"],"hands":[["CARE"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["CARE"],["EAST"],["WATER"],["CARE"],["FEED"],["PLANT","WHEAT"],["EAST"]],"market":[["SELL","MILK",1],["SELL","WHEAT",2],["BUY_ANIMAL","GOOSE",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["COLLECT_FERTILIZER"],["SOUTH"],["FEED"],["WATER"],["PICKUP","GOOSE",1],["WATER"],["SOUTH"],["COLLECT_FERTILIZER"],["CARE"],["WATER"],["DROP"]],"market":[["BUY_SEED","WHEAT",3]]},{"farmer":["SOUTH"],"hands":[["SOUTH"],["WEST"],["CARE"],["WEST"],["SOUTH"],["SOUTH"],["SOUTH"],["EAST"],["COLLECT_FERTILIZER"],["SOUTH"],["SOUTH"]],"market":[["SELL","FERTILIZER",2],["SELL","WHEAT",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PLANT","WHEAT"],"hands":[["SOUTH"],["DROP"],["COLLECT_FERTILIZER"],["WATER"],["BUILD_COOP"],["WATER"],["SOUTH"],["FEED"],["SOUTH"],["PLANT","WHEAT"],["SOUTH"]],"market":[["SELL","WHEAT",1]]},{"farmer":["WATER"],"hands":[["SOUTH"],["PICKUP","WHEAT",3],["NORTH"],["NORTH"],["PLACE","GOOSE",1],["SOUTH"],["PLANT","WHEAT"],["CARE"],["SOUTH"],["WATER"],["PLANT","WHEAT"]],"market":[["SELL","FERTILIZER",2],["SELL","WHEAT",1],["BUY_ANIMAL","GOOSE",1],["BUY_SEED","WHEAT",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["SOUTH"],"hands":[["SOUTH"],["EAST"],["FEED"],["WATER"],["PICKUP","GOOSE",1],["WEST"],["WATER"],["COLLECT_FERTILIZER"],["DROP"],["SOUTH"],["WATER"]],"market":[["SELL","MILK",1],["SELL","WHEAT",1],["BUY_SEED","WHEAT",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PLANT","STRAWBERRY"],"hands":[["PLANT","STRAWBERRY"],["EAST"],["CARE"],["EAST"],["WEST"],["WATER"],["SOUTH"],["WEST"],["PICKUP","WHEAT",2],["PLANT","WHEAT"],["SOUTH"]],"market":[["SELL","FERTILIZER",2],["SELL","WHEAT",1],["BUY_ANIMAL","GOOSE",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WATER"],"hands":[["WATER"],["EAST"],["COLLECT_FERTILIZER"],["WATER"],["BUILD_COOP"],["NORTH"],["PLANT","STRAWBERRY"],["WEST"],["PICKUP","GOOSE",1],["WATER"],["PLANT","WHEAT"]],"market":[["SELL","WHEAT",1],["BUY_SEED","WHEAT",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["SOUTH"],"hands":[["SOUTH"],["FEED"],["HARVEST"],["EAST"],["PLACE","GOOSE",1],["NORTH"],["WATER"],["DROP"],["SOUTH"],["SOUTH"],["WATER"]],"market":[["SELL","WHEAT",1],["BUY_SEED","WHEAT",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PLANT","WHEAT"],"hands":[["PLANT","STRAWBERRY"],["CARE"],["WEST"],["WATER"],["FEED"],["WEST"],["SOUTH"],["PICKUP","WHEAT",1],["SOUTH"],["PLANT","WHEAT"],["SOUTH"]],"market":[["SELL","FERTILIZER",3],["BUY_SEED","WHEAT",1],["BUY_SEED","STRAWBERRY",2],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["WATER"],"hands":[["WATER"],["COLLECT_FERTILIZER"],["WATER"],["EAST"],["CARE"],["WATER"],["PLANT","STRAWBERRY"],["SOUTH"],["WEST"],["WATER"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1],["BUY_PRODUCT","WHEAT",10]]},{"farmer":["SOUTH"],"hands":[["SOUTH"],["EAST"],["NORTH"],["WATER"],["EAST"],["WEST"],["WATER"],["WEST"],["BUILD_COOP"],["SOUTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",2],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["PLANT","WHEAT"],"hands":[["PLANT","WHEAT"],["WATER"],["WATER"],["SOUTH"],["FEED"],["WATER"],["SOUTH"],["FEED"],["PLACE","GOOSE",1],["PLANT","WHEAT"],["SOUTH"]],"market":[["SELL","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WATER"],["NORTH"],["NORTH"],["WATER"],["CARE"],["WEST"],["PLANT","STRAWBERRY"],["CARE"],["FEED"],["WATER"],["PLANT","WHEAT"]],"market":[]},{"farmer":["NORTH"],"hands":[["PASS"],["WATER"],["WATER"],["PASS"],["PASS"],["WATER"],["WATER"],["PASS"],["CARE"],["PASS"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[],"market":[["SELL","FERTILIZER",4],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["HARVEST"],["PICKUP","WHEAT",4],["NORTH"],["NORTH"],["NORTH"],["NORTH"],["NORTH"],["SOUTH"]],"market":[["HIRE"],["HIRE"],["BUY_PRODUCT","WHEAT",11]]},{"farmer":["WEST"],"hands":[["DROP"],["NORTH"],["NORTH"],["NORTH"],["NORTH"],["NORTH"],["NORTH"],["SOUTH"],["NORTH"],["NORTH"]],"market":[["SELL","EGG",2],["BUY_PRODUCT","WHEAT",11]]},{"farmer":["WATER"],"hands":[["PICKUP","WHEAT",4],["FEED"],["NORTH"],["NORTH"],["HARVEST"],["NORTH"],["NORTH"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"]],"market":[["SELL","MILK",3],["BUY_PRODUCT","WHEAT",14]]},{"farmer":["HARVEST"],"hands":[["NORTH"],["CARE"],["NORTH"],["WATER"],["SOUTH"],["WEST"],["WEST"],["WATER"],["NORTH"],["DROP"]],"market":[]},{"farmer":["SOUTH"],"hands":[["FEED"],["COLLECT_FERTILIZER"],["WATER"],["NORTH"],["SOUTH"],["WEST"],["WEST"],["SOUTH"],["WEST"],["PICKUP","WHEAT",4]],"market":[["SELL","FERTILIZER",1],["BUY_PRODUCT","WHEAT",12]]},{"farmer":["EAST"],"hands":[["CARE"],["HARVEST"],["NORTH"],["WATER"],["DROP"],["WATER"],["WATER"],["WATER"],["WATER"],["EAST"]],"market":[]},{"farmer":["EAST"],"hands":[["COLLECT_FERTILIZER"],["EAST"],["WATER"],["NORTH"],["PICKUP","WHEAT",4],["HARVEST"],["HARVEST"],["WEST"],["HARVEST"],["FEED"]],"market":[["BUY_PRODUCT","WHEAT",14]]},{"farmer":["DROP"],"hands":[["NORTH"],["FEED"],["SOUTH"],["WATER"],["WEST"],["SOUTH"],["SOUTH"],["WATER"],["SOUTH"],["CARE"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PICKUP","WHEAT",4],"hands":[["FEED"],["CARE"],["SOUTH"],["WEST"],["FEED"],["SOUTH"],["SOUTH"],["WEST"],["SOUTH"],["COLLECT_FERTILIZER"]],"market":[["SELL","MELON",6],["BUY_PRODUCT","WHEAT",33]]},{"farmer":["FEED"],"hands":[["CARE"],["COLLECT_FERTILIZER"],["SOUTH"],["WEST"],["CARE"],["SOUTH"],["EAST"],["WATER"],["EAST"],["HARVEST"]],"market":[["BUY_PRODUCT","WHEAT",12]]},{"farmer":["CARE"],"hands":[["COLLECT_FERTILIZER"],["HARVEST"],["WEST"],["WATER"],["COLLECT_FERTILIZER"],["EAST"],["EAST"],["WEST"],["DROP"],["EAST"]],"market":[]},{"farmer":["NORTH"],"hands":[["WEST"],["EAST"],["HARVEST"],["WEST"],["WEST"],["DROP"],["DROP"],["WATER"],["COLLECT_FERTILIZER"],["FEED"]],"market":[["SELL","MELON",6],["SELL","MILK",2],["BUY_PRODUCT","WHEAT",12]]},{"farmer":["WEST"],"hands":[["PLANT","WHEAT"],["WATER"],["SOUTH"],["WATER"],["FEED"],["SOUTH"],["PICKUP","WHEAT",4],["SOUTH"],["DROP"],["CARE"]],"market":[["SELL","MILK",1],["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["WATER"],["EAST"],["EAST"],["WEST"],["CARE"],["COLLECT_FERTILIZER"],["SOUTH"],["PLANT","WHEAT"],["WEST"],["COLLECT_FERTILIZER"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["NORTH"],["WATER"],["DROP"],["WATER"],["COLLECT_FERTILIZER"],["DROP"],["FEED"],["WATER"],["WEST"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["PLANT","WHEAT"],["NORTH"],["PICKUP","WHEAT",4],["WEST"],["WEST"],["SOUTH"],["CARE"],["WEST"],["WEST"],["EAST"]],"market":[["SELL","MILK",1],["SELL","FERTILIZER",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["WATER"],["WATER"],["SOUTH"],["WATER"],["FEED"],["WEST"],["WEST"],["WATER"],["COLLECT_FERTILIZER"],["FEED"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PLANT","WHEAT"],"hands":[["WEST"],["EAST"],["WEST"],["SOUTH"],["CARE"],["COLLECT_FERTILIZER"],["FEED"],["NORTH"],["NORTH"],["CARE"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WATER"],["WATER"],["CARE"],["EAST"],["NORTH"],["NORTH"],["CARE"],["WATER"],["WEST"],["COLLECT_FERTILIZER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["SOUTH"],["NORTH"],["COLLECT_FERTILIZER"],["WATER"],["FEED"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"],["EAST"]],"market":[]},{"farmer":["NORTH"],"hands":[["PLANT","WHEAT"],["WEST"],["WEST"],["WEST"],["CARE"],["EAST"],["SOUTH"],["WATER"],["HARVEST"],["WATER"]],"market":[["SELL","MILK",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WATER"],["WATER"],["FERTILIZE"],["WATER"],["COLLECT_FERTILIZER"],["DROP"],["FEED"],["EAST"],["PLANT","WHEAT"],["NORTH"]],"market":[["SELL","WHEAT",9]]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["WATER"],["PASS"],["HARVEST"],["PASS"],["CARE"],["WATER"],["WATER"],["WATER"]],"market":[["SELL","MELON",3],["SELL","WHEAT",5],["SELL","FERTILIZER",1]]},{"farmer":["NORTH"],"hands":[],"market":[["SELL","FERTILIZER",12],["SELL","MILK",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["PICKUP","WHEAT",5],["NORTH"],["NORTH"],["SOUTH"],["SOUTH"]],"market":[["SELL","EGG",7],["SELL","MILK",2],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["NORTH"],["FEED"],["FEED"],["NORTH"],["NORTH"],["NORTH"],["WATER"],["SOUTH"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",4]],"market":[["SELL","EGG",4]]},{"farmer":["WATER"],"hands":[["FEED"],["CARE"],["CARE"],["NORTH"],["NORTH"],["WATER"],["SOUTH"],["WEST"],["WEST"],["EAST"]],"market":[]},{"farmer":["NORTH"],"hands":[["CARE"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FEED"],["HARVEST"],["NORTH"],["WEST"],["WATER"],["FEED"],["FEED"]],"market":[]},{"farmer":["WATER"],"hands":[["COLLECT_FERTILIZER"],["NORTH"],["WEST"],["CARE"],["SOUTH"],["WATER"],["WATER"],["SOUTH"],["CARE"],["CARE"]],"market":[["SELL","EGG",2]]},{"farmer":["HARVEST"],"hands":[["NORTH"],["EAST"],["FEED"],["COLLECT_FERTILIZER"],["SOUTH"],["NORTH"],["WEST"],["WATER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"]],"market":[["SELL","MELON",15]]},{"farmer":["SOUTH"],"hands":[["FEED"],["FEED"],["CARE"],["NORTH"],["SOUTH"],["WATER"],["WATER"],["SOUTH"],["WEST"],["EAST"]],"market":[]},{"farmer":["SOUTH"],"hands":[["CARE"],["CARE"],["COLLECT_FERTILIZER"],["EAST"],["DROP"],["WEST"],["WEST"],["WATER"],["FEED"],["FEED"]],"market":[]},{"farmer":["SOUTH"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["SOUTH"],["WATER"],["COLLECT_FERTILIZER"],["WEST"],["WATER"],["WEST"],["CARE"],["CARE"]],"market":[["SELL","MELON",6],["SELL","MILK",1]]},{"farmer":["SOUTH"],"hands":[["NORTH"],["HARVEST"],["FEED"],["NORTH"],["NORTH"],["WATER"],["NORTH"],["WATER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["DROP"],"hands":[["PLANT","WHEAT"],["NORTH"],["CARE"],["WATER"],["WEST"],["HARVEST"],["WATER"],["WEST"],["WEST"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PICKUP","WHEAT",4],"hands":[["WATER"],["EAST"],["COLLECT_FERTILIZER"],["NORTH"],["COLLECT_FERTILIZER"],["SOUTH"],["WEST"],["WATER"],["HARVEST"],["EAST"]],"market":[["SELL","MELON",6],["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["NORTH"],["WATER"],["WEST"],["WATER"],["NORTH"],["SOUTH"],["WATER"],["WEST"],["FEED"],["FEED"]],"market":[["SELL","EGG",1]]},{"farmer":["CARE"],"hands":[["PLANT","WHEAT"],["NORTH"],["FERTILIZE"],["EAST"],["NORTH"],["SOUTH"],["NORTH"],["WEST"],["CARE"],["CARE"]],"market":[["SELL","EGG",2],["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["WATER"],["WATER"],["WATER"],["WATER"],["WEST"],["SOUTH"],["WATER"],["WATER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["WEST"],["EAST"],["NORTH"],["EAST"],["WATER"],["EAST"],["NORTH"],["HARVEST"],["EAST"],["HARVEST"]],"market":[]},{"farmer":["FEED"],"hands":[["PLANT","WHEAT"],["EAST"],["WATER"],["WATER"],["NORTH"],["DROP"],["WATER"],["PLANT","WHEAT"],["EAST"],["EAST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["WATER"],["WATER"],["WEST"],["EAST"],["WEST"],["SOUTH"],["NORTH"],["WATER"],["EAST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["WEST"],["WEST"],["FERTILIZE"],["WATER"],["WATER"],["WEST"],["NORTH"],["NORTH"],["DROP"],["HARVEST"]],"market":[]},{"farmer":["WEST"],"hands":[["WATER"],["WATER"],["WATER"],["SOUTH"],["HARVEST"],["WEST"],["WATER"],["WATER"],["NORTH"],["PLANT","WHEAT"]],"market":[["SELL","FERTILIZER",3]]},{"farmer":["FEED"],"hands":[["HARVEST"],["SOUTH"],["SOUTH"],["SOUTH"],["PLANT","WHEAT"],["SOUTH"],["NORTH"],["NORTH"],["WEST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["PLANT","WHEAT"],["WATER"],["SOUTH"],["WATER"],["WATER"],["SOUTH"],["NORTH"],["WATER"],["WEST"],["NORTH"]],"market":[["SELL","WHEAT",5]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["PASS"],["SOUTH"],["PASS"],["PASS"],["SOUTH"],["WATER"],["PASS"],["WEST"],["WATER"]],"market":[]},{"farmer":["HARVEST"],"hands":[],"market":[["SELL","FERTILIZER",12],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["BUY_ANIMAL","COW",1]]},{"farmer":["DROP"],"hands":[["PICKUP","WHEAT",4],["PICKUP","COW",1],["PICKUP","WHEAT",3],["NORTH"],["WEST"],["SOUTH"],["SOUTH"],["NORTH"]],"market":[["SELL","WOOL",1],["HIRE"],["HIRE"]]},{"farmer":["PICKUP","WHEAT",4],"hands":[["FEED"],["WEST"],["NORTH"],["HARVEST"],["WEST"],["WATER"],["SOUTH"],["HARVEST"],["PICKUP","WHEAT",3],["WEST"]],"market":[["SELL","WOOL",2]]},{"farmer":["WEST"],"hands":[["CARE"],["WEST"],["EAST"],["SOUTH"],["WEST"],["WEST"],["WEST"],["NORTH"],["NORTH"],["COLLECT_FERTILIZER"]],"market":[["SELL","WOOL",1]]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["WATER"],["FEED"],["DROP"],["HARVEST"],["WEST"],["WATER"],["HARVEST"],["FEED"],["WEST"]],"market":[]},{"farmer":["CARE"],"hands":[["NORTH"],["HARVEST"],["CARE"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WATER"],["HARVEST"],["SOUTH"],["CARE"],["WEST"]],"market":[["BUY_SEED","STRAWBERRY",3]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["EAST"],["BUILD_PASTURE"],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",3],["WEST"],["HARVEST"],["PLANT","STRAWBERRY"],["SOUTH"],["COLLECT_FERTILIZER"],["WATER"]],"market":[["SELL","EGG",2]]},{"farmer":["WEST"],"hands":[["FEED"],["PLACE","COW",1],["HARVEST"],["NORTH"],["COLLECT_FERTILIZER"],["PLANT","STRAWBERRY"],["WATER"],["DROP"],["HARVEST"],["HARVEST"]],"market":[["SELL","EGG",1]]},{"farmer":["FEED"],"hands":[["CARE"],["FEED"],["EAST"],["FEED"],["NORTH"],["WATER"],["SOUTH"],["PICKUP","WHEAT",3],["NORTH"],["PLANT","WHEAT"]],"market":[["SELL","EGG",4]]},{"farmer":["CARE"],"hands":[["COLLECT_FERTILIZER"],["CARE"],["FEED"],["CARE"],["NORTH"],["SOUTH"],["WATER"],["FEED"],["WATER"],["WATER"]],"market":[["SELL","MILK",1]]},{"farmer":["WEST"],"hands":[["HARVEST"],["SOUTH"],["CARE"],["COLLECT_FERTILIZER"],["FERTILIZE"],["WATER"],["HARVEST"],["CARE"],["NORTH"],["WEST"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["FEED"],"hands":[["EAST"],["EAST"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"],["SOUTH"],["PLANT","STRAWBERRY"],["NORTH"],["WEST"],["FERTILIZE"]],"market":[]},{"farmer":["CARE"],"hands":[["WATER"],["FEED"],["HARVEST"],["FEED"],["NORTH"],["WATER"],["WATER"],["WEST"],["WEST"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["EAST"],["CARE"],["EAST"],["CARE"],["WATER"],["HARVEST"],["SOUTH"],["FEED"],["WATER"],["SOUTH"]],"market":[["SELL","MILK",1]]},{"farmer":["FEED"],"hands":[["WATER"],["COLLECT_FERTILIZER"],["FEED"],["COLLECT_FERTILIZER"],["NORTH"],["PLANT","STRAWBERRY"],["WATER"],["CARE"],["WEST"],["WATER"]],"market":[["SELL","WHEAT",9]]},{"farmer":["CARE"],"hands":[["NORTH"],["NORTH"],["CARE"],["WEST"],["WEST"],["WATER"],["HARVEST"],["COLLECT_FERTILIZER"],["SOUTH"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["FEED"],["COLLECT_FERTILIZER"],["FERTILIZE"],["WATER"],["WEST"],["PLANT","STRAWBERRY"],["HARVEST"],["FERTILIZE"],["PLANT","WHEAT"]],"market":[]},{"farmer":["HARVEST"],"hands":[["NORTH"],["CARE"],["HARVEST"],["WATER"],["SOUTH"],["WATER"],["WATER"],["WEST"],["WATER"],["WATER"]],"market":[["SELL","MILK",2],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["WATER"],["EAST"],["WEST"],["NORTH"],["WATER"],["WEST"],["WEST"],["FERTILIZE"],["NORTH"],["SOUTH"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["EAST"],["FEED"],["WEST"],["NORTH"],["SOUTH"],["WATER"],["WATER"],["WATER"],["WATER"],["WATER"]],"market":[]},{"farmer":["WATER"],"hands":[["WATER"],["CARE"],["WEST"],["FERTILIZE"],["WATER"],["HARVEST"],["NORTH"],["SOUTH"],["EAST"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["SOUTH"],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["DROP"],["WATER"],["SOUTH"],["PLANT","STRAWBERRY"],["WATER"],["WEST"],["EAST"],["PASS"]],"market":[["SELL","MILK",1]]},{"farmer":["WATER"],"hands":[["WATER"],["DROP"],["PASS"],["WEST"],["SOUTH"],["WATER"],["SOUTH"],["WEST"],["EAST"],["SOUTH"]],"market":[["SELL","EGG",8],["SELL","FERTILIZER",3]]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["FERTILIZE"],["PASS"],["PASS"],["WEST"],["PASS"],["WATER"],["PASS"]],"market":[["SELL","MELON",3],["SELL","FERTILIZER",2]]},{"farmer":["WEST"],"hands":[],"market":[["SELL","FERTILIZER",4],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",3],["PICKUP","WHEAT",4],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["NORTH"],["NORTH"],["SOUTH"],["SOUTH"]],"market":[["SELL","WOOL",1],["HIRE"],["HIRE"],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["NORTH"],["FEED"],["FEED"],["NORTH"],["WEST"],["NORTH"],["WATER"],["SOUTH"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3]],"market":[["SELL","WHEAT",2]]},{"farmer":["HARVEST"],"hands":[["FEED"],["CARE"],["CARE"],["NORTH"],["WEST"],["WATER"],["HARVEST"],["WEST"],["WEST"],["EAST"]],"market":[]},{"farmer":["EAST"],"hands":[["CARE"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FEED"],["WATER"],["EAST"],["PLANT","WHEAT"],["WATER"],["FEED"],["FEED"]],"market":[]},{"farmer":["EAST"],"hands":[["COLLECT_FERTILIZER"],["NORTH"],["HARVEST"],["CARE"],["HARVEST"],["WATER"],["WATER"],["WEST"],["CARE"],["CARE"]],"market":[["SELL","WHEAT",3],["SELL","MILK",1],["BUY_SEED","WHEAT",1]]},{"farmer":["EAST"],"hands":[["NORTH"],["EAST"],["WEST"],["COLLECT_FERTILIZER"],["PLANT","WHEAT"],["NORTH"],["WEST"],["WATER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"]],"market":[["SELL","EGG",4]]},{"farmer":["DROP"],"hands":[["FEED"],["FEED"],["FEED"],["NORTH"],["WATER"],["WATER"],["FEED"],["SOUTH"],["HARVEST"],["EAST"]],"market":[]},{"farmer":["PICKUP","WHEAT",3],"hands":[["CARE"],["CARE"],["CARE"],["NORTH"],["WEST"],["NORTH"],["CARE"],["SOUTH"],["WEST"],["FEED"]],"market":[]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WATER"],["FEED"],["WATER"],["COLLECT_FERTILIZER"],["WATER"],["FEED"],["CARE"]],"market":[["SELL","MILK",1]]},{"farmer":["CARE"],"hands":[["WEST"],["HARVEST"],["HARVEST"],["NORTH"],["CARE"],["EAST"],["HARVEST"],["HARVEST"],["CARE"],["COLLECT_FERTILIZER"]],"market":[["SELL","EGG",6]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["NORTH"],["WEST"],["WATER"],["COLLECT_FERTILIZER"],["WATER"],["WEST"],["PLANT","WHEAT"],["COLLECT_FERTILIZER"],["HARVEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["WEST"],["EAST"],["FEED"],["WEST"],["NORTH"],["EAST"],["WEST"],["WATER"],["WEST"],["EAST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["WATER"],["WATER"],["CARE"],["FERTILIZE"],["WATER"],["WATER"],["WATER"],["WEST"],["FEED"],["FEED"]],"market":[["SELL","MILK",1]]},{"farmer":["FEED"],"hands":[["NORTH"],["NORTH"],["COLLECT_FERTILIZER"],["WATER"],["HARVEST"],["EAST"],["SOUTH"],["WATER"],["CARE"],["CARE"]],"market":[["SELL","WHEAT",10]]},{"farmer":["CARE"],"hands":[["WATER"],["WATER"],["WEST"],["WEST"],["WEST"],["WATER"],["WATER"],["WEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FERTILIZE"],["EAST"],["WEST"],["WATER"],["WATER"],["SOUTH"],["WEST"],["DIG"],["WEST"],["HARVEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["WEST"],["WATER"],["WATER"],["WEST"],["NORTH"],["WATER"],["PLANT","WHEAT"],["PLANT","WHEAT"],["WATER"],["EAST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["FERTILIZE"],["SOUTH"],["HARVEST"],["WATER"],["WATER"],["SOUTH"],["WATER"],["WATER"],["NORTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FERTILIZE"],"hands":[["WATER"],["WATER"],["PLANT","WHEAT"],["WEST"],["FERTILIZE"],["WATER"],["SOUTH"],["WEST"],["WATER"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["NORTH"],["SOUTH"],["WATER"],["WATER"],["NORTH"],["SOUTH"],["SOUTH"],["WATER"],["HARVEST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["EAST"],"hands":[["WEST"],["WATER"],["SOUTH"],["WEST"],["WATER"],["WEST"],["NORTH"],["NORTH"],["PLANT","WHEAT"],["WEST"]],"market":[["SELL","MILK",1]]},{"farmer":["FERTILIZE"],"hands":[["HARVEST"],["WEST"],["FERTILIZE"],["HARVEST"],["HARVEST"],["WEST"],["EAST"],["WATER"],["WATER"],["WEST"]],"market":[["SELL","MELON",6]]},{"farmer":["WATER"],"hands":[["PASS"],["WATER"],["WATER"],["PASS"],["PASS"],["WATER"],["WATER"],["PASS"],["PASS"],["WATER"]],"market":[["SELL","MELON",3]]},{"farmer":["HARVEST"],"hands":[],"market":[["SELL","FERTILIZER",11],["SELL","EGG",9],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["DROP"],"hands":[["HARVEST"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["NORTH"],["NORTH"],["SOUTH"],["SOUTH"],["NORTH"]],"market":[["SELL","EGG",3],["HIRE"],["HIRE"]]},{"farmer":["PICKUP","WHEAT",4],"hands":[["DROP"],["FEED"],["NORTH"],["WEST"],["NORTH"],["WEST"],["SOUTH"],["NORTH"],["PICKUP","WHEAT",3],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",3],["CARE"],["EAST"],["HARVEST"],["WEST"],["COLLECT_FERTILIZER"],["SOUTH"],["WEST"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["FEED"],"hands":[["FEED"],["COLLECT_FERTILIZER"],["FEED"],["COLLECT_FERTILIZER"],["WEST"],["WEST"],["WEST"],["WATER"],["FEED"],["NORTH"]],"market":[]},{"farmer":["CARE"],"hands":[["CARE"],["WEST"],["CARE"],["NORTH"],["WEST"],["WATER"],["WATER"],["HARVEST"],["CARE"],["WATER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["FEED"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["SOUTH"],["SOUTH"],["PLANT","WHEAT"],["COLLECT_FERTILIZER"],["NORTH"]],"market":[["SELL","EGG",2]]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["CARE"],["HARVEST"],["WATER"],["NORTH"],["WATER"],["WATER"],["WATER"],["NORTH"],["WEST"]],"market":[]},{"farmer":["FEED"],"hands":[["HARVEST"],["COLLECT_FERTILIZER"],["EAST"],["HARVEST"],["WEST"],["WEST"],["NORTH"],["NORTH"],["FEED"],["WATER"]],"market":[["SELL","EGG",2]]},{"farmer":["CARE"],"hands":[["FEED"],["SOUTH"],["FEED"],["PLANT","WHEAT"],["WATER"],["WATER"],["WEST"],["WATER"],["CARE"],["HARVEST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["CARE"],["FEED"],["CARE"],["WATER"],["HARVEST"],["SOUTH"],["WATER"],["HARVEST"],["COLLECT_FERTILIZER"],["PLANT","WHEAT"]],"market":[["SELL","EGG",2],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["EAST"],["CARE"],["COLLECT_FERTILIZER"],["WEST"],["PLANT","WHEAT"],["SOUTH"],["SOUTH"],["PLANT","WHEAT"],["HARVEST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["FEED"],["SOUTH"],["EAST"],["WATER"],["WATER"],["WEST"],["WEST"],["WATER"],["SOUTH"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["CARE"],["WATER"],["FEED"],["WEST"],["WEST"],["FERTILIZE"],["DIG"],["SOUTH"],["SOUTH"],["WATER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["SOUTH"],["CARE"],["WATER"],["PLANT","WHEAT"],["WATER"],["PLANT","WHEAT"],["SOUTH"],["DROP"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["HARVEST"],["WEST"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"],["NORTH"],["WATER"],["FEED"],["PICKUP","WHEAT",3],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["NORTH"],["WATER"],["HARVEST"],["WATER"],["EAST"],["WATER"],["NORTH"],["CARE"],["FEED"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["WATER"],["NORTH"],["EAST"],["HARVEST"],["EAST"],["NORTH"],["WEST"],["SOUTH"],["CARE"],["WEST"]],"market":[["SELL","MILK",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["NORTH"],["FERTILIZE"],["EAST"],["WATER"],["NORTH"],["WATER"],["SOUTH"],["COLLECT_FERTILIZER"],["WATER"]],"market":[["SELL","WHEAT",10]]},{"farmer":["HARVEST"],"hands":[["WATER"],["NORTH"],["WATER"],["WATER"],["HARVEST"],["WATER"],["SOUTH"],["WEST"],["SOUTH"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["NORTH"],["WEST"],["NORTH"],["HARVEST"],["PLANT","WHEAT"],["EAST"],["WATER"],["FEED"],["NORTH"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["WATER"],["FERTILIZE"],["WATER"],["EAST"],["WATER"],["WATER"],["EAST"],["CARE"],["DROP"],["WATER"]],"market":[["SELL","MILK",2],["SELL","WOOL",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["EAST"],["WATER"],["NORTH"],["WATER"],["SOUTH"],["SOUTH"],["EAST"],["COLLECT_FERTILIZER"],["PASS"],["SOUTH"]],"market":[["SELL","MELON",7],["SELL","STRAWBERRY",2],["SELL","MILK",2],["SELL","FERTILIZER",2],["SELL","WHEAT",2]]},{"farmer":["PASS"],"hands":[["WATER"],["PASS"],["WATER"],["HARVEST"],["HARVEST"],["WEST"],["WATER"],["PASS"],["PASS"],["EAST"]],"market":[["SELL","MELON",3],["SELL","MILK",3],["SELL","FERTILIZER",1]]},{"farmer":["NORTH"],"hands":[],"market":[["SELL","MILK",4],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["PICKUP","WHEAT",3],["PICKUP","WHEAT",4],["PICKUP","WHEAT",3],["PICKUP","FERTILIZER",7],["WEST"],["EAST"],["SOUTH"],["PASS"]],"market":[["SELL","MILK",3],["HIRE"],["HIRE"],["BUY_PRODUCT","WHEAT",10]]},{"farmer":["NORTH"],"hands":[["FEED"],["FEED"],["FEED"],["NORTH"],["WEST"],["HARVEST"],["WATER"],["PICKUP","FERTILIZER",5],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3]],"market":[["SELL","EGG",9],["SELL","MILK",3],["SELL","FERTILIZER",5]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["CARE"],["CARE"],["CARE"],["NORTH"],["WEST"],["COLLECT_FERTILIZER"],["SOUTH"],["NORTH"],["WEST"],["NORTH"]],"market":[]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"],["EAST"],["WATER"],["NORTH"],["FEED"],["FEED"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["EAST"],["HARVEST"],["FERTILIZE"],["WATER"],["COLLECT_FERTILIZER"],["WEST"],["EAST"],["CARE"],["CARE"]],"market":[["SELL","MILK",1]]},{"farmer":["WEST"],"hands":[["WEST"],["CARE"],["WEST"],["WATER"],["HARVEST"],["HARVEST"],["WATER"],["EAST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"]],"market":[["SELL","EGG",4]]},{"farmer":["WEST"],"hands":[["FEED"],["FEED"],["FEED"],["NORTH"],["EAST"],["EAST"],["SOUTH"],["FERTILIZE"],["WEST"],["EAST"]],"market":[]},{"farmer":["WATER"],"hands":[["CARE"],["EAST"],["CARE"],["FERTILIZE"],["EAST"],["EAST"],["SOUTH"],["WATER"],["FEED"],["FEED"]],"market":[]},{"farmer":["HARVEST"],"hands":[["COLLECT_FERTILIZER"],["FEED"],["COLLECT_FERTILIZER"],["WATER"],["EAST"],["WATER"],["WATER"],["NORTH"],["CARE"],["CARE"]],"market":[["SELL","STRAWBERRY",2],["SELL","MILK",1]]},{"farmer":["PLANT","WHEAT"],"hands":[["WEST"],["CARE"],["HARVEST"],["NORTH"],["EAST"],["HARVEST"],["WEST"],["FERTILIZE"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"]],"market":[["SELL","EGG",3]]},{"farmer":["WATER"],"hands":[["FERTILIZE"],["EAST"],["WEST"],["FERTILIZE"],["DROP"],["PLANT","WHEAT"],["WEST"],["WATER"],["WEST"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["WATER"],["FEED"],["FEED"],["WATER"],["SOUTH"],["WATER"],["WEST"],["NORTH"],["HARVEST"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WEST"],["CARE"],["CARE"],["EAST"],["WEST"],["NORTH"],["WATER"],["FERTILIZE"],["FEED"],["FERTILIZE"]],"market":[["SELL","STRAWBERRY",2],["SELL","MILK",1]]},{"farmer":["EAST"],"hands":[["FEED"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FERTILIZE"],["WEST"],["FERTILIZE"],["HARVEST"],["WATER"],["CARE"],["WATER"]],"market":[["SELL","WHEAT",3]]},{"farmer":["WATER"],"hands":[["CARE"],["HARVEST"],["WEST"],["WATER"],["WEST"],["WATER"],["PLANT","WHEAT"],["EAST"],["COLLECT_FERTILIZER"],["NORTH"]],"market":[]},{"farmer":["EAST"],"hands":[["COLLECT_FERTILIZER"],["NORTH"],["WEST"],["EAST"],["WATER"],["NORTH"],["WATER"],["FERTILIZE"],["WEST"],["FERTILIZE"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["NORTH"],["FERTILIZE"],["FERTILIZE"],["FERTILIZE"],["HARVEST"],["FERTILIZE"],["EAST"],["WATER"],["PLANT","WHEAT"],["WATER"]],"market":[["SELL","MILK",1],["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["HARVEST"],["WATER"],["WATER"],["WATER"],["PLANT","WHEAT"],["WATER"],["WATER"],["EAST"],["WATER"],["SOUTH"]],"market":[["SELL","WHEAT",6],["BUY_SEED","WHEAT",1]]},{"farmer":["FERTILIZE"],"hands":[["SOUTH"],["NORTH"],["SOUTH"],["EAST"],["WATER"],["WEST"],["NORTH"],["FERTILIZE"],["NORTH"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["NORTH"],["FERTILIZE"],["WATER"],["FERTILIZE"],["SOUTH"],["WATER"],["WEST"],["WATER"],["FERTILIZE"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["WATER"],["NORTH"],["HARVEST"],["WATER"],["EAST"],["NORTH"],["WATER"],["NORTH"],["WATER"],["FEED"]],"market":[["SELL","STRAWBERRY",2],["SELL","MILK",1]]},{"farmer":["FERTILIZE"],"hands":[["EAST"],["NORTH"],["PLANT","WHEAT"],["EAST"],["EAST"],["NORTH"],["NORTH"],["WATER"],["SOUTH"],["CARE"]],"market":[["SELL","WHEAT",11]]},{"farmer":["WATER"],"hands":[["FERTILIZE"],["WEST"],["WATER"],["FERTILIZE"],["COLLECT_FERTILIZER"],["WEST"],["WATER"],["PASS"],["SOUTH"],["PASS"]],"market":[]},{"farmer":["PICKUP","WHEAT",3],"hands":[],"market":[["SELL","EGG",8],["SELL","FERTILIZER",6],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["NORTH"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"]],"market":[["SELL","EGG",5],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["EAST"],["FEED"],["NORTH"],["WEST"],["NORTH"],["SOUTH"],["NORTH"],["WEST"],["WEST"],["NORTH"]],"market":[["HIRE"]]},{"farmer":["CARE"],"hands":[["EAST"],["CARE"],["EAST"],["WEST"],["HARVEST"],["FERTILIZE"],["EAST"],["WEST"],["COLLECT_FERTILIZER"],["EAST"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["HARVEST"],["WEST"],["EAST"],["WEST"],["NORTH"],["WATER"],["EAST"],["WATER"],["WEST"],["EAST"],["HARVEST"]],"market":[["SELL","MELON",6]]},{"farmer":["NORTH"],"hands":[["NORTH"],["FEED"],["FEED"],["FEED"],["HARVEST"],["SOUTH"],["EAST"],["HARVEST"],["COLLECT_FERTILIZER"],["EAST"],["PLACE","MILK",3]],"market":[["SELL","MELON",8],["SELL","MILK",1]]},{"farmer":["FEED"],"hands":[["HARVEST"],["CARE"],["CARE"],["CARE"],["EAST"],["SOUTH"],["HARVEST"],["PLANT","WHEAT"],["SOUTH"],["HARVEST"],["PICKUP","WHEAT",3]],"market":[]},{"farmer":["CARE"],"hands":[["WEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["HARVEST"],["WATER"],["NORTH"],["WATER"],["WEST"],["NORTH"],["FEED"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["HARVEST"],["SOUTH"],["EAST"],["NORTH"],["NORTH"],["SOUTH"],["HARVEST"],["WEST"],["WEST"],["HARVEST"],["CARE"]],"market":[]},{"farmer":["HARVEST"],"hands":[["SOUTH"],["FEED"],["FEED"],["COLLECT_FERTILIZER"],["HARVEST"],["WATER"],["SOUTH"],["FEED"],["WATER"],["NORTH"],["NORTH"]],"market":[["SELL","STRAWBERRY",2],["SELL","MILK",1]]},{"farmer":["NORTH"],"hands":[["SOUTH"],["CARE"],["CARE"],["HARVEST"],["WEST"],["NORTH"],["SOUTH"],["CARE"],["HARVEST"],["HARVEST"],["WEST"]],"market":[]},{"farmer":["WATER"],"hands":[["WEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["NORTH"],["HARVEST"],["WEST"],["WEST"],["WEST"],["PLANT","WHEAT"],["WEST"],["FEED"]],"market":[]},{"farmer":["NORTH"],"hands":[["DROP"],["HARVEST"],["HARVEST"],["FERTILIZE"],["SOUTH"],["WATER"],["WEST"],["WATER"],["WATER"],["HARVEST"],["CARE"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["PICKUP","WHEAT",3],["WEST"],["NORTH"],["WATER"],["SOUTH"],["WEST"],["WEST"],["HARVEST"],["SOUTH"],["SOUTH"],["COLLECT_FERTILIZER"]],"market":[["SELL","STRAWBERRY",6],["SELL","EGG",5],["SELL","MILK",1]]},{"farmer":["WEST"],"hands":[["FEED"],["WATER"],["EAST"],["NORTH"],["SOUTH"],["WATER"],["DROP"],["PLANT","WHEAT"],["SOUTH"],["SOUTH"],["HARVEST"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["CARE"],["SOUTH"],["HARVEST"],["NORTH"],["SOUTH"],["NORTH"],["PICKUP","WHEAT",3],["WATER"],["FERTILIZE"],["SOUTH"],["NORTH"]],"market":[["SELL","STRAWBERRY",4],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["COLLECT_FERTILIZER"],["WATER"],["NORTH"],["WATER"],["DROP"],["WATER"],["NORTH"],["SOUTH"],["WATER"],["WEST"],["FERTILIZE"]],"market":[]},{"farmer":["SOUTH"],"hands":[["EAST"],["SOUTH"],["HARVEST"],["WEST"],["NORTH"],["WEST"],["FEED"],["SOUTH"],["SOUTH"],["WEST"],["WATER"]],"market":[["SELL","MILK",1]]},{"farmer":["FERTILIZE"],"hands":[["FEED"],["SOUTH"],["NORTH"],["FERTILIZE"],["NORTH"],["WATER"],["CARE"],["EAST"],["SOUTH"],["DROP"],["WEST"]],"market":[]},{"farmer":["WATER"],"hands":[["CARE"],["FERTILIZE"],["HARVEST"],["WATER"],["NORTH"],["NORTH"],["COLLECT_FERTILIZER"],["EAST"],["EAST"],["HARVEST"],["WATER"]],"market":[]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["WATER"],["NORTH"],["SOUTH"],["NORTH"],["WATER"],["HARVEST"],["FEED"],["FERTILIZE"],["PLACE","MILK",3],["NORTH"]],"market":[]},{"farmer":["HARVEST"],"hands":[["NORTH"],["EAST"],["HARVEST"],["HARVEST"],["EAST"],["SOUTH"],["EAST"],["CARE"],["WATER"],["NORTH"],["NORTH"]],"market":[["SELL","STRAWBERRY",14]]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["FERTILIZE"],["WEST"],["EAST"],["EAST"],["SOUTH"],["FEED"],["COLLECT_FERTILIZER"],["NORTH"],["EAST"],["WATER"]],"market":[["SELL","WHEAT",8]]},{"farmer":["WATER"],"hands":[["HARVEST"],["WATER"],["HARVEST"],["HARVEST"],["HARVEST"],["WATER"],["CARE"],["PASS"],["WATER"],["PASS"],["PASS"]],"market":[]},{"farmer":["PICKUP","WHEAT",3],"hands":[],"market":[["SELL","STRAWBERRY",9],["SELL","FERTILIZER",4],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["PICKUP","WHEAT",4],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["EAST"],["SOUTH"],["PASS"],["NORTH"]],"market":[["SELL","WOOL",1],["HIRE"],["HIRE"]]},{"farmer":["CARE"],"hands":[["FEED"],["FEED"],["NORTH"],["WEST"],["EAST"],["WATER"],["PICKUP","FERTILIZER",3],["NORTH"],["NORTH"],["WEST"]],"market":[["SELL","EGG",7],["SELL","FERTILIZER",4],["HIRE"]]},{"farmer":["NORTH"],"hands":[["CARE"],["CARE"],["NORTH"],["FEED"],["HARVEST"],["HARVEST"],["WEST"],["WEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FEED"],["CARE"],["COLLECT_FERTILIZER"],["PLANT","WHEAT"],["WEST"],["WATER"],["NORTH"],["HARVEST"],["PICKUP","WHEAT",3]],"market":[]},{"farmer":["CARE"],"hands":[["EAST"],["HARVEST"],["CARE"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"],["WEST"],["HARVEST"],["WATER"],["SOUTH"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FEED"],["WEST"],["EAST"],["HARVEST"],["WATER"],["SOUTH"],["WEST"],["PLANT","WHEAT"],["NORTH"],["SOUTH"],["WEST"]],"market":[["SELL","EGG",5]]},{"farmer":["HARVEST"],"hands":[["CARE"],["FEED"],["FEED"],["WEST"],["EAST"],["WATER"],["FERTILIZE"],["WATER"],["WATER"],["WATER"],["FEED"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["COLLECT_FERTILIZER"],["CARE"],["CARE"],["FEED"],["WATER"],["SOUTH"],["WATER"],["WEST"],["NORTH"],["SOUTH"],["CARE"]],"market":[]},{"farmer":["FEED"],"hands":[["HARVEST"],["SOUTH"],["COLLECT_FERTILIZER"],["CARE"],["EAST"],["SOUTH"],["SOUTH"],["WATER"],["WATER"],["SOUTH"],["COLLECT_FERTILIZER"]],"market":[["SELL","STRAWBERRY",2],["SELL","MILK",1]]},{"farmer":["CARE"],"hands":[["EAST"],["FEED"],["HARVEST"],["COLLECT_FERTILIZER"],["WATER"],["NORTH"],["WEST"],["HARVEST"],["WEST"],["WATER"],["WEST"]],"market":[["SELL","EGG",4]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FEED"],["CARE"],["NORTH"],["HARVEST"],["NORTH"],["WEST"],["FERTILIZE"],["PLANT","WHEAT"],["FERTILIZE"],["HARVEST"],["WEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["CARE"],["COLLECT_FERTILIZER"],["WATER"],["WEST"],["WATER"],["WATER"],["WATER"],["WATER"],["WATER"],["PLANT","WHEAT"],["FEED"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FERTILIZE"],"hands":[["EAST"],["WEST"],["NORTH"],["HARVEST"],["NORTH"],["WEST"],["SOUTH"],["WEST"],["WEST"],["WATER"],["CARE"]],"market":[["SELL","MILK",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["FEED"],["WATER"],["WATER"],["FEED"],["WATER"],["WATER"],["WATER"],["WATER"],["WATER"],["NORTH"],["COLLECT_FERTILIZER"]],"market":[["SELL","WHEAT",7]]},{"farmer":["WEST"],"hands":[["CARE"],["WEST"],["NORTH"],["CARE"],["NORTH"],["SOUTH"],["HARVEST"],["HARVEST"],["HARVEST"],["NORTH"],["NORTH"]],"market":[["BUY_SEED","WHEAT",3],["BUY_SEED","TOMATO",1]]},{"farmer":["WATER"],"hands":[["COLLECT_FERTILIZER"],["WATER"],["WATER"],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["PLANT","WHEAT"],["NORTH"],["PLANT","WHEAT"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["HARVEST"],"hands":[["HARVEST"],["NORTH"],["EAST"],["WEST"],["WEST"],["WEST"],["WATER"],["WATER"],["WATER"],["NORTH"],["FERTILIZE"]],"market":[["SELL","STRAWBERRY",3],["SELL","MILK",1],["BUY_SEED","WHEAT",1],["BUY_SEED","TOMATO",1]]},{"farmer":["PLANT","WHEAT"],"hands":[["EAST"],["EAST"],["WATER"],["FERTILIZE"],["WATER"],["WATER"],["SOUTH"],["NORTH"],["WEST"],["EAST"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WATER"],["EAST"],["SOUTH"],["WATER"],["SOUTH"],["HARVEST"],["SOUTH"],["WATER"],["SOUTH"],["DROP"],["FERTILIZE"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","TOMATO",1]]},{"farmer":["WEST"],"hands":[["NORTH"],["EAST"],["WATER"],["NORTH"],["WATER"],["PLANT","TOMATO"],["FERTILIZE"],["HARVEST"],["WATER"],["PICKUP","WHEAT",1],["WATER"]],"market":[["SELL","WHEAT",6],["SELL","EGG",4]]},{"farmer":["FERTILIZE"],"hands":[["NORTH"],["DROP"],["SOUTH"],["NORTH"],["SOUTH"],["WATER"],["WATER"],["PLANT","TOMATO"],["NORTH"],["WEST"],["NORTH"]],"market":[["SELL","STRAWBERRY",4],["SELL","MILK",1]]},{"farmer":["NORTH"],"hands":[["WEST"],["PASS"],["WATER"],["FERTILIZE"],["WATER"],["NORTH"],["NORTH"],["WATER"],["WATER"],["WEST"],["WATER"]],"market":[["SELL","EGG",4],["SELL","FERTILIZER",3]]},{"farmer":["PASS"],"hands":[["FERTILIZE"],["PASS"],["PASS"],["WATER"],["WEST"],["WATER"],["WATER"],["PASS"],["PASS"],["COLLECT_FERTILIZER"],["PASS"]],"market":[["SELL","WOOL",1]]},{"farmer":["PICKUP","WHEAT",3],"hands":[],"market":[["SELL","WOOL",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["NORTH"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["NORTH"],["SOUTH"],["NORTH"],["NORTH"]],"market":[["SELL","MILK",3],["SELL","WOOL",1],["HIRE"],["HIRE"],["HIRE"],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["NORTH"],["FEED"],["NORTH"],["WEST"],["NORTH"],["SOUTH"],["NORTH"],["COLLECT_FERTILIZER"],["WEST"],["EAST"],["PICKUP","FERTILIZER",6]],"market":[["SELL","WHEAT",14],["SELL","FERTILIZER",7]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["EAST"],["CARE"],["EAST"],["WEST"],["HARVEST"],["SOUTH"],["EAST"],["NORTH"],["COLLECT_FERTILIZER"],["EAST"],["SOUTH"]],"market":[]},{"farmer":["WEST"],"hands":[["HARVEST"],["COLLECT_FERTILIZER"],["FEED"],["WEST"],["NORTH"],["WATER"],["EAST"],["COLLECT_FERTILIZER"],["WEST"],["EAST"],["SOUTH"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["NORTH"],["WEST"],["CARE"],["FEED"],["HARVEST"],["SOUTH"],["HARVEST"],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"]],"market":[]},{"farmer":["WATER"],"hands":[["HARVEST"],["FEED"],["COLLECT_FERTILIZER"],["CARE"],["NORTH"],["WATER"],["NORTH"],["WATER"],["WEST"],["HARVEST"],["FERTILIZE"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["CARE"],["EAST"],["COLLECT_FERTILIZER"],["HARVEST"],["WEST"],["HARVEST"],["HARVEST"],["WEST"],["NORTH"],["WATER"]],"market":[["BUY_SEED","TOMATO",1]]},{"farmer":["WEST"],"hands":[["HARVEST"],["COLLECT_FERTILIZER"],["FEED"],["NORTH"],["SOUTH"],["WEST"],["NORTH"],["PLANT","TOMATO"],["WATER"],["HARVEST"],["SOUTH"]],"market":[]},{"farmer":["WATER"],"hands":[["SOUTH"],["WEST"],["CARE"],["FEED"],["SOUTH"],["WATER"],["HARVEST"],["WATER"],["HARVEST"],["NORTH"],["FERTILIZE"]],"market":[["SELL","MILK",1]]},{"farmer":["NORTH"],"hands":[["SOUTH"],["FEED"],["COLLECT_FERTILIZER"],["CARE"],["SOUTH"],["HARVEST"],["SOUTH"],["NORTH"],["PLANT","WHEAT"],["HARVEST"],["WATER"]],"market":[["SELL","STRAWBERRY",2],["SELL","WHEAT",4]]},{"farmer":["HARVEST"],"hands":[["SOUTH"],["CARE"],["EAST"],["COLLECT_FERTILIZER"],["SOUTH"],["PLANT","WHEAT"],["SOUTH"],["WATER"],["WATER"],["NORTH"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["EAST"],"hands":[["SOUTH"],["COLLECT_FERTILIZER"],["FEED"],["HARVEST"],["DROP"],["WATER"],["SOUTH"],["HARVEST"],["SOUTH"],["HARVEST"],["WEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","TOMATO",1]]},{"farmer":["HARVEST"],"hands":[["WEST"],["SOUTH"],["CARE"],["WEST"],["NORTH"],["WEST"],["WEST"],["PLANT","TOMATO"],["FERTILIZE"],["WEST"],["FERTILIZE"]],"market":[["SELL","STRAWBERRY",6],["SELL","MILK",1]]},{"farmer":["SOUTH"],"hands":[["DROP"],["WATER"],["COLLECT_FERTILIZER"],["FERTILIZE"],["NORTH"],["WEST"],["WEST"],["WATER"],["WATER"],["HARVEST"],["WATER"]],"market":[["SELL","WHEAT",6],["SELL","EGG",5]]},{"farmer":["SOUTH"],"hands":[["PICKUP","WHEAT",3],["SOUTH"],["EAST"],["WATER"],["NORTH"],["WATER"],["DROP"],["WEST"],["EAST"],["SOUTH"],["NORTH"]],"market":[["SELL","STRAWBERRY",6]]},{"farmer":["SOUTH"],"hands":[["FEED"],["FERTILIZE"],["FERTILIZE"],["NORTH"],["EAST"],["HARVEST"],["COLLECT_FERTILIZER"],["WEST"],["WATER"],["SOUTH"],["FERTILIZE"]],"market":[["SELL","STRAWBERRY",6]]},{"farmer":["EAST"],"hands":[["CARE"],["WATER"],["WATER"],["WATER"],["EAST"],["PLANT","TOMATO"],["NORTH"],["WATER"],["SOUTH"],["SOUTH"],["WATER"]],"market":[["SELL","MILK",1]]},{"farmer":["EAST"],"hands":[["NORTH"],["SOUTH"],["NORTH"],["HARVEST"],["EAST"],["WATER"],["COLLECT_FERTILIZER"],["HARVEST"],["EAST"],["SOUTH"],["NORTH"]],"market":[["SELL","EGG",7],["SELL","WHEAT",7]]},{"farmer":["DROP"],"hands":[["FEED"],["FERTILIZE"],["HARVEST"],["PLANT","WHEAT"],["EAST"],["NORTH"],["HARVEST"],["PLANT","WHEAT"],["EAST"],["WEST"],["FERTILIZE"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PICKUP","WHEAT",1],"hands":[["CARE"],["WATER"],["NORTH"],["WATER"],["HARVEST"],["WATER"],["EAST"],["WATER"],["FEED"],["WEST"],["WATER"]],"market":[["SELL","STRAWBERRY",4],["SELL","WHEAT",3],["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["EAST"],["NORTH"],["HARVEST"],["NORTH"],["NORTH"],["SOUTH"],["COLLECT_FERTILIZER"],["WEST"],["CARE"],["DROP"],["WEST"]],"market":[["SELL","MILK",1]]},{"farmer":["CARE"],"hands":[["FEED"],["NORTH"],["FERTILIZE"],["HARVEST"],["HARVEST"],["EAST"],["EAST"],["WEST"],["COLLECT_FERTILIZER"],["HARVEST"],["WATER"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["CARE"],["SOUTH"],["WATER"],["WATER"],["WATER"],["WATER"],["FERTILIZE"],["HARVEST"],["PASS"],["PASS"],["PASS"]],"market":[["SELL","STRAWBERRY",2],["SELL","MILK",1],["SELL","WOOL",1]]},{"farmer":["PICKUP","WHEAT",3],"hands":[],"market":[["SELL","STRAWBERRY",3],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["PICKUP","WHEAT",4],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["EAST"],["SOUTH"],["PASS"],["NORTH"]],"market":[["SELL","MILK",2],["SELL","WOOL",1],["HIRE"],["HIRE"],["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["FEED"],["FEED"],["NORTH"],["WEST"],["EAST"],["WEST"],["PICKUP","FERTILIZER",9],["WEST"],["NORTH"],["COLLECT_FERTILIZER"]],"market":[["SELL","FERTILIZER",11],["SELL","WHEAT",8],["HIRE"]]},{"farmer":["NORTH"],"hands":[["CARE"],["CARE"],["NORTH"],["FEED"],["HARVEST"],["WEST"],["NORTH"],["WEST"],["COLLECT_FERTILIZER"],["SOUTH"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["HARVEST"],["FEED"],["CARE"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["WATER"],["NORTH"],["FERTILIZE"],["PICKUP","WHEAT",3]],"market":[]},{"farmer":["CARE"],"hands":[["EAST"],["WEST"],["CARE"],["COLLECT_FERTILIZER"],["EAST"],["HARVEST"],["NORTH"],["HARVEST"],["WATER"],["WATER"],["NORTH"]],"market":[["SELL","MILK",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FEED"],["FEED"],["EAST"],["WEST"],["EAST"],["SOUTH"],["FERTILIZE"],["PLANT","WHEAT"],["NORTH"],["SOUTH"],["WEST"]],"market":[["SELL","WHEAT",4]]},{"farmer":["NORTH"],"hands":[["CARE"],["CARE"],["FEED"],["FEED"],["WATER"],["HARVEST"],["EAST"],["WATER"],["WATER"],["WATER"],["FEED"]],"market":[]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["CARE"],["CARE"],["HARVEST"],["EAST"],["FERTILIZE"],["WEST"],["NORTH"],["SOUTH"],["CARE"]],"market":[]},{"farmer":["CARE"],"hands":[["HARVEST"],["HARVEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["PLANT","WHEAT"],["HARVEST"],["WATER"],["FEED"],["WATER"],["WEST"],["COLLECT_FERTILIZER"]],"market":[["SELL","MILK",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["EAST"],["WEST"],["HARVEST"],["WEST"],["WATER"],["EAST"],["NORTH"],["CARE"],["FERTILIZE"],["WATER"],["NORTH"]],"market":[["SELL","WHEAT",4]]},{"farmer":["HARVEST"],"hands":[["FEED"],["FEED"],["EAST"],["HARVEST"],["NORTH"],["HARVEST"],["FERTILIZE"],["COLLECT_FERTILIZER"],["WEST"],["HARVEST"],["FERTILIZE"]],"market":[]},{"farmer":["NORTH"],"hands":[["CARE"],["CARE"],["WATER"],["FEED"],["WATER"],["NORTH"],["WATER"],["NORTH"],["WEST"],["SOUTH"],["WATER"]],"market":[]},{"farmer":["EAST"],"hands":[["EAST"],["COLLECT_FERTILIZER"],["EAST"],["CARE"],["NORTH"],["NORTH"],["NORTH"],["HARVEST"],["WATER"],["WATER"],["WEST"]],"market":[["SELL","MILK",1]]},{"farmer":["FERTILIZE"],"hands":[["FEED"],["WEST"],["WATER"],["COLLECT_FERTILIZER"],["WATER"],["EAST"],["FERTILIZE"],["DIG"],["WEST"],["NORTH"],["FERTILIZE"]],"market":[["SELL","WHEAT",3]]},{"farmer":["EAST"],"hands":[["CARE"],["WATER"],["NORTH"],["SOUTH"],["NORTH"],["DROP"],["WATER"],["PLANT","WHEAT"],["WEST"],["WEST"],["WATER"]],"market":[]},{"farmer":["EAST"],"hands":[["COLLECT_FERTILIZER"],["HARVEST"],["WATER"],["WEST"],["WATER"],["PICKUP","WHEAT",1],["EAST"],["WATER"],["WATER"],["WATER"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["HARVEST"],["PLANT","WHEAT"],["WEST"],["WATER"],["FERTILIZE"],["SOUTH"],["FERTILIZE"],["SOUTH"],["WEST"],["WEST"],["WATER"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["NORTH"],["WATER"],["FERTILIZE"],["SOUTH"],["NORTH"],["WEST"],["EAST"],["WEST"],["PLANT","WHEAT"],["HARVEST"],["EAST"]],"market":[["SELL","EGG",8],["SELL","WHEAT",5],["BUY_SEED","WHEAT",1]]},{"farmer":["EAST"],"hands":[["FERTILIZE"],["SOUTH"],["WATER"],["WATER"],["WATER"],["FEED"],["FERTILIZE"],["WATER"],["WATER"],["WEST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["EAST"],["WATER"],["NORTH"],["HARVEST"],["WEST"],["CARE"],["SOUTH"],["HARVEST"],["SOUTH"],["WATER"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["FERTILIZE"],["SOUTH"],["NORTH"],["PLANT","WHEAT"],["WATER"],["COLLECT_FERTILIZER"],["FERTILIZE"],["PLANT","WHEAT"],["WATER"],["EAST"],["WEST"]],"market":[["SELL","STRAWBERRY",19],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["NORTH"],["WEST"],["WATER"],["WATER"],["WEST"],["HARVEST"],["NORTH"],["WATER"],["EAST"],["WATER"],["WATER"]],"market":[]},{"farmer":["PASS"],"hands":[["NORTH"],["WATER"],["PASS"],["PASS"],["PASS"],["PASS"],["EAST"],["PASS"],["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["PICKUP","WHEAT",3],"hands":[],"market":[["SELL","FERTILIZER",10],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["NORTH"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["NORTH"],["WEST"],["NORTH"],["NORTH"]],"market":[["SELL","MILK",2],["SELL","WOOL",1],["HIRE"],["HIRE"],["HIRE"],["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["NORTH"],["FEED"],["NORTH"],["WEST"],["NORTH"],["WEST"],["NORTH"],["NORTH"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["CARE"],"hands":[["EAST"],["CARE"],["EAST"],["WEST"],["HARVEST"],["HARVEST"],["EAST"],["WEST"],["COLLECT_FERTILIZER"],["EAST"],["SOUTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["HARVEST"],["WEST"],["FEED"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["EAST"],["WATER"],["WEST"],["EAST"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["FEED"],["CARE"],["FEED"],["HARVEST"],["SOUTH"],["HARVEST"],["HARVEST"],["COLLECT_FERTILIZER"],["EAST"],["HARVEST"]],"market":[["SELL","MILK",1]]},{"farmer":["FEED"],"hands":[["HARVEST"],["CARE"],["COLLECT_FERTILIZER"],["CARE"],["SOUTH"],["WATER"],["NORTH"],["PLANT","WHEAT"],["WEST"],["HARVEST"],["PLANT","WHEAT"]],"market":[]},{"farmer":["CARE"],"hands":[["SOUTH"],["COLLECT_FERTILIZER"],["EAST"],["COLLECT_FERTILIZER"],["SOUTH"],["SOUTH"],["HARVEST"],["WATER"],["WEST"],["NORTH"],["WATER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["SOUTH"],["SOUTH"],["FEED"],["NORTH"],["SOUTH"],["WATER"],["SOUTH"],["WEST"],["FERTILIZE"],["HARVEST"],["SOUTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["SOUTH"],["FEED"],["CARE"],["FEED"],["DROP"],["WEST"],["SOUTH"],["WATER"],["WATER"],["NORTH"],["SOUTH"]],"market":[["SELL","STRAWBERRY",6],["SELL","MILK",1]]},{"farmer":["WATER"],"hands":[["WEST"],["CARE"],["COLLECT_FERTILIZER"],["CARE"],["NORTH"],["WATER"],["WEST"],["HARVEST"],["SOUTH"],["HARVEST"],["WATER"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["NORTH"],"hands":[["DROP"],["COLLECT_FERTILIZER"],["EAST"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"],["WEST"],["PLANT","WHEAT"],["WATER"],["SOUTH"],["SOUTH"]],"market":[]},{"farmer":["WATER"],"hands":[["PICKUP","WHEAT",3],["SOUTH"],["FEED"],["HARVEST"],["NORTH"],["FERTILIZE"],["DROP"],["WATER"],["HARVEST"],["SOUTH"],["WATER"]],"market":[["SELL","STRAWBERRY",4],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["FEED"],["WATER"],["CARE"],["NORTH"],["NORTH"],["WATER"],["COLLECT_FERTILIZER"],["NORTH"],["PLANT","WHEAT"],["SOUTH"],["WEST"]],"market":[["SELL","STRAWBERRY",4],["SELL","MILK",1]]},{"farmer":["FERTILIZE"],"hands":[["CARE"],["SOUTH"],["COLLECT_FERTILIZER"],["WEST"],["HARVEST"],["SOUTH"],["WEST"],["WEST"],["WATER"],["WEST"],["FERTILIZE"]],"market":[["SELL","EGG",10],["SELL","WHEAT",6],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["NORTH"],["WATER"],["HARVEST"],["FERTILIZE"],["EAST"],["SOUTH"],["COLLECT_FERTILIZER"],["HARVEST"],["SOUTH"],["WEST"],["WATER"]],"market":[]},{"farmer":["SOUTH"],"hands":[["FEED"],["SOUTH"],["NORTH"],["WATER"],["HARVEST"],["WATER"],["HARVEST"],["DIG"],["EAST"],["WEST"],["WEST"]],"market":[["BUY_SEED","CARROT",2]]},{"farmer":["FERTILIZE"],"hands":[["CARE"],["WEST"],["EAST"],["NORTH"],["EAST"],["EAST"],["PLACE","MILK",6],["PLANT","CARROT"],["WATER"],["DROP"],["WEST"]],"market":[["SELL","MILK",1]]},{"farmer":["WATER"],"hands":[["COLLECT_FERTILIZER"],["FERTILIZE"],["HARVEST"],["NORTH"],["HARVEST"],["WATER"],["PICKUP","WHEAT",2],["WATER"],["NORTH"],["PICKUP","WHEAT",2],["NORTH"]],"market":[]},{"farmer":["WEST"],"hands":[["HARVEST"],["WATER"],["NORTH"],["EAST"],["EAST"],["NORTH"],["FEED"],["WEST"],["FERTILIZE"],["NORTH"],["WATER"]],"market":[]},{"farmer":["HARVEST"],"hands":[["EAST"],["NORTH"],["HARVEST"],["EAST"],["WATER"],["WEST"],["CARE"],["HARVEST"],["WATER"],["EAST"],["WEST"]],"market":[["SELL","WHEAT",5]]},{"farmer":["DIG"],"hands":[["COLLECT_FERTILIZER"],["WATER"],["DIG"],["FERTILIZE"],["HARVEST"],["WATER"],["NORTH"],["DIG"],["SOUTH"],["FEED"],["WATER"]],"market":[["SELL","MILK",2]]},{"farmer":["PLANT","WHEAT"],"hands":[["EAST"],["NORTH"],["PLANT","CARROT"],["WATER"],["EAST"],["NORTH"],["WEST"],["PLANT","WHEAT"],["WEST"],["CARE"],["NORTH"]],"market":[["SELL","EGG",18]]},{"farmer":["WATER"],"hands":[["FERTILIZE"],["EAST"],["WATER"],["PASS"],["HARVEST"],["NORTH"],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["PASS"],["NORTH"]],"market":[]},{"farmer":["PICKUP","WHEAT",3],"hands":[],"market":[["SELL","MILK",3],["SELL","WOOL",4],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["PICKUP","WHEAT",4],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["EAST"],["WEST"],["PASS"],["NORTH"]],"market":[["SELL","WOOL",2],["HIRE"],["HIRE"]]},{"farmer":["CARE"],"hands":[["FEED"],["FEED"],["NORTH"],["WEST"],["EAST"],["HARVEST"],["PICKUP","FERTILIZER",5],["COLLECT_FERTILIZER"],["NORTH"],["SOUTH"]],"market":[["SELL","FERTILIZER",8]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["CARE"],["CARE"],["NORTH"],["FEED"],["HARVEST"],["COLLECT_FERTILIZER"],["SOUTH"],["NORTH"],["COLLECT_FERTILIZER"],["SOUTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FEED"],["CARE"],["COLLECT_FERTILIZER"],["WEST"],["SOUTH"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"]],"market":[]},{"farmer":["WEST"],"hands":[["EAST"],["HARVEST"],["CARE"],["COLLECT_FERTILIZER"],["NORTH"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["WATER"],["SOUTH"]],"market":[["SELL","MILK",1]]},{"farmer":["FEED"],"hands":[["FEED"],["WEST"],["EAST"],["WEST"],["WATER"],["WEST"],["FERTILIZE"],["WEST"],["NORTH"],["SOUTH"]],"market":[]},{"farmer":["CARE"],"hands":[["CARE"],["FEED"],["FEED"],["FEED"],["EAST"],["WATER"],["SOUTH"],["WATER"],["WATER"],["WEST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["CARE"],["CARE"],["CARE"],["WATER"],["SOUTH"],["FERTILIZE"],["HARVEST"],["NORTH"],["WATER"]],"market":[]},{"farmer":["HARVEST"],"hands":[["HARVEST"],["SOUTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["EAST"],["HARVEST"],["WATER"],["PLANT","WHEAT"],["WATER"],["HARVEST"]],"market":[["SELL","MILK",1]]},{"farmer":["WEST"],"hands":[["EAST"],["FEED"],["HARVEST"],["WEST"],["WATER"],["WEST"],["SOUTH"],["WATER"],["WEST"],["PLANT","WHEAT"]],"market":[["SELL","WHEAT",5],["BUY_SEED","WHEAT",1]]},{"farmer":["FERTILIZE"],"hands":[["FEED"],["CARE"],["NORTH"],["HARVEST"],["NORTH"],["FERTILIZE"],["FERTILIZE"],["NORTH"],["WATER"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["CARE"],["COLLECT_FERTILIZER"],["WATER"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"],["WATER"],["WATER"],["WEST"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["EAST"],["HARVEST"],["NORTH"],["WEST"],["WATER"],["SOUTH"],["WEST"],["HARVEST"],["WEST"],["WATER"]],"market":[["SELL","MILK",1],["BUY_SEED","WHEAT",1],["BUY_SEED","CARROT",2]]},{"farmer":["FEED"],"hands":[["FEED"],["WEST"],["WATER"],["WATER"],["HARVEST"],["WATER"],["NORTH"],["PLANT","WHEAT"],["WATER"],["HARVEST"]],"market":[["SELL","WHEAT",5]]},{"farmer":["CARE"],"hands":[["CARE"],["FERTILIZE"],["NORTH"],["HARVEST"],["NORTH"],["HARVEST"],["WEST"],["WATER"],["HARVEST"],["PLANT","CARROT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["WATER"],["WATER"],["PLANT","WHEAT"],["FERTILIZE"],["PLANT","WHEAT"],["WEST"],["SOUTH"],["PLANT","CARROT"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["EAST"],["NORTH"],["EAST"],["WATER"],["WATER"],["WATER"],["WEST"],["SOUTH"],["WATER"],["WEST"]],"market":[["SELL","MILK",2],["BUY_SEED","WHEAT",1]]},{"farmer":["FERTILIZE"],"hands":[["FERTILIZE"],["EAST"],["WATER"],["NORTH"],["WEST"],["NORTH"],["FERTILIZE"],["EAST"],["WEST"],["WATER"]],"market":[["SELL","EGG",10]]},{"farmer":["WATER"],"hands":[["WATER"],["EAST"],["SOUTH"],["FERTILIZE"],["WATER"],["EAST"],["WATER"],["FEED"],["WATER"],["NORTH"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["DROP"],["WATER"],["WATER"],["SOUTH"],["WATER"],["EAST"],["CARE"],["WEST"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["NORTH"],["SOUTH"],["SOUTH"],["NORTH"],["WATER"],["SOUTH"],["FERTILIZE"],["WEST"],["FERTILIZE"],["EAST"]],"market":[["SELL","STRAWBERRY",3],["SELL","MILK",2],["SELL","WOOL",3]]},{"farmer":["NORTH"],"hands":[["WEST"],["SOUTH"],["WATER"],["NORTH"],["SOUTH"],["WATER"],["WATER"],["FERTILIZE"],["WATER"],["EAST"]],"market":[["SELL","EGG",8],["SELL","FERTILIZER",1]]},{"farmer":["FERTILIZE"],"hands":[["FERTILIZE"],["WEST"],["PASS"],["WATER"],["WATER"],["PASS"],["PASS"],["WATER"],["PASS"],["HARVEST"]],"market":[["SELL","STRAWBERRY",3],["SELL","WOOL",3]]},{"farmer":["PICKUP","WHEAT",3],"hands":[],"market":[["SELL","MILK",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["NORTH"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["NORTH"],["PICKUP","FERTILIZER",3],["NORTH"],["NORTH"]],"market":[["SELL","MILK",1],["HIRE"],["HIRE"],["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["NORTH"],["FEED"],["NORTH"],["WEST"],["NORTH"],["SOUTH"],["NORTH"],["WEST"],["WEST"],["COLLECT_FERTILIZER"]],"market":[["SELL","WHEAT",9],["SELL","FERTILIZER",3],["HIRE"]]},{"farmer":["CARE"],"hands":[["EAST"],["CARE"],["EAST"],["WEST"],["HARVEST"],["FERTILIZE"],["EAST"],["WEST"],["COLLECT_FERTILIZER"],["EAST"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["HARVEST"],["COLLECT_FERTILIZER"],["FEED"],["WEST"],["DIG"],["WATER"],["EAST"],["WATER"],["WEST"],["EAST"],["NORTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["EAST"],["WEST"],["CARE"],["FEED"],["PLANT","WHEAT"],["SOUTH"],["HARVEST"],["HARVEST"],["COLLECT_FERTILIZER"],["EAST"],["WEST"]],"market":[["SELL","STRAWBERRY",2],["SELL","MILK",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["HARVEST"],["FEED"],["COLLECT_FERTILIZER"],["CARE"],["WATER"],["WATER"],["DIG"],["PLANT","WHEAT"],["SOUTH"],["EAST"],["COLLECT_FERTILIZER"]],"market":[["SELL","WHEAT",5]]},{"farmer":["NORTH"],"hands":[["DIG"],["CARE"],["EAST"],["COLLECT_FERTILIZER"],["NORTH"],["SOUTH"],["PLANT","WHEAT"],["WATER"],["DIG"],["WATER"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["PLANT","WHEAT"],["COLLECT_FERTILIZER"],["FEED"],["NORTH"],["HARVEST"],["WEST"],["WATER"],["EAST"],["PLANT","WHEAT"],["NORTH"],["WATER"]],"market":[]},{"farmer":["WEST"],"hands":[["WATER"],["SOUTH"],["CARE"],["FEED"],["DIG"],["WATER"],["EAST"],["EAST"],["WATER"],["HARVEST"],["WEST"]],"market":[["SELL","STRAWBERRY",2],["SELL","MILK",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["NORTH"],["FEED"],["COLLECT_FERTILIZER"],["CARE"],["PLANT","WHEAT"],["FERTILIZE"],["HARVEST"],["EAST"],["WEST"],["DIG"],["FERTILIZE"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["HARVEST"],["CARE"],["EAST"],["COLLECT_FERTILIZER"],["WATER"],["WEST"],["DIG"],["COLLECT_FERTILIZER"],["WATER"],["PLANT","WHEAT"],["WATER"]],"market":[["BUY_SEED","WHEAT",3]]},{"farmer":["WATER"],"hands":[["DIG"],["COLLECT_FERTILIZER"],["FEED"],["HARVEST"],["EAST"],["FERTILIZE"],["PLANT","WHEAT"],["HARVEST"],["HARVEST"],["WATER"],["WEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","CARROT",4]]},{"farmer":["WEST"],"hands":[["PLANT","CARROT"],["SOUTH"],["CARE"],["WEST"],["HARVEST"],["WATER"],["WATER"],["FEED"],["PLANT","WHEAT"],["NORTH"],["WATER"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["WATER"],["FERTILIZE"],["COLLECT_FERTILIZER"],["WATER"],["DIG"],["WEST"],["NORTH"],["CARE"],["WATER"],["FERTILIZE"],["HARVEST"]],"market":[["SELL","WHEAT",14],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["NORTH"],["WATER"],["HARVEST"],["HARVEST"],["PLANT","WHEAT"],["WATER"],["HARVEST"],["EAST"],["SOUTH"],["WATER"],["PLANT","WHEAT"]],"market":[]},{"farmer":["WEST"],"hands":[["HARVEST"],["WEST"],["WEST"],["PLANT","WHEAT"],["WATER"],["SOUTH"],["DIG"],["FEED"],["FERTILIZE"],["NORTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["DIG"],["FERTILIZE"],["WEST"],["WATER"],["NORTH"],["WEST"],["PLANT","CARROT"],["CARE"],["WATER"],["HARVEST"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["PLANT","CARROT"],["WATER"],["WEST"],["SOUTH"],["HARVEST"],["WATER"],["WATER"],["COLLECT_FERTILIZER"],["WEST"],["DIG"],["WATER"]],"market":[["SELL","EGG",16],["BUY_SEED","WHEAT",1],["BUY_SEED","CARROT",2]]},{"farmer":["WATER"],"hands":[["WATER"],["WEST"],["DROP"],["SOUTH"],["DIG"],["NORTH"],["NORTH"],["NORTH"],["WATER"],["PLANT","CARROT"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","CARROT",1]]},{"farmer":["HARVEST"],"hands":[["EAST"],["FERTILIZE"],["NORTH"],["FERTILIZE"],["PLANT","CARROT"],["WATER"],["HARVEST"],["DIG"],["SOUTH"],["WATER"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PLANT","WHEAT"],"hands":[["HARVEST"],["WATER"],["NORTH"],["WATER"],["WATER"],["HARVEST"],["DIG"],["PLANT","WHEAT"],["FERTILIZE"],["NORTH"],["WATER"]],"market":[["SELL","STRAWBERRY",3],["SELL","WOOL",3],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["DIG"],["NORTH"],["NORTH"],["NORTH"],["WEST"],["SOUTH"],["PLANT","CARROT"],["WATER"],["WATER"],["HARVEST"],["NORTH"]],"market":[["SELL","MILK",4],["SELL","EGG",4],["SELL","FERTILIZER",3]]},{"farmer":["PASS"],"hands":[["PASS"],["EAST"],["NORTH"],["FERTILIZE"],["HARVEST"],["EAST"],["WATER"],["PASS"],["PASS"],["DIG"],["NORTH"]],"market":[]},{"farmer":["PICKUP","WHEAT",3],"hands":[],"market":[["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["HARVEST"],["HARVEST"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["EAST"],["WEST"],["NORTH"],["NORTH"]],"market":[["HIRE"],["HIRE"]]},{"farmer":["CARE"],"hands":[["DROP"],["DROP"],["NORTH"],["WEST"],["EAST"],["HARVEST"],["NORTH"],["NORTH"],["SOUTH"],["PICKUP","FERTILIZER",3]],"market":[["SELL","WHEAT",4],["SELL","FERTILIZER",3],["HIRE"]]},{"farmer":["NORTH"],"hands":[["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["FEED"],["FEED"],["HARVEST"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"],["WATER"],["SOUTH"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["WEST"],"hands":[["EAST"],["FEED"],["CARE"],["CARE"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["WATER"],["HARVEST"],["SOUTH"],["NORTH"]],"market":[]},{"farmer":["FEED"],"hands":[["FEED"],["CARE"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["EAST"],["WEST"],["NORTH"],["HARVEST"],["PLANT","WHEAT"],["SOUTH"],["COLLECT_FERTILIZER"]],"market":[["SELL","MILK",1]]},{"farmer":["CARE"],"hands":[["CARE"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"],["EAST"],["WEST"],["DIG"],["PLANT","WHEAT"],["WATER"],["WEST"],["NORTH"]],"market":[["SELL","WHEAT",6],["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["FEED"],["FEED"],["WATER"],["WATER"],["PLANT","CARROT"],["WATER"],["NORTH"],["WATER"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["WEST"],"hands":[["HARVEST"],["FEED"],["CARE"],["CARE"],["HARVEST"],["HARVEST"],["WATER"],["WEST"],["DROP"],["SOUTH"],["HARVEST"]],"market":[]},{"farmer":["WEST"],"hands":[["EAST"],["CARE"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["PLANT","WHEAT"],["PLANT","WHEAT"],["WEST"],["WATER"],["SOUTH"],["WATER"],["NORTH"]],"market":[["SELL","MILK",2]]},{"farmer":["FEED"],"hands":[["FEED"],["SOUTH"],["EAST"],["WEST"],["WATER"],["WATER"],["WATER"],["HARVEST"],["SOUTH"],["WEST"],["WEST"]],"market":[["SELL","WHEAT",11],["BUY_SEED","WHEAT",3]]},{"farmer":["CARE"],"hands":[["CARE"],["FEED"],["FEED"],["HARVEST"],["NORTH"],["SOUTH"],["WEST"],["PLANT","WHEAT"],["WATER"],["FERTILIZE"],["FERTILIZE"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["EAST"],["CARE"],["CARE"],["FEED"],["NORTH"],["WATER"],["WEST"],["WATER"],["WEST"],["WATER"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["FEED"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["CARE"],["WATER"],["HARVEST"],["WEST"],["EAST"],["WATER"],["WEST"],["NORTH"]],"market":[["SELL","MILK",1],["BUY_SEED","CARROT",2]]},{"farmer":["NORTH"],"hands":[["CARE"],["HARVEST"],["HARVEST"],["COLLECT_FERTILIZER"],["HARVEST"],["PLANT","WHEAT"],["WATER"],["EAST"],["SOUTH"],["FERTILIZE"],["FERTILIZE"]],"market":[["SELL","EGG",11],["BUY_SEED","CARROT",2]]},{"farmer":["WATER"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["WEST"],["SOUTH"],["WATER"],["SOUTH"],["FEED"],["WATER"],["WATER"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["HARVEST"],["WATER"],["WEST"],["WATER"],["SOUTH"],["NORTH"],["HARVEST"],["CARE"],["WEST"],["HARVEST"],["WEST"]],"market":[]},{"farmer":["PLANT","CARROT"],"hands":[["NORTH"],["WEST"],["FERTILIZE"],["SOUTH"],["WEST"],["EAST"],["WEST"],["SOUTH"],["WATER"],["PLANT","CARROT"],["FERTILIZE"]],"market":[["SELL","MILK",1]]},{"farmer":["WATER"],"hands":[["FERTILIZE"],["WATER"],["WATER"],["SOUTH"],["WEST"],["EAST"],["WATER"],["SOUTH"],["WEST"],["WATER"],["WATER"]],"market":[]},{"farmer":["EAST"],"hands":[["WATER"],["SOUTH"],["SOUTH"],["SOUTH"],["WEST"],["EAST"],["HARVEST"],["DROP"],["WATER"],["WEST"],["SOUTH"]],"market":[]},{"farmer":["WATER"],"hands":[["NORTH"],["WATER"],["SOUTH"],["WATER"],["WEST"],["EAST"],["PLANT","WHEAT"],["HARVEST"],["WEST"],["FERTILIZE"],["WATER"]],"market":[["SELL","WHEAT",9]]},{"farmer":["NORTH"],"hands":[["EAST"],["HARVEST"],["DROP"],["SOUTH"],["DROP"],["DROP"],["WATER"],["DROP"],["WATER"],["WATER"],["HARVEST"]],"market":[["SELL","MILK",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["PLANT","CARROT"],["EAST"],["PASS"],["FERTILIZE"],["PASS"],["PASS"],["NORTH"],["PASS"],["SOUTH"],["WEST"],["PLANT","WHEAT"]],"market":[["SELL","WHEAT",17],["SELL","EGG",12],["SELL","CARROT",4],["SELL","MILK",3],["SELL","FERTILIZER",4]]},{"farmer":["FERTILIZE"],"hands":[["WATER"],["WATER"],["PASS"],["EAST"],["PASS"],["PASS"],["WATER"],["PASS"],["WATER"],["WATER"],["WATER"]],"market":[]},{"farmer":["PICKUP","WHEAT",3],"hands":[],"market":[["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["BUY_PRODUCT","WHEAT",9]]},{"farmer":["FEED"],"hands":[["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["COLLECT_FERTILIZER"],["NORTH"],["WEST"],["NORTH"],["NORTH"]],"market":[["HIRE"],["HIRE"],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["CARE"],"hands":[["FEED"],["FEED"],["NORTH"],["NORTH"],["HARVEST"],["COLLECT_FERTILIZER"],["EAST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["PICKUP","FERTILIZER",4]],"market":[["SELL","FERTILIZER",6],["HIRE"],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["WEST"],"hands":[["CARE"],["CARE"],["EAST"],["WEST"],["COLLECT_FERTILIZER"],["WEST"],["EAST"],["NORTH"],["SOUTH"],["WEST"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["FEED"],["COLLECT_FERTILIZER"],["NORTH"],["FERTILIZE"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["SOUTH"],["WEST"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["FEED"],["CARE"],["HARVEST"],["WATER"],["WATER"],["NORTH"],["NORTH"],["WATER"],["WEST"],["WEST"]],"market":[]},{"farmer":["FEED"],"hands":[["FEED"],["CARE"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["SOUTH"],["FERTILIZE"],["WATER"],["WEST"],["WEST"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["CARE"],"hands":[["CARE"],["SOUTH"],["EAST"],["FERTILIZE"],["FERTILIZE"],["WEST"],["WATER"],["WEST"],["WATER"],["FERTILIZE"],["WEST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["EAST"],["FEED"],["FEED"],["WATER"],["WATER"],["WATER"],["EAST"],["WATER"],["HARVEST"],["WATER"],["WEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["FEED"],["CARE"],["CARE"],["NORTH"],["EAST"],["SOUTH"],["WATER"],["HARVEST"],["SOUTH"],["SOUTH"],["WATER"]],"market":[["SELL","STRAWBERRY",3],["SELL","MILK",1]]},{"farmer":["FEED"],"hands":[["CARE"],["COLLECT_FERTILIZER"],["EAST"],["NORTH"],["WATER"],["WATER"],["NORTH"],["PLANT","WHEAT"],["WATER"],["SOUTH"],["HARVEST"]],"market":[["SELL","WHEAT",4]]},{"farmer":["CARE"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"],["WEST"],["WATER"],["WATER"],["SOUTH"],["WEST"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["HARVEST"],["WATER"],["HARVEST"],["WATER"],["WATER"],["WATER"],["HARVEST"],["SOUTH"],["WATER"],["SOUTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",3]]},{"farmer":["HARVEST"],"hands":[["NORTH"],["HARVEST"],["NORTH"],["HARVEST"],["HARVEST"],["HARVEST"],["PLANT","CARROT"],["SOUTH"],["HARVEST"],["WATER"],["NORTH"]],"market":[["SELL","STRAWBERRY",4],["SELL","MILK",1],["BUY_SEED","CARROT",2]]},{"farmer":["NORTH"],"hands":[["FERTILIZE"],["SOUTH"],["EAST"],["PLANT","CARROT"],["PLANT","CARROT"],["NORTH"],["WATER"],["FEED"],["PASS"],["HARVEST"],["FERTILIZE"]],"market":[["SELL","EGG",10]]},{"farmer":["FERTILIZE"],"hands":[["WATER"],["WATER"],["FERTILIZE"],["WATER"],["WATER"],["NORTH"],["NORTH"],["CARE"],["PLANT","WHEAT"],["EAST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["EAST"],["HARVEST"],["WATER"],["EAST"],["EAST"],["EAST"],["WATER"],["NORTH"],["WATER"],["FERTILIZE"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["FERTILIZE"],["SOUTH"],["NORTH"],["WATER"],["WATER"],["EAST"],["HARVEST"],["EAST"],["NORTH"],["WATER"],["EAST"]],"market":[["SELL","STRAWBERRY",4],["SELL","MILK",2],["BUY_SEED","CARROT",2]]},{"farmer":["FERTILIZE"],"hands":[["WATER"],["WATER"],["NORTH"],["HARVEST"],["HARVEST"],["EAST"],["PLANT","CARROT"],["FEED"],["NORTH"],["SOUTH"],["EAST"]],"market":[["SELL","CARROT",7]]},{"farmer":["WATER"],"hands":[["NORTH"],["SOUTH"],["FERTILIZE"],["PLANT","WHEAT"],["PLANT","WHEAT"],["EAST"],["WATER"],["CARE"],["NORTH"],["WATER"],["EAST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["WATER"],["WEST"],["WATER"],["WATER"],["WATER"],["DROP"],["NORTH"],["SOUTH"],["NORTH"],["WEST"],["EAST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["HARVEST"],["WEST"],["HARVEST"],["WEST"],["WEST"],["SOUTH"],["PLANT","WHEAT"],["SOUTH"],["EAST"],["FERTILIZE"],["DROP"]],"market":[["SELL","WHEAT",5],["SELL","MILK",2]]},{"farmer":["EAST"],"hands":[["PLANT","WHEAT"],["WATER"],["PLANT","CARROT"],["WEST"],["WEST"],["SOUTH"],["WATER"],["DROP"],["DROP"],["WATER"],["PASS"]],"market":[["SELL","WHEAT",5],["SELL","FERTILIZER",1]]},{"farmer":["WATER"],"hands":[["WATER"],["PASS"],["WATER"],["WEST"],["WATER"],["SOUTH"],["PASS"],["PASS"],["PASS"],["PASS"],["PASS"]],"market":[["SELL","STRAWBERRY",5],["SELL","WHEAT",8],["SELL","FERTILIZER",3],["SELL","MILK",1]]},{"farmer":["PICKUP","WHEAT",4],"hands":[],"market":[["SELL","CARROT",12],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["BUY_PRODUCT","WHEAT",9]]},{"farmer":["FEED"],"hands":[["PICKUP","WHEAT",3],["HARVEST"],["PICKUP","WHEAT",3],["COLLECT_FERTILIZER"],["NORTH"],["WEST"],["NORTH"],["NORTH"]],"market":[["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["CARE"],"hands":[["FEED"],["DROP"],["NORTH"],["NORTH"],["NORTH"],["HARVEST"],["EAST"],["WEST"],["SOUTH"],["PICKUP","FERTILIZER",3],["WEST"]],"market":[["SELL","FERTILIZER",3],["HIRE"],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["WEST"],"hands":[["CARE"],["PICKUP","WHEAT",3],["EAST"],["DIG"],["WATER"],["COLLECT_FERTILIZER"],["EAST"],["WEST"],["SOUTH"],["SOUTH"],["COLLECT_FERTILIZER"],["NORTH"]],"market":[]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["FEED"],["FEED"],["PLANT","WHEAT"],["HARVEST"],["WEST"],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["WEST"],["WEST"],["NORTH"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["CARE"],["CARE"],["WATER"],["PLANT","WHEAT"],["WATER"],["HARVEST"],["HARVEST"],["HARVEST"],["FERTILIZE"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"]],"market":[["SELL","STRAWBERRY",3],["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["FEED"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"],["WEST"],["NORTH"],["PLANT","WHEAT"],["WEST"],["WATER"],["WEST"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["CARE"],["WEST"],["HARVEST"],["NORTH"],["EAST"],["WATER"],["WATER"],["WATER"],["HARVEST"],["SOUTH"],["HARVEST"],["FERTILIZE"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["FEED"],["EAST"],["NORTH"],["WATER"],["SOUTH"],["HARVEST"],["EAST"],["DIG"],["FERTILIZE"],["SOUTH"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["EAST"],["CARE"],["FEED"],["FERTILIZE"],["HARVEST"],["HARVEST"],["PLANT","WHEAT"],["FEED"],["PLANT","WHEAT"],["SOUTH"],["WEST"],["EAST"]],"market":[["SELL","STRAWBERRY",4],["SELL","MILK",1]]},{"farmer":["FEED"],"hands":[["FEED"],["SOUTH"],["CARE"],["WATER"],["PLANT","WHEAT"],["DIG"],["WATER"],["CARE"],["WATER"],["FERTILIZE"],["FERTILIZE"],["WATER"]],"market":[["SELL","WHEAT",3],["SELL","CARROT",2],["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["CARE"],["FEED"],["EAST"],["WEST"],["WATER"],["PLANT","WHEAT"],["EAST"],["COLLECT_FERTILIZER"],["SOUTH"],["WATER"],["WATER"],["NORTH"]],"market":[["BUY_SEED","WHEAT",3]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["CARE"],["FEED"],["WEST"],["EAST"],["WATER"],["WATER"],["NORTH"],["HARVEST"],["HARVEST"],["SOUTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["CARE"],["WEST"],["WATER"],["SOUTH"],["HARVEST"],["FERTILIZE"],["DIG"],["SOUTH"],["FERTILIZE"],["HARVEST"]],"market":[["SELL","STRAWBERRY",3],["SELL","MILK",1],["BUY_SEED","CARROT",2]]},{"farmer":["WATER"],"hands":[["NORTH"],["HARVEST"],["COLLECT_FERTILIZER"],["WATER"],["HARVEST"],["HARVEST"],["PLANT","WHEAT"],["WATER"],["PLANT","CARROT"],["WATER"],["WATER"],["PLANT","WHEAT"]],"market":[["SELL","EGG",16],["SELL","CARROT",3]]},{"farmer":["NORTH"],"hands":[["FERTILIZE"],["WEST"],["EAST"],["HARVEST"],["PLANT","WHEAT"],["DIG"],["WATER"],["EAST"],["WATER"],["HARVEST"],["SOUTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","CARROT",2]]},{"farmer":["WATER"],"hands":[["WATER"],["FERTILIZE"],["FERTILIZE"],["WEST"],["WATER"],["PLANT","CARROT"],["SOUTH"],["FEED"],["WEST"],["WEST"],["PLANT","CARROT"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["EAST"],"hands":[["NORTH"],["WATER"],["WATER"],["WATER"],["SOUTH"],["WATER"],["WEST"],["CARE"],["WEST"],["WEST"],["WATER"],["WEST"]],"market":[["SELL","STRAWBERRY",4],["SELL","MILK",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["EAST"],["NORTH"],["NORTH"],["HARVEST"],["SOUTH"],["SOUTH"],["WEST"],["SOUTH"],["HARVEST"],["WATER"],["SOUTH"],["WEST"]],"market":[]},{"farmer":["EAST"],"hands":[["FERTILIZE"],["EAST"],["WATER"],["PLANT","WHEAT"],["WEST"],["EAST"],["WEST"],["SOUTH"],["DIG"],["WEST"],["WATER"],["WEST"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["WATER"],["EAST"],["NORTH"],["WATER"],["WEST"],["FERTILIZE"],["DROP"],["DROP"],["PLANT","CARROT"],["WATER"],["SOUTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["EAST"],["DROP"],["FERTILIZE"],["SOUTH"],["DROP"],["WATER"],["HARVEST"],["NORTH"],["WATER"],["HARVEST"],["WATER"],["WEST"]],"market":[["SELL","WHEAT",13],["SELL","STRAWBERRY",3],["SELL","MILK",1]]},{"farmer":["NORTH"],"hands":[["FERTILIZE"],["PASS"],["WATER"],["WATER"],["PASS"],["NORTH"],["DROP"],["NORTH"],["NORTH"],["NORTH"],["NORTH"],["WATER"]],"market":[["SELL","WHEAT",15],["SELL","EGG",8],["SELL","FERTILIZER",2]]},{"farmer":["FERTILIZE"],"hands":[["WATER"],["PASS"],["HARVEST"],["PASS"],["PASS"],["HARVEST"],["PASS"],["NORTH"],["EAST"],["NORTH"],["NORTH"],["PASS"]],"market":[]},{"farmer":["PICKUP","WHEAT",3],"hands":[],"market":[["SELL","CARROT",5],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["BUY_PRODUCT","WHEAT",9]]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["COLLECT_FERTILIZER"],["NORTH"],["SOUTH"],["NORTH"],["NORTH"]],"market":[["SELL","STRAWBERRY",4],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["FEED"],["FEED"],["NORTH"],["NORTH"],["HARVEST"],["WATER"],["EAST"],["NORTH"],["WEST"],["WEST"],["WEST"]],"market":[["SELL","TOMATO",4],["HIRE"],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["WEST"],"hands":[["CARE"],["CARE"],["EAST"],["NORTH"],["COLLECT_FERTILIZER"],["HARVEST"],["EAST"],["WEST"],["DIG"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"]],"market":[["BUY_SEED","CARROT",2]]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FEED"],["COLLECT_FERTILIZER"],["NORTH"],["PLANT","WHEAT"],["COLLECT_FERTILIZER"],["WATER"],["PLANT","WHEAT"],["WEST"],["WEST"],["WEST"]],"market":[]},{"farmer":["CARE"],"hands":[["NORTH"],["WEST"],["CARE"],["NORTH"],["NORTH"],["WATER"],["EAST"],["HARVEST"],["WATER"],["WATER"],["WEST"],["COLLECT_FERTILIZER"]],"market":[["SELL","STRAWBERRY",4],["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FEED"],["FEED"],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["SOUTH"],["EAST"],["PLANT","WHEAT"],["WEST"],["HARVEST"],["WATER"],["NORTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["CARE"],["CARE"],["EAST"],["NORTH"],["HARVEST"],["WATER"],["WATER"],["WATER"],["DIG"],["PLANT","CARROT"],["HARVEST"],["NORTH"]],"market":[["BUY_SEED","CARROT",4]]},{"farmer":["FEED"],"hands":[["EAST"],["SOUTH"],["FEED"],["WATER"],["PLANT","WHEAT"],["SOUTH"],["HARVEST"],["WEST"],["PLANT","CARROT"],["WATER"],["PLANT","CARROT"],["FERTILIZE"]],"market":[]},{"farmer":["CARE"],"hands":[["FEED"],["FEED"],["CARE"],["WEST"],["WATER"],["WATER"],["PLANT","CARROT"],["WATER"],["WATER"],["WEST"],["WATER"],["WATER"]],"market":[["SELL","STRAWBERRY",4],["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["CARE"],["CARE"],["EAST"],["FERTILIZE"],["EAST"],["SOUTH"],["WATER"],["HARVEST"],["WEST"],["WEST"],["WEST"],["WEST"]],"market":[["SELL","WHEAT",2]]},{"farmer":["HARVEST"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FEED"],["WATER"],["WATER"],["WATER"],["NORTH"],["PLANT","CARROT"],["WEST"],["WATER"],["WATER"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["HARVEST"],["WEST"],["CARE"],["WEST"],["HARVEST"],["WEST"],["WATER"],["WATER"],["WATER"],["HARVEST"],["HARVEST"],["HARVEST"]],"market":[["BUY_SEED","CARROT",3]]},{"farmer":["WATER"],"hands":[["NORTH"],["WATER"],["COLLECT_FERTILIZER"],["WEST"],["PLANT","CARROT"],["WATER"],["HARVEST"],["EAST"],["NORTH"],["PLANT","CARROT"],["PLANT","CARROT"],["PLANT","CARROT"]],"market":[["SELL","STRAWBERRY",3],["SELL","MILK",2]]},{"farmer":["HARVEST"],"hands":[["NORTH"],["SOUTH"],["NORTH"],["FERTILIZE"],["WATER"],["WEST"],["PLANT","CARROT"],["EAST"],["WATER"],["WATER"],["WATER"],["WATER"]],"market":[["BUY_SEED","CARROT",2]]},{"farmer":["PLANT","CARROT"],"hands":[["EAST"],["SOUTH"],["NORTH"],["WATER"],["SOUTH"],["WATER"],["WATER"],["FEED"],["HARVEST"],["EAST"],["SOUTH"],["WEST"]],"market":[["BUY_SEED","CARROT",2]]},{"farmer":["WATER"],"hands":[["FERTILIZE"],["WATER"],["FERTILIZE"],["HARVEST"],["SOUTH"],["HARVEST"],["SOUTH"],["CARE"],["PLANT","CARROT"],["EAST"],["WATER"],["WATER"]],"market":[]},{"farmer":["SOUTH"],"hands":[["WATER"],["HARVEST"],["WATER"],["EAST"],["SOUTH"],["PLANT","CARROT"],["WEST"],["HARVEST"],["WATER"],["EAST"],["HARVEST"],["HARVEST"]],"market":[["SELL","STRAWBERRY",4],["SELL","MILK",3],["BUY_SEED","CARROT",2]]},{"farmer":["SOUTH"],"hands":[["NORTH"],["WEST"],["NORTH"],["WATER"],["WEST"],["WATER"],["WEST"],["SOUTH"],["NORTH"],["EAST"],["PLANT","CARROT"],["PLANT","CARROT"]],"market":[["SELL","EGG",8]]},{"farmer":["EAST"],"hands":[["WATER"],["WEST"],["WATER"],["EAST"],["DROP"],["WEST"],["WEST"],["SOUTH"],["WATER"],["DROP"],["WATER"],["WATER"]],"market":[]},{"farmer":["EAST"],"hands":[["WEST"],["FERTILIZE"],["EAST"],["EAST"],["PICKUP","WHEAT",1],["WEST"],["WEST"],["DROP"],["HARVEST"],["PICKUP","FERTILIZER",1],["SOUTH"],["WEST"]],"market":[["SELL","WHEAT",23],["BUY_SEED","CARROT",1]]},{"farmer":["EAST"],"hands":[["FERTILIZE"],["WATER"],["WATER"],["EAST"],["WEST"],["WATER"],["DROP"],["PICKUP","WHEAT",1],["PLANT","CARROT"],["SOUTH"],["SOUTH"],["WATER"]],"market":[["SELL","MILK",5],["SELL","WHEAT",8]]},{"farmer":["DROP"],"hands":[["WATER"],["SOUTH"],["NORTH"],["WATER"],["FEED"],["EAST"],["PASS"],["FEED"],["WATER"],["SOUTH"],["SOUTH"],["NORTH"]],"market":[["SELL","WHEAT",10],["SELL","EGG",4],["SELL","FERTILIZER",2]]},{"farmer":["PASS"],"hands":[["PASS"],["EAST"],["WEST"],["PASS"],["CARE"],["WATER"],["PASS"],["CARE"],["PASS"],["SOUTH"],["EAST"],["WATER"]],"market":[["SELL","STRAWBERRY",3],["SELL","WHEAT",7],["SELL","EGG",4],["SELL","FERTILIZER",2]]},{"farmer":["PICKUP","WHEAT",3],"hands":[],"market":[["SELL","WHEAT",21],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["PICKUP","WHEAT",3],["HARVEST"],["PICKUP","WHEAT",3],["COLLECT_FERTILIZER"],["NORTH"],["WEST"],["NORTH"],["NORTH"]],"market":[["HIRE"],["HIRE"]]},{"farmer":["CARE"],"hands":[["FEED"],["DROP"],["NORTH"],["NORTH"],["NORTH"],["HARVEST"],["EAST"],["WATER"],["COLLECT_FERTILIZER"],["PICKUP","FERTILIZER",3]],"market":[["SELL","TOMATO",2],["SELL","FERTILIZER",3],["HIRE"],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["NORTH"],"hands":[["CARE"],["PICKUP","WHEAT",3],["EAST"],["NORTH"],["WATER"],["COLLECT_FERTILIZER"],["EAST"],["NORTH"],["SOUTH"],["SOUTH"],["HARVEST"]],"market":[]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["FEED"],["FEED"],["NORTH"],["NORTH"],["SOUTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["SOUTH"],["SOUTH"],["PLACE","MILK",5]],"market":[]},{"farmer":["FEED"],"hands":[["NORTH"],["CARE"],["CARE"],["WATER"],["NORTH"],["WEST"],["HARVEST"],["NORTH"],["WATER"],["WEST"],["WEST"]],"market":[["SELL","MILK",1]]},{"farmer":["CARE"],"hands":[["FEED"],["WEST"],["COLLECT_FERTILIZER"],["HARVEST"],["WATER"],["WEST"],["NORTH"],["WEST"],["SOUTH"],["SOUTH"],["WEST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["CARE"],["FEED"],["HARVEST"],["NORTH"],["EAST"],["FERTILIZE"],["FERTILIZE"],["WATER"],["WATER"],["SOUTH"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["CARE"],["EAST"],["WATER"],["WATER"],["WATER"],["WATER"],["HARVEST"],["WEST"],["FERTILIZE"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["EAST"],["SOUTH"],["FEED"],["HARVEST"],["HARVEST"],["EAST"],["NORTH"],["PLANT","WHEAT"],["WATER"],["WATER"],["HARVEST"]],"market":[["SELL","STRAWBERRY",3],["SELL","MILK",1],["BUY_SEED","CARROT",4]]},{"farmer":["WATER"],"hands":[["FEED"],["FEED"],["CARE"],["WEST"],["PLANT","CARROT"],["WATER"],["EAST"],["WATER"],["WEST"],["WEST"],["WEST"]],"market":[["SELL","WHEAT",2]]},{"farmer":["WEST"],"hands":[["CARE"],["CARE"],["EAST"],["WATER"],["WATER"],["HARVEST"],["WATER"],["NORTH"],["WATER"],["FERTILIZE"],["FERTILIZE"]],"market":[]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FEED"],["HARVEST"],["EAST"],["SOUTH"],["HARVEST"],["WEST"],["WEST"],["WATER"],["WATER"]],"market":[]},{"farmer":["CARE"],"hands":[["NORTH"],["HARVEST"],["CARE"],["SOUTH"],["WATER"],["DIG"],["PLANT","CARROT"],["FERTILIZE"],["WATER"],["WEST"],["HARVEST"]],"market":[["SELL","STRAWBERRY",3],["SELL","MILK",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FERTILIZE"],["SOUTH"],["COLLECT_FERTILIZER"],["SOUTH"],["HARVEST"],["PLANT","CARROT"],["WATER"],["WATER"],["NORTH"],["WEST"],["PLANT","CARROT"]],"market":[]},{"farmer":["NORTH"],"hands":[["WATER"],["FERTILIZE"],["HARVEST"],["EAST"],["SOUTH"],["WATER"],["NORTH"],["HARVEST"],["FERTILIZE"],["WATER"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["EAST"],["WATER"],["NORTH"],["FEED"],["SOUTH"],["NORTH"],["WATER"],["PLANT","CARROT"],["WATER"],["HARVEST"],["EAST"]],"market":[]},{"farmer":["WEST"],"hands":[["FERTILIZE"],["WEST"],["FERTILIZE"],["SOUTH"],["SOUTH"],["NORTH"],["HARVEST"],["WATER"],["WEST"],["FERTILIZE"],["EAST"]],"market":[["SELL","STRAWBERRY",3],["SELL","MILK",2]]},{"farmer":["WATER"],"hands":[["WATER"],["WEST"],["WATER"],["SOUTH"],["SOUTH"],["EAST"],["NORTH"],["WEST"],["WATER"],["WEST"],["EAST"]],"market":[["SELL","EGG",8],["SELL","CARROT",4]]},{"farmer":["HARVEST"],"hands":[["NORTH"],["SOUTH"],["NORTH"],["DROP"],["WEST"],["EAST"],["WATER"],["WATER"],["HARVEST"],["WATER"],["EAST"]],"market":[]},{"farmer":["NORTH"],"hands":[["WATER"],["WEST"],["NORTH"],["PICKUP","FERTILIZER",1],["WEST"],["DROP"],["SOUTH"],["HARVEST"],["SOUTH"],["HARVEST"],["DROP"]],"market":[["SELL","TOMATO",8],["SELL","WHEAT",4]]},{"farmer":["FERTILIZE"],"hands":[["HARVEST"],["WATER"],["EAST"],["WEST"],["DROP"],["WEST"],["EAST"],["SOUTH"],["WATER"],["EAST"],["WEST"]],"market":[["SELL","STRAWBERRY",4],["SELL","MILK",3],["SELL","WHEAT",4]]},{"farmer":["WATER"],"hands":[["PLANT","WHEAT"],["NORTH"],["WATER"],["FERTILIZE"],["PASS"],["WEST"],["WATER"],["WATER"],["NORTH"],["EAST"],["WEST"]],"market":[["SELL","EGG",4],["SELL","CARROT",4],["SELL","WHEAT",5]]},{"farmer":["PASS"],"hands":[["WATER"],["NORTH"],["HARVEST"],["WATER"],["PASS"],["WATER"],["HARVEST"],["PASS"],["NORTH"],["WATER"],["WATER"]],"market":[["SELL","STRAWBERRY",3]]},{"farmer":["HARVEST"],"hands":[],"market":[["SELL","CARROT",16],["SELL","WHEAT",9],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["DROP"],"hands":[["HARVEST"],["PICKUP","WHEAT",3],["PICKUP","FERTILIZER",2],["COLLECT_FERTILIZER"],["NORTH"],["SOUTH"],["NORTH"],["NORTH"]],"market":[["SELL","STRAWBERRY",3],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["DROP"],["FEED"],["NORTH"],["NORTH"],["HARVEST"],["WEST"],["NORTH"],["WEST"],["SOUTH"],["WEST"]],"market":[["SELL","TOMATO",9]]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["CARE"],["NORTH"],["NORTH"],["COLLECT_FERTILIZER"],["WEST"],["EAST"],["WEST"],["WATER"],["WEST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["EAST"],["COLLECT_FERTILIZER"],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"],["HARVEST"],["EAST"],["WATER"],["SOUTH"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["HARVEST"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["FERTILIZE"],["HARVEST"],["WATER"],["WEST"],["WATER"],["HARVEST"],["HARVEST"],["WEST"]],"market":[["SELL","STRAWBERRY",4],["SELL","MILK",2]]},{"farmer":["NORTH"],"hands":[["EAST"],["FEED"],["NORTH"],["NORTH"],["EAST"],["WATER"],["HARVEST"],["WEST"],["SOUTH"],["FERTILIZE"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["COLLECT_FERTILIZER"],["CARE"],["FERTILIZE"],["FERTILIZE"],["WATER"],["HARVEST"],["EAST"],["COLLECT_FERTILIZER"],["HARVEST"],["WATER"]],"market":[]},{"farmer":["WATER"],"hands":[["EAST"],["SOUTH"],["WATER"],["WATER"],["HARVEST"],["SOUTH"],["WATER"],["HARVEST"],["SOUTH"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["FEED"],["NORTH"],["HARVEST"],["SOUTH"],["WATER"],["HARVEST"],["SOUTH"],["HARVEST"],["WATER"]],"market":[["SELL","STRAWBERRY",4],["SELL","MILK",2]]},{"farmer":["WATER"],"hands":[["EAST"],["CARE"],["WATER"],["NORTH"],["SOUTH"],["HARVEST"],["SOUTH"],["FEED"],["WEST"],["WEST"]],"market":[["SELL","WHEAT",2]]},{"farmer":["NORTH"],"hands":[["FERTILIZE"],["COLLECT_FERTILIZER"],["SOUTH"],["FERTILIZE"],["WEST"],["EAST"],["FEED"],["CARE"],["WATER"],["WATER"]],"market":[]},{"farmer":["WATER"],"hands":[["WATER"],["NORTH"],["EAST"],["WATER"],["DROP"],["EAST"],["WEST"],["COLLECT_FERTILIZER"],["HARVEST"],["SOUTH"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["NORTH"],["WATER"],["HARVEST"],["NORTH"],["WATER"],["FEED"],["NORTH"],["WEST"],["WATER"]],"market":[["SELL","STRAWBERRY",4],["SELL","MILK",1]]},{"farmer":["WATER"],"hands":[["FERTILIZE"],["WATER"],["NORTH"],["SOUTH"],["EAST"],["HARVEST"],["WEST"],["WEST"],["WATER"],["HARVEST"]],"market":[["SELL","WHEAT",5]]},{"farmer":["HARVEST"],"hands":[["WATER"],["WEST"],["EAST"],["SOUTH"],["COLLECT_FERTILIZER"],["NORTH"],["FEED"],["FERTILIZE"],["HARVEST"],["SOUTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["HARVEST"],["FERTILIZE"],["EAST"],["SOUTH"],["HARVEST"],["NORTH"],["WEST"],["WATER"],["WEST"],["SOUTH"]],"market":[]},{"farmer":["HARVEST"],"hands":[["NORTH"],["WATER"],["WATER"],["SOUTH"],["WEST"],["EAST"],["DROP"],["NORTH"],["HARVEST"],["HARVEST"]],"market":[["SELL","STRAWBERRY",5],["SELL","MILK",2]]},{"farmer":["WEST"],"hands":[["WEST"],["NORTH"],["HARVEST"],["DROP"],["WEST"],["DROP"],["NORTH"],["FERTILIZE"],["NORTH"],["EAST"]],"market":[["SELL","EGG",20],["SELL","WHEAT",7],["SELL","FERTILIZER",1]]},{"farmer":["WATER"],"hands":[["WEST"],["NORTH"],["SOUTH"],["PICKUP","WHEAT",1],["FERTILIZE"],["SOUTH"],["NORTH"],["WATER"],["WEST"],["WATER"]],"market":[["SELL","WHEAT",10],["SELL","CARROT",4]]},{"farmer":["HARVEST"],"hands":[["WATER"],["WEST"],["SOUTH"],["NORTH"],["WATER"],["SOUTH"],["EAST"],["HARVEST"],["SOUTH"],["HARVEST"]],"market":[]},{"farmer":["EAST"],"hands":[["HARVEST"],["FERTILIZE"],["WATER"],["EAST"],["SOUTH"],["SOUTH"],["NORTH"],["SOUTH"],["WATER"],["EAST"]],"market":[["SELL","STRAWBERRY",6],["SELL","MILK",3]]},{"farmer":["WATER"],"hands":[["NORTH"],["WATER"],["NORTH"],["FEED"],["DROP"],["WEST"],["NORTH"],["SOUTH"],["HARVEST"],["HARVEST"]],"market":[]},{"farmer":["PASS"],"hands":[["FERTILIZE"],["HARVEST"],["WEST"],["CARE"],["PASS"],["HARVEST"],["WATER"],["WATER"],["PASS"],["EAST"]],"market":[["SELL","TOMATO",4],["SELL","EGG",4]]},{"farmer":["NORTH"],"hands":[],"market":[["SELL","CARROT",20],["SELL","WHEAT",14],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["WEST"],["EAST"],["SOUTH"],["NORTH"],["NORTH"],["NORTH"],["SOUTH"],["NORTH"]],"market":[["SELL","MILK",2],["SELL","FERTILIZER",1],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["WATER"],["EAST"],["WATER"],["EAST"],["WEST"],["NORTH"],["SOUTH"],["NORTH"],["NORTH"],["WEST"]],"market":[]},{"farmer":["HARVEST"],"hands":[["HARVEST"],["HARVEST"],["HARVEST"],["EAST"],["WEST"],["WATER"],["WEST"],["NORTH"],["WATER"],["WEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["WEST"],["COLLECT_FERTILIZER"],["NORTH"],["EAST"],["WEST"],["HARVEST"],["WEST"],["NORTH"],["HARVEST"],["WATER"]],"market":[]},{"farmer":["HARVEST"],"hands":[["WATER"],["NORTH"],["DROP"],["EAST"],["WEST"],["NORTH"],["WATER"],["EAST"],["NORTH"],["HARVEST"]],"market":[["SELL","STRAWBERRY",6],["SELL","MILK",1]]},{"farmer":["WEST"],"hands":[["HARVEST"],["NORTH"],["WEST"],["WATER"],["WATER"],["WATER"],["HARVEST"],["EAST"],["COLLECT_FERTILIZER"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["WEST"],["EAST"],["SOUTH"],["HARVEST"],["HARVEST"],["HARVEST"],["SOUTH"],["WATER"],["WEST"],["WATER"]],"market":[]},{"farmer":["WATER"],"hands":[["HARVEST"],["FERTILIZE"],["COLLECT_FERTILIZER"],["WEST"],["EAST"],["NORTH"],["SOUTH"],["HARVEST"],["WATER"],["HARVEST"]],"market":[]},{"farmer":["HARVEST"],"hands":[["COLLECT_FERTILIZER"],["WATER"],["HARVEST"],["HARVEST"],["HARVEST"],["WATER"],["WEST"],["WEST"],["HARVEST"],["WEST"]],"market":[["SELL","STRAWBERRY",4],["SELL","MILK",2]]},{"farmer":["SOUTH"],"hands":[["EAST"],["HARVEST"],["NORTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["HARVEST"],["WEST"],["WATER"],["WEST"],["WATER"]],"market":[["SELL","STRAWBERRY",4],["SELL","WHEAT",13]]},{"farmer":["WATER"],"hands":[["EAST"],["SOUTH"],["COLLECT_FERTILIZER"],["WEST"],["EAST"],["SOUTH"],["HARVEST"],["HARVEST"],["FERTILIZE"],["HARVEST"]],"market":[["SELL","STRAWBERRY",5]]},{"farmer":["HARVEST"],"hands":[["EAST"],["WEST"],["HARVEST"],["WEST"],["EAST"],["SOUTH"],["NORTH"],["NORTH"],["WATER"],["NORTH"]],"market":[["SELL","STRAWBERRY",3]]},{"farmer":["EAST"],"hands":[["DROP"],["WEST"],["EAST"],["WEST"],["COLLECT_FERTILIZER"],["SOUTH"],["NORTH"],["WATER"],["HARVEST"],["WATER"]],"market":[["SELL","STRAWBERRY",4],["SELL","MILK",1]]},{"farmer":["WATER"],"hands":[["EAST"],["COLLECT_FERTILIZER"],["DROP"],["DROP"],["SOUTH"],["SOUTH"],["NORTH"],["HARVEST"],["SOUTH"],["HARVEST"]],"market":[["SELL","EGG",4],["SELL","CARROT",4],["SELL","WHEAT",5],["SELL","FERTILIZER",1]]},{"farmer":["HARVEST"],"hands":[["EAST"],["HARVEST"],["HARVEST"],["NORTH"],["EAST"],["DROP"],["NORTH"],["SOUTH"],["SOUTH"],["EAST"]],"market":[["SELL","TOMATO",5],["SELL","CARROT",4],["SELL","FERTILIZER",3]]},{"farmer":["SOUTH"],"hands":[["COLLECT_FERTILIZER"],["SOUTH"],["DROP"],["COLLECT_FERTILIZER"],["DROP"],["EAST"],["EAST"],["SOUTH"],["EAST"],["EAST"]],"market":[["SELL","WHEAT",15]]},{"farmer":["SOUTH"],"hands":[["HARVEST"],["WEST"],["COLLECT_FERTILIZER"],["HARVEST"],["COLLECT_FERTILIZER"],["HARVEST"],["EAST"],["SOUTH"],["EAST"],["EAST"]],"market":[["SELL","STRAWBERRY",4],["SELL","CARROT",4],["SELL","FERTILIZER",2]]},{"farmer":["SOUTH"],"hands":[["WEST"],["DROP"],["DROP"],["SOUTH"],["DROP"],["WEST"],["EAST"],["SOUTH"],["DROP"],["EAST"]],"market":[["SELL","EGG",17]]},{"farmer":["EAST"],"hands":[["DROP"],["COLLECT_FERTILIZER"],["NORTH"],["DROP"],["EAST"],["COLLECT_FERTILIZER"],["EAST"],["WEST"],["EAST"],["DROP"]],"market":[["SELL","WHEAT",11],["SELL","EGG",5],["SELL","CARROT",7],["SELL","FERTILIZER",3]]},{"farmer":["DROP"],"hands":[["PASS"],["DROP"],["NORTH"],["PASS"],["PASS"],["NORTH"],["DROP"],["DROP"],["PASS"],["PASS"]],"market":[["SELL","CARROT",12],["SELL","EGG",6],["SELL","FERTILIZER",2]]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["NORTH"],["PASS"],["PASS"],["NORTH"],["PASS"],["PASS"],["PASS"],["PASS"]],"market":[["SELL","CARROT",12],["SELL","MILK",3],["SELL","WHEAT",5],["SELL","FERTILIZER",1]]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["NORTH"],["PASS"],["PASS"],["NORTH"],["PASS"],["PASS"],["PASS"],["PASS"]],"market":[["SELL","TOMATO",5],["SELL","STRAWBERRY",3]]}]')
_PROXY=make_agent({0:_DEMO})
def archived_proxy_agent(observation,configuration=None):
    return _PROXY(observation,configuration)
archived_proxy_agent.telemetry=_PROXY.chassis.diagnostics
agent=archived_proxy_agent
