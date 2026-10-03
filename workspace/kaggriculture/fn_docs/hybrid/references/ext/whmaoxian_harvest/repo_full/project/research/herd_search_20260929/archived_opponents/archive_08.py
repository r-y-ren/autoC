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
_DEMO=json.loads('[{"farmer":["PASS"],"hands":[],"market":[["BUY_ANIMAL","COW",1],["BUY_PRODUCT","WHEAT",5],["BUY_ANIMAL","SHEEP",1],["BUY_ANIMAL","SHEEP",1],["BUY_ANIMAL","SHEEP",1]]},{"farmer":["PICKUP","COW",1],"hands":[],"market":[["SELL","WHEAT",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["BUY_ANIMAL","COW",1],["HIRE"]]},{"farmer":["BUILD_PASTURE"],"hands":[["PICKUP","SHEEP",1],["PICKUP","SHEEP",1],["PICKUP","COW",1],["PICKUP","SHEEP",1],["PASS"]],"market":[["SELL","WHEAT",1]]},{"farmer":["PLACE","COW",1],"hands":[["NORTH"],["NORTH"],["NORTH"],["WEST"],["NORTH"]],"market":[["SELL","WHEAT",1],["BUY_PRODUCT","WHEAT",1]]},{"farmer":["PICKUP","WHEAT",3],"hands":[["WEST"],["WEST"],["NORTH"],["BUILD_PASTURE"],["NORTH"]],"market":[["BUY_PRODUCT","WHEAT",1]]},{"farmer":["CARE"],"hands":[["BUILD_PASTURE"],["PLACE","SHEEP",1],["NORTH"],["PASS"],["NORTH"]],"market":[["BUY_SEED","MELON",2],["BUY_PRODUCT","WHEAT",1]]},{"farmer":["WEST"],"hands":[["PLACE","SHEEP",1],["CARE"],["WEST"],["WEST"],["WEST"]],"market":[["BUY_SEED","MELON",2]]},{"farmer":["FEED"],"hands":[["CARE"],["WEST"],["BUILD_PASTURE"],["BUILD_PASTURE"],["PLANT","MELON"]],"market":[]},{"farmer":["EAST"],"hands":[["SOUTH"],["NORTH"],["PLACE","COW",1],["PLACE","SHEEP",1],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["NORTH"],["PLANT","MELON"],["NORTH"],["WEST"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["WEST"],["WATER"],["WEST"],["PLANT","MELON"],["PLANT","WHEAT"]],"market":[["BUY_SEED","MELON",2]]},{"farmer":["SOUTH"],"hands":[["PLANT","MELON"],["NORTH"],["PLANT","WHEAT"],["WATER"],["WATER"]],"market":[["BUY_SEED","WHEAT",3]]},{"farmer":["WEST"],"hands":[["WATER"],["PLANT","WHEAT"],["WATER"],["WEST"],["WEST"]],"market":[["BUY_SEED","MELON",2]]},{"farmer":["WEST"],"hands":[["NORTH"],["WATER"],["WEST"],["PLANT","MELON"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["PLANT","MELON"],["WEST"],["PLANT","WHEAT"],["WATER"],["WATER"]],"market":[["SELL","WHEAT",2]]},{"farmer":["CARE"],"hands":[["WATER"],["PASS"],["WATER"],["NORTH"],["WEST"]],"market":[["BUY_SEED","WHEAT",3]]},{"farmer":["PASS"],"hands":[["PASS"],["PLANT","WHEAT"],["WEST"],["NORTH"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PASS"],"hands":[["SOUTH"],["WATER"],["PLANT","WHEAT"],["PLANT","WHEAT"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PASS"],"hands":[["WEST"],["NORTH"],["WATER"],["WATER"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PASS"],"hands":[["WEST"],["WEST"],["WEST"],["NORTH"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PASS"],"hands":[["PASS"],["PLANT","WHEAT"],["NORTH"],["NORTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PASS"],"hands":[["PASS"],["WATER"],["PLANT","WHEAT"],["PASS"],["PASS"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["WATER"],["PASS"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[],"market":[["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["PLACE","FERTILIZER",1],"hands":[["NORTH"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["NORTH"],["NORTH"]],"market":[["SELL","FERTILIZER",1],["BUY_PRODUCT","WHEAT",3]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WEST"],["WEST"],["WEST"]],"market":[]},{"farmer":["SOUTH"],"hands":[["COLLECT_FERTILIZER"],["SOUTH"],["WEST"]],"market":[]},{"farmer":["DROP"],"hands":[["SOUTH"],["COLLECT_FERTILIZER"],["SOUTH"]],"market":[]},{"farmer":["PICKUP","WHEAT",2],"hands":[["SOUTH"],["EAST"],["WEST"]],"market":[["SELL","FERTILIZER",1],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["FEED"],"hands":[["DROP"],["DROP"],["COLLECT_FERTILIZER"]],"market":[["BUY_SEED","MELON",1]]},{"farmer":["CARE"],"hands":[["PICKUP","WHEAT",2],["PICKUP","WHEAT",1],["EAST"]],"market":[["SELL","FERTILIZER",2],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["NORTH"],"hands":[["NORTH"],["NORTH"],["EAST"]],"market":[["BUY_SEED","MELON",1]]},{"farmer":["CARE"],"hands":[["PASS"],["PASS"],["DROP"]],"market":[["BUY_SEED","MELON",1]]},{"farmer":["FEED"],"hands":[["NORTH"],["WEST"],["PICKUP","WHEAT",2]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["WEST"],"hands":[["CARE"],["WEST"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["FEED"],["SOUTH"],["CARE"]],"market":[]},{"farmer":["WEST"],"hands":[["SOUTH"],["CARE"],["FEED"]],"market":[]},{"farmer":["PLANT","MELON"],"hands":[["PASS"],["FEED"],["PASS"]],"market":[]},{"farmer":["WATER"],"hands":[["PASS"],["WEST"],["PASS"]],"market":[]},{"farmer":["WEST"],"hands":[["PASS"],["WEST"],["PASS"]],"market":[]},{"farmer":["PLANT","MELON"],"hands":[["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["WATER"],"hands":[["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[],"market":[["SELL","WHEAT",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["PLACE","FERTILIZER",1],"hands":[["NORTH"],["NORTH"],["NORTH"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["WEST"],"hands":[["WEST"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["WEST"],["WEST"],["SOUTH"],["WEST"]],"market":[]},{"farmer":["EAST"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["CARE"],["DROP"],["NORTH"]],"market":[["SELL","WHEAT",1]]},{"farmer":["DROP"],"hands":[["SOUTH"],["EAST"],["NORTH"],["NORTH"],["NORTH"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["WEST"],"hands":[["SOUTH"],["EAST"],["NORTH"],["NORTH"],["WATER"]],"market":[]},{"farmer":["WEST"],"hands":[["DROP"],["DROP"],["WATER"],["WEST"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["CARE"],["WEST"],["WEST"],["WATER"],["WATER"]],"market":[["SELL","FERTILIZER",2],["BUY_ANIMAL","COW",1]]},{"farmer":["WATER"],"hands":[["PICKUP","COW",1],["CARE"],["WATER"],["WEST"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["WEST"],["NORTH"],["WEST"],["WATER"],["WATER"]],"market":[]},{"farmer":["WATER"],"hands":[["NORTH"],["WATER"],["WATER"],["WEST"],["WEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["WEST"],["HARVEST"],["WATER"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["WATER"],["SOUTH"],["NORTH"],["HARVEST"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WATER"],"hands":[["HARVEST"],["PASS"],["SOUTH"],["WATER"],["PLANT","STRAWBERRY"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["NORTH"],"hands":[["BUILD_PASTURE"],["PASS"],["SOUTH"],["WEST"],["WATER"]],"market":[]},{"farmer":["WATER"],"hands":[["PLACE","COW",1],["PASS"],["CARE"],["NORTH"],["EAST"]],"market":[]},{"farmer":["HARVEST"],"hands":[["SOUTH"],["PASS"],["FEED"],["WATER"],["SOUTH"]],"market":[]},{"farmer":["PLANT","STRAWBERRY"],"hands":[["SOUTH"],["PASS"],["EAST"],["HARVEST"],["EAST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["EAST"],["NORTH"],["FEED"],["PASS"],["SOUTH"]],"market":[]},{"farmer":["EAST"],"hands":[["FEED"],["NORTH"],["PASS"],["PLANT","WHEAT"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PASS"],"hands":[["PASS"],["PLANT","WHEAT"],["PASS"],["WATER"],["SOUTH"]],"market":[]},{"farmer":["SOUTH"],"hands":[["SOUTH"],["WATER"],["PASS"],["SOUTH"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[],"market":[["SELL","WHEAT",7],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["DROP"],"hands":[["NORTH"],["NORTH"],["NORTH"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["WEST"],"hands":[["WEST"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["WEST"],["NORTH"],["SOUTH"],["WEST"]],"market":[]},{"farmer":["EAST"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WEST"],["DROP"],["NORTH"]],"market":[]},{"farmer":["DROP"],"hands":[["SOUTH"],["EAST"],["NORTH"],["NORTH"],["NORTH"]],"market":[["SELL","FERTILIZER",1],["BUY_ANIMAL","COW",1]]},{"farmer":["PICKUP","COW",1],"hands":[["SOUTH"],["EAST"],["WEST"],["NORTH"],["WATER"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["NORTH"],"hands":[["DROP"],["DROP"],["COLLECT_FERTILIZER"],["NORTH"],["HARVEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["CARE"],["PASS"],["SOUTH"],["WEST"],["SOUTH"]],"market":[["SELL","FERTILIZER",2],["BUY_ANIMAL","COW",1]]},{"farmer":["NORTH"],"hands":[["WEST"],["WEST"],["SOUTH"],["NORTH"],["SOUTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["CARE"],["WEST"],["EAST"],["WATER"],["FEED"]],"market":[]},{"farmer":["BUILD_PASTURE"],"hands":[["NORTH"],["NORTH"],["SOUTH"],["HARVEST"],["CARE"]],"market":[]},{"farmer":["PLACE","COW",1],"hands":[["WEST"],["NORTH"],["DROP"],["SOUTH"],["SOUTH"]],"market":[]},{"farmer":["WEST"],"hands":[["WEST"],["WATER"],["PASS"],["FEED"],["CARE"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PLANT","STRAWBERRY"],"hands":[["WATER"],["WEST"],["PASS"],["CARE"],["FEED"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WATER"],"hands":[["WEST"],["WATER"],["PASS"],["SOUTH"],["SOUTH"]],"market":[]},{"farmer":["WEST"],"hands":[["WATER"],["NORTH"],["PASS"],["SOUTH"],["FEED"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WATER"],"hands":[["NORTH"],["WATER"],["PASS"],["SOUTH"],["PASS"]],"market":[]},{"farmer":["HARVEST"],"hands":[["WATER"],["HARVEST"],["PASS"],["FEED"],["PASS"]],"market":[]},{"farmer":["PLANT","STRAWBERRY"],"hands":[["HARVEST"],["PLANT","STRAWBERRY"],["PASS"],["WEST"],["PASS"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WATER"],"hands":[["PLANT","STRAWBERRY"],["WATER"],["PASS"],["FEED"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["WATER"],["PASS"],["PASS"],["CARE"],["PASS"]],"market":[]},{"farmer":["WEST"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["WATER"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[],"market":[["SELL","WHEAT",10],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["DROP"],"hands":[["NORTH"],["NORTH"],["NORTH"],["NORTH"],["NORTH"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["WEST"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["WEST"],["NORTH"],["SOUTH"],["NORTH"],["WEST"]],"market":[]},{"farmer":["EAST"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WEST"],["DROP"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["DROP"],"hands":[["SOUTH"],["EAST"],["NORTH"],["NORTH"],["PASS"],["NORTH"]],"market":[["SELL","FERTILIZER",2],["BUY_ANIMAL","COW",1]]},{"farmer":["PICKUP","COW",1],"hands":[["SOUTH"],["EAST"],["WATER"],["NORTH"],["WEST"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["DROP"],["DROP"],["WEST"],["WEST"],["COLLECT_FERTILIZER"],["HARVEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["CARE"],["WEST"],["COLLECT_FERTILIZER"],["WATER"],["SOUTH"],["EAST"]],"market":[["SELL","FERTILIZER",2],["BUY_ANIMAL","COW",1]]},{"farmer":["WEST"],"hands":[["WEST"],["WEST"],["SOUTH"],["WEST"],["SOUTH"],["EAST"]],"market":[]},{"farmer":["WEST"],"hands":[["CARE"],["WEST"],["SOUTH"],["NORTH"],["SOUTH"],["NORTH"]],"market":[]},{"farmer":["BUILD_COOP"],"hands":[["WEST"],["WATER"],["EAST"],["WATER"],["SOUTH"],["NORTH"]],"market":[]},{"farmer":["DIG"],"hands":[["NORTH"],["WEST"],["SOUTH"],["WEST"],["DROP"],["FEED"]],"market":[["BUY_ANIMAL","COW",1]]},{"farmer":["BUILD_PASTURE"],"hands":[["WATER"],["WATER"],["DROP"],["WEST"],["PASS"],["CARE"]],"market":[["SELL","FERTILIZER",2],["BUY_ANIMAL","COW",1]]},{"farmer":["PLACE","COW",1],"hands":[["EAST"],["NORTH"],["PICKUP","COW",1],["WATER"],["PASS"],["SOUTH"]],"market":[]},{"farmer":["WEST"],"hands":[["WATER"],["NORTH"],["WEST"],["NORTH"],["PASS"],["SOUTH"]],"market":[["BUY_PRODUCT","WHEAT",2]]},{"farmer":["WATER"],"hands":[["EAST"],["PASS"],["NORTH"],["WATER"],["PICKUP","WHEAT",2],["FEED"]],"market":[]},{"farmer":["HARVEST"],"hands":[["CARE"],["PASS"],["WEST"],["HARVEST"],["FEED"],["CARE"]],"market":[]},{"farmer":["SOUTH"],"hands":[["SOUTH"],["PASS"],["NORTH"],["PASS"],["WEST"],["SOUTH"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["SOUTH"],"hands":[["PASS"],["PASS"],["WEST"],["PASS"],["FEED"],["FEED"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["EAST"],"hands":[["PASS"],["PASS"],["BUILD_PASTURE"],["PASS"],["WEST"],["PASS"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["FEED"],"hands":[["PASS"],["PASS"],["PLACE","COW",1],["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["CARE"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"],["PASS"],["SOUTH"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["WATER"],["PASS"],["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[],"market":[["SELL","WHEAT",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["PLACE","FERTILIZER",1],"hands":[["NORTH"],["NORTH"],["NORTH"],["NORTH"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WEST"],["WEST"],["NORTH"],["SOUTH"],["WEST"],["WEST"]],"market":[]},{"farmer":["EAST"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WEST"],["DROP"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["DROP"],"hands":[["SOUTH"],["EAST"],["NORTH"],["CARE"],["NORTH"],["NORTH"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["PICKUP","WHEAT",3],"hands":[["SOUTH"],["EAST"],["WEST"],["PICKUP","WHEAT",2],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["WEST"],"hands":[["PLACE","FERTILIZER",1],["PLACE","FERTILIZER",1],["COLLECT_FERTILIZER"],["WEST"],["SOUTH"],["WEST"]],"market":[["BUY_PRODUCT","WHEAT",2]]},{"farmer":["FEED"],"hands":[["PASS"],["PASS"],["SOUTH"],["WEST"],["SOUTH"],["COLLECT_FERTILIZER"]],"market":[["SELL","FERTILIZER",2],["BUY_ANIMAL","COW",1]]},{"farmer":["CARE"],"hands":[["PICKUP","COW",1],["PASS"],["EAST"],["FEED"],["SOUTH"],["SOUTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["WEST"],["PICKUP","WHEAT",2],["SOUTH"],["CARE"],["SOUTH"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["FEED"],["SOUTH"],["NORTH"],["DROP"],["EAST"]],"market":[["BUY_PRODUCT","WHEAT",2]]},{"farmer":["NORTH"],"hands":[["NORTH"],["NORTH"],["DROP"],["NORTH"],["NORTH"],["EAST"]],"market":[["SELL","FERTILIZER",2],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["FEED"],"hands":[["WEST"],["CARE"],["PICKUP","WHEAT",2],["WEST"],["NORTH"],["EAST"]],"market":[]},{"farmer":["CARE"],"hands":[["NORTH"],["FEED"],["NORTH"],["FEED"],["NORTH"],["SOUTH"]],"market":[]},{"farmer":["WEST"],"hands":[["WATER"],["WEST"],["NORTH"],["CARE"],["NORTH"],["DROP"]],"market":[["BUY_PRODUCT","WHEAT",2]]},{"farmer":["SOUTH"],"hands":[["HARVEST"],["WEST"],["FEED"],["NORTH"],["WEST"],["PICKUP","WHEAT",2]],"market":[["SELL","FERTILIZER",2],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["FEED"],"hands":[["BUILD_PASTURE"],["WEST"],["CARE"],["WATER"],["WATER"],["NORTH"]],"market":[]},{"farmer":["CARE"],"hands":[["PLACE","COW",1],["WEST"],["NORTH"],["NORTH"],["WEST"],["NORTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["FEED"],["WATER"],["NORTH"],["WATER"],["WATER"],["NORTH"]],"market":[]},{"farmer":["CARE"],"hands":[["PASS"],["NORTH"],["FEED"],["WEST"],["WEST"],["NORTH"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["WATER"],["CARE"],["PLANT","STRAWBERRY"],["PASS"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["NORTH"],["PASS"],["WATER"],["PASS"],["SOUTH"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["WATER"],["PASS"],["PASS"],["PASS"],["SOUTH"]],"market":[]},{"farmer":["NORTH"],"hands":[],"market":[["SELL","WHEAT",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["HARVEST"],"hands":[["WEST"],["WEST"],["PICKUP","WHEAT",3],["NORTH"],["WEST"],["WEST"],["NORTH"],["NORTH"],["WEST"]],"market":[]},{"farmer":["SOUTH"],"hands":[["HARVEST"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"],["WEST"],["NORTH"],["WEST"],["NORTH"],["WEST"]],"market":[]},{"farmer":["DROP"],"hands":[["EAST"],["PLACE","FERTILIZER",1],["WEST"],["NORTH"],["HARVEST"],["NORTH"],["WEST"],["NORTH"],["WEST"]],"market":[["SELL","WOOL",6],["BUY_LAND"]]},{"farmer":["NORTH"],"hands":[["DROP"],["NORTH"],["FEED"],["EAST"],["EAST"],["NORTH"],["NORTH"],["EAST"],["WATER"]],"market":[["SELL","WOOL",6],["BUY_ANIMAL","COW",1],["BUY_SEED","WHEAT",1],["BUY_SEED","STRAWBERRY",1],["BUY_SEED","STRAWBERRY",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["PICKUP","COW",1],["NORTH"],["CARE"],["EAST"],["EAST"],["WATER"],["WATER"],["EAST"],["WEST"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["EAST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["PLANT","STRAWBERRY"],["DROP"],["NORTH"],["NORTH"],["EAST"],["WATER"]],"market":[["SELL","WOOL",6],["BUY_PRODUCT","WHEAT",1]]},{"farmer":["PLACE","FERTILIZER",1],"hands":[["BUILD_PASTURE"],["SOUTH"],["WEST"],["WATER"],["PICKUP","WHEAT",2],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["PLANT","STRAWBERRY"],["EAST"]],"market":[["BUY_ANIMAL","GOOSE",1]]},{"farmer":["PICKUP","GOOSE",1],"hands":[["PLACE","COW",1],["SOUTH"],["FEED"],["NORTH"],["FEED"],["SOUTH"],["NORTH"],["WATER"],["NORTH"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","MELON",2],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["EAST"],"hands":[["EAST"],["DROP"],["CARE"],["PLANT","STRAWBERRY"],["CARE"],["SOUTH"],["COLLECT_FERTILIZER"],["EAST"],["NORTH"]],"market":[["BUY_ANIMAL","GOOSE",1],["BUY_SEED","STRAWBERRY",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["NORTH"],"hands":[["PLANT","MELON"],["PICKUP","GOOSE",1],["COLLECT_FERTILIZER"],["WATER"],["NORTH"],["SOUTH"],["EAST"],["PLANT","STRAWBERRY"],["COLLECT_FERTILIZER"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","MELON",2],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["BUILD_COOP"],"hands":[["WATER"],["EAST"],["EAST"],["EAST"],["FEED"],["SOUTH"],["COLLECT_FERTILIZER"],["WATER"],["EAST"]],"market":[["BUY_PRODUCT","WHEAT",2]]},{"farmer":["PLACE","GOOSE",1],"hands":[["EAST"],["NORTH"],["EAST"],["PLANT","STRAWBERRY"],["CARE"],["DROP"],["SOUTH"],["SOUTH"],["EAST"]],"market":[["BUY_ANIMAL","GOOSE",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["SOUTH"],"hands":[["PLANT","MELON"],["NORTH"],["DROP"],["WATER"],["SOUTH"],["PICKUP","GOOSE",1],["WATER"],["PLANT","STRAWBERRY"],["SOUTH"]],"market":[["SELL","FERTILIZER",2],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PICKUP","WHEAT",2],"hands":[["WATER"],["BUILD_COOP"],["PICKUP","WHEAT",1],["EAST"],["PASS"],["EAST"],["SOUTH"],["WATER"],["WATER"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["NORTH"],"hands":[["EAST"],["PLACE","GOOSE",1],["NORTH"],["PLANT","STRAWBERRY"],["NORTH"],["NORTH"],["EAST"],["SOUTH"],["EAST"]],"market":[["BUY_PRODUCT","WHEAT",2]]},{"farmer":["FEED"],"hands":[["PLANT","MELON"],["NORTH"],["NORTH"],["WATER"],["SOUTH"],["EAST"],["SOUTH"],["PLANT","STRAWBERRY"],["SOUTH"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["CARE"],"hands":[["WATER"],["PLANT","STRAWBERRY"],["FEED"],["NORTH"],["PICKUP","WHEAT",2],["BUILD_COOP"],["DROP"],["WATER"],["DROP"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["NORTH"],"hands":[["NORTH"],["WATER"],["CARE"],["PLANT","STRAWBERRY"],["NORTH"],["PLACE","GOOSE",1],["PASS"],["NORTH"],["NORTH"]],"market":[["SELL","FERTILIZER",3],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["FEED"],"hands":[["PLANT","STRAWBERRY"],["NORTH"],["NORTH"],["WATER"],["NORTH"],["EAST"],["PASS"],["NORTH"],["NORTH"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["CARE"],"hands":[["WATER"],["PLANT","STRAWBERRY"],["WEST"],["WEST"],["WEST"],["PLANT","STRAWBERRY"],["PASS"],["NORTH"],["EAST"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["EAST"],"hands":[["PASS"],["WATER"],["CARE"],["PLANT","STRAWBERRY"],["NORTH"],["WATER"],["PASS"],["WEST"],["EAST"]],"market":[]},{"farmer":["PLANT","STRAWBERRY"],"hands":[["PASS"],["WEST"],["PASS"],["WATER"],["FEED"],["WEST"],["PASS"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["WATER"],"hands":[["PASS"],["CARE"],["PASS"],["PASS"],["PASS"],["PASS"],["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[],"market":[["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["PLACE","FERTILIZER",1],"hands":[["CARE"],["NORTH"],["NORTH"],["WEST"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"]],"market":[["BUY_PRODUCT","WHEAT",6]]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",3],["WEST"],["PASS"],["COLLECT_FERTILIZER"],["DROP"],["NORTH"],["NORTH"]],"market":[["SELL","FERTILIZER",1],["BUY_PRODUCT","WHEAT",5]]},{"farmer":["WEST"],"hands":[["FEED"],["WEST"],["NORTH"],["EAST"],["NORTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["NORTH"],["NORTH"],["DROP"],["NORTH"],["SOUTH"],["SOUTH"]],"market":[["BUY_PRODUCT","WHEAT",2]]},{"farmer":["EAST"],"hands":[["EAST"],["WATER"],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",4],["WEST"],["DROP"],["DROP"]],"market":[["SELL","FERTILIZER",2],["BUY_PRODUCT","WHEAT",5]]},{"farmer":["EAST"],"hands":[["FEED"],["NORTH"],["SOUTH"],["WEST"],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",4],["PICKUP","WHEAT",2]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["DROP"],"hands":[["CARE"],["COLLECT_FERTILIZER"],["SOUTH"],["FEED"],["SOUTH"],["WEST"],["NORTH"]],"market":[["BUY_PRODUCT","WHEAT",2]]},{"farmer":["PICKUP","WHEAT",2],"hands":[["COLLECT_FERTILIZER"],["NORTH"],["DROP"],["CARE"],["SOUTH"],["WEST"],["WEST"]],"market":[["SELL","FERTILIZER",2],["BUY_PRODUCT","WHEAT",5]]},{"farmer":["CARE"],"hands":[["WEST"],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",3],["NORTH"],["DROP"],["FEED"],["FEED"]],"market":[["BUY_LAND"]]},{"farmer":["FEED"],"hands":[["SOUTH"],["EAST"],["NORTH"],["WATER"],["WEST"],["CARE"],["CARE"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["NORTH"],"hands":[["DROP"],["COLLECT_FERTILIZER"],["FEED"],["NORTH"],["WEST"],["WEST"],["NORTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["PICKUP","WHEAT",2],["SOUTH"],["CARE"],["WATER"],["WEST"],["WATER"],["FEED"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["CARE"],"hands":[["NORTH"],["SOUTH"],["NORTH"],["WEST"],["WEST"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["EAST"],["FEED"],["FEED"],["WATER"],["WATER"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["CARE"],["SOUTH"],["NORTH"],["CARE"],["NORTH"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["FEED"],"hands":[["WEST"],["DROP"],["EAST"],["NORTH"],["WATER"],["FEED"],["WEST"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["CARE"],"hands":[["WEST"],["PASS"],["PLANT","MELON"],["FEED"],["NORTH"],["CARE"],["WATER"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["PASS"],["WATER"],["CARE"],["WATER"],["COLLECT_FERTILIZER"],["WEST"]],"market":[]},{"farmer":["EAST"],"hands":[["FEED"],["PASS"],["NORTH"],["WEST"],["NORTH"],["NORTH"],["WATER"]],"market":[]},{"farmer":["EAST"],"hands":[["CARE"],["PASS"],["PLANT","WHEAT"],["WATER"],["WATER"],["NORTH"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["PASS"],["PASS"],["EAST"],["PASS"],["NORTH"],["WATER"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["SOUTH"],["PASS"],["PLANT","WHEAT"],["SOUTH"],["WATER"],["PASS"],["PASS"]],"market":[]},{"farmer":["WATER"],"hands":[["PASS"],["PASS"],["WATER"],["PASS"],["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["HARVEST"],"hands":[],"market":[["SELL","FERTILIZER",2],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["DROP"],"hands":[["CARE"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["WEST"],["EAST"],["NORTH"],["NORTH"],["NORTH"],["EAST"]],"market":[["SELL","MILK",6],["HIRE"]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["NORTH"],["NORTH"],["WEST"],["WATER"],["WEST"],["NORTH"],["NORTH"],["EAST"],["NORTH"]],"market":[["BUY_PRODUCT","WHEAT",6],["BUY_PRODUCT","WHEAT",6]]},{"farmer":["PLACE","FERTILIZER",1],"hands":[["PLACE","FERTILIZER",1],["WEST"],["WEST"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["HARVEST"],["WATER"],["NORTH"]],"market":[]},{"farmer":["PICKUP","WHEAT",4],"hands":[["PICKUP","WHEAT",4],["FEED"],["NORTH"],["WATER"],["COLLECT_FERTILIZER"],["EAST"],["NORTH"],["SOUTH"],["EAST"],["COLLECT_FERTILIZER"]],"market":[["SELL","FERTILIZER",2],["BUY_LAND"]]},{"farmer":["FEED"],"hands":[["NORTH"],["CARE"],["CARE"],["WEST"],["NORTH"],["PLACE","FERTILIZER",1],["COLLECT_FERTILIZER"],["SOUTH"],["WATER"],["SOUTH"]],"market":[["BUY_LAND"]]},{"farmer":["CARE"],"hands":[["FEED"],["WEST"],["FEED"],["WATER"],["WATER"],["PICKUP","WHEAT",2],["SOUTH"],["DROP"],["EAST"],["DROP"]],"market":[["SELL","MILK",6],["BUY_LAND"]]},{"farmer":["NORTH"],"hands":[["CARE"],["FEED"],["NORTH"],["SOUTH"],["EAST"],["WEST"],["SOUTH"],["SOUTH"],["WATER"],["WEST"]],"market":[["SELL","FERTILIZER",2],["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["NORTH"],["CARE"],["FEED"],["PLANT","WHEAT"],["WATER"],["NORTH"],["DROP"],["SOUTH"],["NORTH"],["WEST"]],"market":[["BUY_ANIMAL","GOOSE",1],["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["FEED"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"],["NORTH"],["WATER"],["PICKUP","GOOSE",1],["SOUTH"],["WATER"],["SOUTH"]],"market":[["SELL","FERTILIZER",2],["BUY_ANIMAL","GOOSE",1],["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["CARE"],["EAST"],["WATER"],["SOUTH"],["WATER"],["WEST"],["SOUTH"],["SOUTH"],["NORTH"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["NORTH"],["EAST"],["WEST"],["PLANT","WHEAT"],["EAST"],["WATER"],["WEST"],["SOUTH"],["WATER"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WATER"],["DROP"],["FEED"],["WATER"],["WATER"],["WEST"],["WEST"],["PLANT","WHEAT"],["NORTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["NORTH"],["PICKUP","GOOSE",1],["CARE"],["SOUTH"],["SOUTH"],["WATER"],["BUILD_COOP"],["WATER"],["WATER"],["SOUTH"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["WEST"],["SOUTH"],["COLLECT_FERTILIZER"],["PLANT","WHEAT"],["WATER"],["WEST"],["PLACE","GOOSE",1],["WEST"],["NORTH"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["FEED"],["WEST"],["SOUTH"],["WATER"],["SOUTH"],["WATER"],["SOUTH"],["PLANT","WHEAT"],["WATER"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["CARE"],["WEST"],["SOUTH"],["SOUTH"],["WATER"],["NORTH"],["SOUTH"],["WATER"],["WEST"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["COLLECT_FERTILIZER"],["BUILD_COOP"],["EAST"],["PLANT","WHEAT"],["WEST"],["EAST"],["PLANT","WHEAT"],["WEST"],["WATER"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["WEST"],["PLACE","GOOSE",1],["SOUTH"],["WATER"],["WATER"],["FEED"],["WATER"],["PLANT","WHEAT"],["PASS"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["WATER"],["WEST"],["DROP"],["SOUTH"],["WEST"],["CARE"],["SOUTH"],["WATER"],["PASS"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WEST"],["PLANT","WHEAT"],["SOUTH"],["PLANT","WHEAT"],["WEST"],["COLLECT_FERTILIZER"],["PLANT","WHEAT"],["WEST"],["PASS"],["PLANT","WHEAT"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["WATER"],["WATER"],["SOUTH"],["WATER"],["SOUTH"],["WEST"],["WATER"],["PLANT","WHEAT"],["PASS"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WEST"],["SOUTH"],["SOUTH"],["PASS"],["DROP"],["WATER"],["EAST"],["WATER"],["PASS"],["NORTH"]],"market":[]},{"farmer":["WEST"],"hands":[["WATER"],["PASS"],["PASS"],["PASS"],["PASS"],["NORTH"],["PASS"],["PASS"],["PASS"],["PASS"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["NORTH"],"hands":[],"market":[["SELL","FERTILIZER",6],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["HARVEST"],"hands":[["WEST"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["PASS"],["WEST"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["NORTH"]],"market":[["BUY_PRODUCT","WHEAT",6],["BUY_PRODUCT","WHEAT",5],["BUY_PRODUCT","WHEAT",6]]},{"farmer":["SOUTH"],"hands":[["HARVEST"],["FEED"],["WEST"],["PICKUP","WHEAT",3],["WEST"],["DROP"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"]],"market":[]},{"farmer":["DROP"],"hands":[["EAST"],["CARE"],["FEED"],["NORTH"],["HARVEST"],["PICKUP","WHEAT",4],["EAST"],["COLLECT_FERTILIZER"],["WATER"]],"market":[["SELL","WOOL",4],["BUY_PRODUCT","WHEAT",6]]},{"farmer":["PICKUP","WHEAT",3],"hands":[["DROP"],["NORTH"],["CARE"],["NORTH"],["EAST"],["NORTH"],["PLACE","FERTILIZER",1],["NORTH"],["WEST"]],"market":[["SELL","WOOL",4],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["FEED"],["WEST"],["NORTH"],["EAST"],["WEST"],["PICKUP","WHEAT",2],["COLLECT_FERTILIZER"],["WATER"]],"market":[["SELL","FERTILIZER",2],["BUY_ANIMAL","GOOSE",1]]},{"farmer":["FEED"],"hands":[["PLACE","FERTILIZER",1],["CARE"],["FEED"],["FEED"],["DROP"],["FEED"],["PICKUP","GOOSE",1],["NORTH"],["WEST"]],"market":[["SELL","WOOL",4],["BUY_SEED","TOMATO",1]]},{"farmer":["CARE"],"hands":[["PICKUP","WHEAT",4],["EAST"],["CARE"],["CARE"],["PICKUP","WHEAT",3],["CARE"],["BUILD_COOP"],["NORTH"],["WATER"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FEED"],["FEED"],["COLLECT_FERTILIZER"],["WEST"],["PASS"],["COLLECT_FERTILIZER"],["PLACE","GOOSE",1],["WATER"],["WEST"]],"market":[["BUY_SEED","TOMATO",1]]},{"farmer":["WEST"],"hands":[["CARE"],["CARE"],["SOUTH"],["FEED"],["WEST"],["NORTH"],["FEED"],["EAST"],["WATER"]],"market":[]},{"farmer":["FEED"],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["WEST"],["CARE"],["WEST"],["NORTH"],["CARE"],["WATER"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["NORTH"],["WEST"],["PLANT","WHEAT"],["COLLECT_FERTILIZER"],["WEST"],["WATER"],["SOUTH"],["HARVEST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WEST"],["SOUTH"],["WATER"],["WEST"],["WATER"],["NORTH"],["SOUTH"],["PLANT","STRAWBERRY"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","TOMATO",1]]},{"farmer":["EAST"],"hands":[["WATER"],["DROP"],["SOUTH"],["NORTH"],["SOUTH"],["FEED"],["SOUTH"],["WATER"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["EAST"],"hands":[["WEST"],["EAST"],["PLANT","TOMATO"],["FEED"],["SOUTH"],["CARE"],["PLANT","TOMATO"],["SOUTH"],["WATER"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","WHEAT",1]]},{"farmer":["PLACE","FERTILIZER",2],"hands":[["FEED"],["EAST"],["WATER"],["CARE"],["EAST"],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["NORTH"]],"market":[]},{"farmer":["SOUTH"],"hands":[["CARE"],["NORTH"],["SOUTH"],["COLLECT_FERTILIZER"],["EAST"],["SOUTH"],["NORTH"],["EAST"],["WATER"]],"market":[["SELL","FERTILIZER",2],["BUY_SEED","TOMATO",1]]},{"farmer":["SOUTH"],"hands":[["COLLECT_FERTILIZER"],["WATER"],["WEST"],["NORTH"],["PLANT","WHEAT"],["SOUTH"],["PLANT","TOMATO"],["WATER"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PLANT","TOMATO"],"hands":[["WEST"],["NORTH"],["WATER"],["WATER"],["WATER"],["SOUTH"],["WATER"],["NORTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","TOMATO",1]]},{"farmer":["WATER"],"hands":[["FEED"],["WATER"],["SOUTH"],["WEST"],["PASS"],["SOUTH"],["SOUTH"],["WATER"],["EAST"]],"market":[]},{"farmer":["PASS"],"hands":[["CARE"],["EAST"],["WATER"],["WATER"],["PASS"],["DROP"],["SOUTH"],["HARVEST"],["WATER"]],"market":[]},{"farmer":["PASS"],"hands":[["COLLECT_FERTILIZER"],["WATER"],["EAST"],["SOUTH"],["PASS"],["PASS"],["WEST"],["PLANT","TOMATO"],["SOUTH"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["PASS"],"hands":[["SOUTH"],["NORTH"],["WATER"],["COLLECT_FERTILIZER"],["SOUTH"],["PASS"],["WEST"],["WATER"],["EAST"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["WATER"],["PASS"],["CARE"],["WATER"],["PASS"],["WATER"],["EAST"],["PASS"]],"market":[]},{"farmer":["WEST"],"hands":[],"market":[["SELL","FERTILIZER",9],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["WEST"],["PICKUP","WHEAT",4],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["NORTH"],["EAST"],["WEST"],["NORTH"],["NORTH"]],"market":[["HIRE"],["HIRE"],["BUY_PRODUCT","WHEAT",12]]},{"farmer":["WATER"],"hands":[["WEST"],["FEED"],["FEED"],["WEST"],["NORTH"],["WATER"],["NORTH"],["PICKUP","WHEAT",4],["WEST"],["HARVEST"],["NORTH"]],"market":[]},{"farmer":["HARVEST"],"hands":[["WEST"],["CARE"],["CARE"],["WEST"],["NORTH"],["EAST"],["WEST"],["NORTH"],["WEST"],["DROP"],["WEST"]],"market":[["SELL","MILK",3]]},{"farmer":["SOUTH"],"hands":[["WATER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FEED"],["WATER"],["WATER"],["WEST"],["FEED"],["WATER"],["PICKUP","WHEAT",4],["NORTH"]],"market":[]},{"farmer":["EAST"],"hands":[["HARVEST"],["NORTH"],["SOUTH"],["CARE"],["HARVEST"],["EAST"],["WEST"],["CARE"],["HARVEST"],["WEST"],["WATER"]],"market":[]},{"farmer":["DROP"],"hands":[["EAST"],["HARVEST"],["SOUTH"],["COLLECT_FERTILIZER"],["SOUTH"],["WATER"],["WATER"],["NORTH"],["EAST"],["FEED"],["HARVEST"]],"market":[["SELL","MELON",6],["BUY_PRODUCT","WHEAT",12]]},{"farmer":["PICKUP","WHEAT",4],"hands":[["EAST"],["COLLECT_FERTILIZER"],["SOUTH"],["WEST"],["SOUTH"],["EAST"],["HARVEST"],["FEED"],["SOUTH"],["CARE"],["SOUTH"]],"market":[["BUY_PRODUCT","WHEAT",6]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["EAST"],["EAST"],["SOUTH"],["COLLECT_FERTILIZER"],["SOUTH"],["WATER"],["EAST"],["CARE"],["EAST"],["COLLECT_FERTILIZER"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["DROP"],["FEED"],["WATER"],["SOUTH"],["DROP"],["NORTH"],["EAST"],["HARVEST"],["DROP"],["WEST"],["EAST"]],"market":[["SELL","MELON",12],["SELL","MELON",6]]},{"farmer":["FEED"],"hands":[["PICKUP","WHEAT",4],["CARE"],["WEST"],["WATER"],["PICKUP","WHEAT",3],["WATER"],["EAST"],["COLLECT_FERTILIZER"],["WEST"],["FEED"],["DROP"]],"market":[["SELL","MELON",6],["BUY_SEED","TOMATO",1]]},{"farmer":["CARE"],"hands":[["CARE"],["COLLECT_FERTILIZER"],["WATER"],["SOUTH"],["NORTH"],["NORTH"],["EAST"],["NORTH"],["WEST"],["CARE"],["WEST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FEED"],["HARVEST"],["NORTH"],["WATER"],["NORTH"],["WATER"],["DROP"],["WATER"],["COLLECT_FERTILIZER"],["WEST"],["WEST"]],"market":[["SELL","MELON",6]]},{"farmer":["NORTH"],"hands":[["WEST"],["NORTH"],["WATER"],["SOUTH"],["FEED"],["NORTH"],["PICKUP","WHEAT",2],["WEST"],["WEST"],["PLANT","WHEAT"],["WEST"]],"market":[["BUY_SEED","TOMATO",1]]},{"farmer":["CARE"],"hands":[["NORTH"],["WATER"],["NORTH"],["WATER"],["WEST"],["WATER"],["WEST"],["PLANT","WHEAT"],["WATER"],["WEST"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["PLANT","WHEAT"],["SOUTH"],["FERTILIZE"],["WEST"],["PLANT","WHEAT"],["NORTH"],["NORTH"],["WATER"],["SOUTH"],["PLANT","WHEAT"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["EAST"],["WATER"],["WATER"],["WATER"],["WATER"],["WEST"],["NORTH"],["FERTILIZE"],["WATER"],["WATER"]],"market":[]},{"farmer":["SOUTH"],"hands":[["NORTH"],["EAST"],["SOUTH"],["SOUTH"],["NORTH"],["WEST"],["PLANT","WHEAT"],["FEED"],["WATER"],["SOUTH"],["EAST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["WEST"],["WATER"],["WEST"],["WATER"],["HARVEST"],["WATER"],["WATER"],["CARE"],["SOUTH"],["FERTILIZE"],["WATER"]],"market":[]},{"farmer":["DROP"],"hands":[["FEED"],["WEST"],["SOUTH"],["WEST"],["FEED"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["WEST"],["WATER"],["NORTH"]],"market":[["SELL","MILK",3]]},{"farmer":["PICKUP","WHEAT",2],"hands":[["CARE"],["WATER"],["WATER"],["WATER"],["CARE"],["WATER"],["NORTH"],["WEST"],["WATER"],["SOUTH"],["NORTH"]],"market":[["SELL","FERTILIZER",3]]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["NORTH"],["HARVEST"],["NORTH"],["COLLECT_FERTILIZER"],["WEST"],["FEED"],["WATER"],["SOUTH"],["SOUTH"],["WATER"]],"market":[]},{"farmer":["WEST"],"hands":[["WEST"],["WATER"],["PLANT","TOMATO"],["FERTILIZE"],["WEST"],["WATER"],["CARE"],["WEST"],["WATER"],["EAST"],["SOUTH"]],"market":[]},{"farmer":["PASS"],"hands":[["CARE"],["NORTH"],["WATER"],["WATER"],["COLLECT_FERTILIZER"],["WEST"],["PASS"],["WATER"],["PASS"],["WATER"],["PASS"]],"market":[]},{"farmer":["WEST"],"hands":[],"market":[["SELL","FERTILIZER",10],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["WEST"],["PICKUP","WHEAT",4],["SOUTH"],["SOUTH"],["NORTH"]],"market":[["SELL","MILK",6],["HIRE"],["BUY_SEED","TOMATO",1]]},{"farmer":["WEST"],"hands":[["CARE"],["FEED"],["CARE"],["WEST"],["WEST"],["NORTH"],["WATER"],["SOUTH"],["NORTH"],["PICKUP","WHEAT",4]],"market":[]},{"farmer":["NORTH"],"hands":[["FEED"],["CARE"],["FEED"],["WEST"],["NORTH"],["FEED"],["SOUTH"],["WEST"],["NORTH"],["WEST"]],"market":[]},{"farmer":["WATER"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FEED"],["WEST"],["CARE"],["WATER"],["SOUTH"],["NORTH"],["FEED"]],"market":[]},{"farmer":["HARVEST"],"hands":[["NORTH"],["NORTH"],["WEST"],["CARE"],["WEST"],["COLLECT_FERTILIZER"],["WEST"],["WATER"],["HARVEST"],["CARE"]],"market":[]},{"farmer":["EAST"],"hands":[["FEED"],["NORTH"],["WEST"],["COLLECT_FERTILIZER"],["WATER"],["NORTH"],["WATER"],["SOUTH"],["SOUTH"],["COLLECT_FERTILIZER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["EAST"],"hands":[["CARE"],["FEED"],["FEED"],["SOUTH"],["HARVEST"],["WEST"],["HARVEST"],["WATER"],["SOUTH"],["WEST"]],"market":[]},{"farmer":["SOUTH"],"hands":[["COLLECT_FERTILIZER"],["CARE"],["CARE"],["FERTILIZE"],["EAST"],["FEED"],["PLANT","TOMATO"],["WEST"],["SOUTH"],["FEED"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["EAST"],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WATER"],["EAST"],["CARE"],["WATER"],["WATER"],["SOUTH"],["CARE"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["DROP"],"hands":[["COLLECT_FERTILIZER"],["HARVEST"],["WEST"],["WEST"],["EAST"],["NORTH"],["WEST"],["HARVEST"],["DROP"],["COLLECT_FERTILIZER"]],"market":[["SELL","MELON",6]]},{"farmer":["PICKUP","WHEAT",2],"hands":[["NORTH"],["EAST"],["WATER"],["WATER"],["SOUTH"],["NORTH"],["WATER"],["PLANT","TOMATO"],["PICKUP","WHEAT",2],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["WEST"],["SOUTH"],["HARVEST"],["HARVEST"],["EAST"],["FEED"],["HARVEST"],["WATER"],["WEST"],["NORTH"]],"market":[]},{"farmer":["WEST"],"hands":[["FEED"],["FEED"],["PLANT","WHEAT"],["PLANT","WHEAT"],["DROP"],["CARE"],["PLANT","WHEAT"],["WEST"],["WEST"],["FEED"]],"market":[["SELL","MELON",6],["BUY_SEED","TOMATO",1]]},{"farmer":["WEST"],"hands":[["CARE"],["CARE"],["WATER"],["WATER"],["PICKUP","WHEAT",2],["COLLECT_FERTILIZER"],["WATER"],["WEST"],["WEST"],["CARE"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","TOMATO",1]]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WEST"],["WEST"],["NORTH"],["EAST"],["SOUTH"],["WATER"],["NORTH"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["PLANT","WHEAT"],"hands":[["WEST"],["HARVEST"],["WATER"],["WATER"],["EAST"],["WATER"],["WATER"],["HARVEST"],["NORTH"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["FEED"],["EAST"],["HARVEST"],["WEST"],["HARVEST"],["EAST"],["HARVEST"],["PLANT","TOMATO"],["FEED"],["WEST"]],"market":[["SELL","MILK",6],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["CARE"],["WATER"],["PLANT","WHEAT"],["WATER"],["SOUTH"],["SOUTH"],["PLANT","TOMATO"],["WATER"],["CARE"],["WEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","TOMATO",1]]},{"farmer":["PLANT","WHEAT"],"hands":[["COLLECT_FERTILIZER"],["NORTH"],["WATER"],["HARVEST"],["DROP"],["WATER"],["WATER"],["WEST"],["COLLECT_FERTILIZER"],["FERTILIZE"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["NORTH"],["EAST"],["SOUTH"],["PLANT","TOMATO"],["EAST"],["EAST"],["EAST"],["WATER"],["NORTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["WEST"],["WATER"],["SOUTH"],["SOUTH"],["EAST"],["WATER"],["WATER"],["HARVEST"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["WATER"],"hands":[["FERTILIZE"],["NORTH"],["WATER"],["NORTH"],["EAST"],["EAST"],["WEST"],["PLANT","WHEAT"],["EAST"],["WATER"]],"market":[["SELL","EGG",6]]},{"farmer":["PASS"],"hands":[["WATER"],["WATER"],["SOUTH"],["WATER"],["PASS"],["NORTH"],["WEST"],["WATER"],["WATER"],["EAST"]],"market":[]},{"farmer":["NORTH"],"hands":[],"market":[["SELL","FERTILIZER",12],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["HARVEST"],"hands":[["HARVEST"],["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["PICKUP","WHEAT",3],["NORTH"],["EAST"],["SOUTH"],["SOUTH"],["NORTH"]],"market":[["SELL","WHEAT",12],["HIRE"],["BUY_SEED","TOMATO",1],["BUY_SEED","STRAWBERRY",1],["BUY_SEED","TOMATO",1],["BUY_SEED","STRAWBERRY",1],["BUY_SEED","STRAWBERRY",1],["HIRE"],["HIRE"]]},{"farmer":["SOUTH"],"hands":[["DROP"],["FEED"],["FEED"],["WEST"],["NORTH"],["WATER"],["WEST"],["SOUTH"],["WEST"],["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["WEST"]],"market":[["SELL","MILK",3]]},{"farmer":["DROP"],"hands":[["PICKUP","WHEAT",4],["CARE"],["CARE"],["WEST"],["HARVEST"],["EAST"],["WATER"],["SOUTH"],["WATER"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"]],"market":[["SELL","WOOL",4]]},{"farmer":["PICKUP","WHEAT",3],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FEED"],["SOUTH"],["WATER"],["HARVEST"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["FEED"],["WEST"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["NORTH"],["WEST"],["CARE"],["SOUTH"],["EAST"],["PLANT","TOMATO"],["SOUTH"],["WEST"],["WEST"],["CARE"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["CARE"],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["HARVEST"],["PASS"],["DROP"],["WATER"],["WATER"],["WATER"],["HARVEST"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"]],"market":[["SELL","MILK",3]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FEED"],["EAST"],["WEST"],["WEST"],["PICKUP","WHEAT",3],["EAST"],["SOUTH"],["HARVEST"],["SOUTH"],["NORTH"],["FEED"],["SOUTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["CARE"],["FEED"],["FEED"],["PASS"],["NORTH"],["WATER"],["SOUTH"],["PLANT","STRAWBERRY"],["EAST"],["NORTH"],["CARE"],["FERTILIZE"]],"market":[]},{"farmer":["NORTH"],"hands":[["COLLECT_FERTILIZER"],["CARE"],["CARE"],["PASS"],["WEST"],["NORTH"],["WATER"],["WATER"],["EAST"],["FEED"],["COLLECT_FERTILIZER"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["HARVEST"],["PASS"],["WEST"],["WATER"],["HARVEST"],["WEST"],["SOUTH"],["CARE"],["NORTH"],["SOUTH"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["NORTH"],["NORTH"],["WEST"],["NORTH"],["WATER"],["NORTH"],["PLANT","STRAWBERRY"],["WEST"],["DROP"],["COLLECT_FERTILIZER"],["WATER"],["WATER"]],"market":[["SELL","MILK",6],["BUY_SEED","TOMATO",1]]},{"farmer":["WATER"],"hands":[["FEED"],["WATER"],["NORTH"],["WEST"],["NORTH"],["WATER"],["WATER"],["WATER"],["PICKUP","WHEAT",2],["WEST"],["NORTH"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["CARE"],["EAST"],["NORTH"],["WATER"],["NORTH"],["NORTH"],["NORTH"],["WEST"],["NORTH"],["HARVEST"],["EAST"],["WATER"]],"market":[]},{"farmer":["HARVEST"],"hands":[["COLLECT_FERTILIZER"],["WATER"],["WEST"],["WEST"],["FEED"],["WATER"],["NORTH"],["NORTH"],["WEST"],["FEED"],["WATER"],["HARVEST"]],"market":[]},{"farmer":["FEED"],"hands":[["WEST"],["EAST"],["NORTH"],["WATER"],["CARE"],["NORTH"],["EAST"],["WATER"],["NORTH"],["CARE"],["EAST"],["PLANT","STRAWBERRY"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","TOMATO",1]]},{"farmer":["CARE"],"hands":[["FERTILIZE"],["SOUTH"],["FERTILIZE"],["HARVEST"],["COLLECT_FERTILIZER"],["WATER"],["NORTH"],["HARVEST"],["WATER"],["COLLECT_FERTILIZER"],["WATER"],["WATER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["WATER"],["WATER"],["PLANT","TOMATO"],["NORTH"],["WEST"],["DROP"],["PLANT","TOMATO"],["SOUTH"],["NORTH"],["SOUTH"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","TOMATO",1]]},{"farmer":["SOUTH"],"hands":[["WEST"],["WEST"],["NORTH"],["WATER"],["FERTILIZE"],["WATER"],["SOUTH"],["WATER"],["HARVEST"],["FERTILIZE"],["WATER"],["WATER"]],"market":[]},{"farmer":["EAST"],"hands":[["WATER"],["WATER"],["HARVEST"],["EAST"],["WEST"],["SOUTH"],["WATER"],["SOUTH"],["PLANT","WHEAT"],["WATER"],["EAST"],["HARVEST"]],"market":[]},{"farmer":["SOUTH"],"hands":[["WEST"],["WEST"],["WATER"],["HARVEST"],["HARVEST"],["WATER"],["SOUTH"],["WATER"],["WATER"],["PASS"],["SOUTH"],["PLANT","TOMATO"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["WATER"],["HARVEST"],["NORTH"],["PLANT","WHEAT"],["PASS"],["SOUTH"],["WATER"],["WEST"],["SOUTH"],["PASS"],["WATER"],["WATER"]],"market":[]},{"farmer":["DROP"],"hands":[["WEST"],["SOUTH"],["WATER"],["WATER"],["SOUTH"],["SOUTH"],["SOUTH"],["PASS"],["HARVEST"],["PASS"],["SOUTH"],["PASS"]],"market":[["SELL","MILK",3],["SELL","EGG",6]]},{"farmer":["PASS"],"hands":[["SOUTH"],["WEST"],["SOUTH"],["PASS"],["SOUTH"],["PASS"],["WATER"],["WATER"],["CARE"],["SOUTH"],["SOUTH"],["PASS"]],"market":[["SELL","WHEAT",6],["SELL","EGG",4]]},{"farmer":["PICKUP","WHEAT",4],"hands":[],"market":[["SELL","FERTILIZER",12],["HIRE"],["HIRE"],["HIRE"],["BUY_SEED","STRAWBERRY",2],["BUY_SEED","STRAWBERRY",2],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",4],["HARVEST"],["PICKUP","WHEAT",4],["PICKUP","WHEAT",5],["EAST"],["WEST"],["SOUTH"]],"market":[["SELL","WHEAT",10],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["FEED"],["DROP"],["WEST"],["FEED"],["WATER"],["COLLECT_FERTILIZER"],["SOUTH"],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",4]],"market":[]},{"farmer":["CARE"],"hands":[["CARE"],["PICKUP","WHEAT",3],["WEST"],["CARE"],["EAST"],["WEST"],["WEST"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["FEED"],["FEED"],["NORTH"],["WATER"],["COLLECT_FERTILIZER"],["WATER"],["COLLECT_FERTILIZER"],["FEED"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["CARE"],["CARE"],["FEED"],["EAST"],["WEST"],["WEST"],["NORTH"],["CARE"]],"market":[]},{"farmer":["FEED"],"hands":[["HARVEST"],["COLLECT_FERTILIZER"],["HARVEST"],["CARE"],["WATER"],["FERTILIZE"],["WATER"],["COLLECT_FERTILIZER"],["NORTH"]],"market":[]},{"farmer":["CARE"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["WEST"],["NORTH"],["PASS"],["WATER"],["WEST"],["NORTH"],["FEED"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["EAST"],["NORTH"],["FEED"],["FEED"],["PASS"],["WEST"],["WATER"],["WATER"],["CARE"]],"market":[]},{"farmer":["HARVEST"],"hands":[["FEED"],["NORTH"],["CARE"],["CARE"],["PASS"],["FERTILIZE"],["SOUTH"],["HARVEST"],["HARVEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["CARE"],["NORTH"],["HARVEST"],["WEST"],["PASS"],["WATER"],["WATER"],["PLANT","STRAWBERRY"],["COLLECT_FERTILIZER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FERTILIZE"],"hands":[["COLLECT_FERTILIZER"],["FERTILIZE"],["SOUTH"],["WEST"],["NORTH"],["SOUTH"],["SOUTH"],["WATER"],["NORTH"]],"market":[]},{"farmer":["WATER"],"hands":[["HARVEST"],["WATER"],["WATER"],["FEED"],["WATER"],["WATER"],["WATER"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["WEST"],"hands":[["WEST"],["NORTH"],["HARVEST"],["CARE"],["NORTH"],["EAST"],["EAST"],["FEED"],["WATER"]],"market":[["SELL","MILK",6]]},{"farmer":["FERTILIZE"],"hands":[["SOUTH"],["FEED"],["PLANT","STRAWBERRY"],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["WATER"],["CARE"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["DROP"],["CARE"],["WATER"],["WEST"],["NORTH"],["HARVEST"],["WEST"],["HARVEST"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["EAST"],["FEED"],["WATER"],["PLANT","TOMATO"],["WEST"],["COLLECT_FERTILIZER"],["HARVEST"]],"market":[["SELL","FERTILIZER",3]]},{"farmer":["WATER"],"hands":[["NORTH"],["WEST"],["EAST"],["CARE"],["NORTH"],["WATER"],["WATER"],["SOUTH"],["WEST"]],"market":[]},{"farmer":["HARVEST"],"hands":[["EAST"],["HARVEST"],["WATER"],["COLLECT_FERTILIZER"],["WATER"],["SOUTH"],["WEST"],["EAST"],["HARVEST"]],"market":[]},{"farmer":["PLANT","STRAWBERRY"],"hands":[["WATER"],["FEED"],["NORTH"],["WEST"],["EAST"],["WATER"],["WATER"],["WATER"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["NORTH"],["CARE"],["DROP"],["HARVEST"],["WATER"],["WEST"],["HARVEST"],["EAST"],["WATER"]],"market":[]},{"farmer":["SOUTH"],"hands":[["WATER"],["COLLECT_FERTILIZER"],["PASS"],["NORTH"],["SOUTH"],["WATER"],["PLANT","WHEAT"],["EAST"],["WEST"]],"market":[["SELL","EGG",8]]},{"farmer":["WATER"],"hands":[["NORTH"],["WEST"],["PASS"],["EAST"],["WATER"],["SOUTH"],["WATER"],["WATER"],["WATER"]],"market":[["SELL","WHEAT",13],["SELL","EGG",6]]},{"farmer":["PASS"],"hands":[["WATER"],["HARVEST"],["PASS"],["PASS"],["SOUTH"],["WATER"],["PASS"],["SOUTH"],["SOUTH"]],"market":[["SELL","EGG",6]]},{"farmer":["HARVEST"],"hands":[],"market":[["SELL","MILK",9],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["DROP"],"hands":[["HARVEST"],["PICKUP","WHEAT",4],["PICKUP","WHEAT",3],["PICKUP","WHEAT",4],["EAST"],["SOUTH"],["SOUTH"],["NORTH"],["NORTH"]],"market":[["SELL","MILK",3],["SELL","FERTILIZER",8],["SELL","FERTILIZER",4],["SELL","FERTILIZER",1]]},{"farmer":["PICKUP","WHEAT",4],"hands":[["DROP"],["FEED"],["WEST"],["WEST"],["WATER"],["WATER"],["SOUTH"],["NORTH"],["COLLECT_FERTILIZER"]],"market":[["SELL","MILK",6]]},{"farmer":["NORTH"],"hands":[["PICKUP","WHEAT",3],["CARE"],["WEST"],["FEED"],["EAST"],["WEST"],["WEST"],["HARVEST"],["NORTH"]],"market":[]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FEED"],["CARE"],["WATER"],["WATER"],["WATER"],["SOUTH"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["CARE"],"hands":[["FEED"],["NORTH"],["CARE"],["COLLECT_FERTILIZER"],["EAST"],["WEST"],["SOUTH"],["SOUTH"],["WEST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["CARE"],["FEED"],["COLLECT_FERTILIZER"],["WEST"],["WATER"],["NORTH"],["WATER"],["DROP"],["COLLECT_FERTILIZER"]],"market":[["SELL","MILK",3]]},{"farmer":["NORTH"],"hands":[["NORTH"],["CARE"],["HARVEST"],["FEED"],["EAST"],["COLLECT_FERTILIZER"],["SOUTH"],["WEST"],["WEST"]],"market":[]},{"farmer":["FEED"],"hands":[["FEED"],["COLLECT_FERTILIZER"],["WEST"],["CARE"],["WATER"],["WEST"],["WATER"],["NORTH"],["WATER"]],"market":[]},{"farmer":["CARE"],"hands":[["CARE"],["NORTH"],["FEED"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"],["WEST"],["WATER"],["HARVEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["HARVEST"],["EAST"],["CARE"],["WEST"],["WATER"],["HARVEST"],["WATER"],["WEST"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["EAST"],["EAST"],["HARVEST"],["FERTILIZE"],["NORTH"],["PLANT","WHEAT"],["NORTH"],["WATER"],["WATER"]],"market":[["SELL","WHEAT",5]]},{"farmer":["FEED"],"hands":[["FEED"],["EAST"],["NORTH"],["WATER"],["WATER"],["WATER"],["WATER"],["HARVEST"],["NORTH"]],"market":[]},{"farmer":["CARE"],"hands":[["COLLECT_FERTILIZER"],["WATER"],["NORTH"],["NORTH"],["NORTH"],["WEST"],["WEST"],["PLANT","WHEAT"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["CARE"],["NORTH"],["WATER"],["WATER"],["WATER"],["WATER"],["WATER"],["NORTH"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["WEST"],"hands":[["HARVEST"],["WATER"],["NORTH"],["NORTH"],["NORTH"],["HARVEST"],["WEST"],["HARVEST"],["WEST"]],"market":[]},{"farmer":["WATER"],"hands":[["WEST"],["NORTH"],["CARE"],["HARVEST"],["WATER"],["PLANT","WHEAT"],["WATER"],["EAST"],["FEED"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["SOUTH"],["WATER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WEST"],["WATER"],["WEST"],["EAST"],["CARE"]],"market":[["SELL","MELON",6]]},{"farmer":["WATER"],"hands":[["DROP"],["WEST"],["FEED"],["WEST"],["WATER"],["NORTH"],["WATER"],["EAST"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",2],["WATER"],["WEST"],["WATER"],["WEST"],["WATER"],["NORTH"],["FEED"],["WEST"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["HARVEST"],"hands":[["NORTH"],["NORTH"],["PASS"],["NORTH"],["WATER"],["NORTH"],["WATER"],["CARE"],["WATER"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["WATER"],["CARE"],["FERTILIZE"],["SOUTH"],["WATER"],["EAST"],["HARVEST"],["SOUTH"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["FERTILIZE"],"hands":[["NORTH"],["WEST"],["EAST"],["WATER"],["EAST"],["SOUTH"],["EAST"],["NORTH"],["FEED"]],"market":[["SELL","EGG",6]]},{"farmer":["WATER"],"hands":[["WATER"],["WATER"],["PASS"],["HARVEST"],["WATER"],["PASS"],["WATER"],["PASS"],["PASS"]],"market":[["SELL","EGG",3]]},{"farmer":["PICKUP","WHEAT",4],"hands":[],"market":[["SELL","MILK",6],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["PICKUP","WHEAT",4],["HARVEST"],["PICKUP","FERTILIZER",4],["PICKUP","WHEAT",4],["PICKUP","FERTILIZER",4],["SOUTH"],["PICKUP","FERTILIZER",4],["WEST"],["PASS"]],"market":[["SELL","MILK",3],["SELL","FERTILIZER",4],["HIRE"],["HIRE"]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["CARE"],["DROP"],["EAST"],["FEED"],["EAST"],["WATER"],["EAST"],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",4],["COLLECT_FERTILIZER"],["WEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["FEED"],["CARE"],["EAST"],["CARE"],["WATER"],["SOUTH"],["EAST"],["WEST"],["NORTH"],["WEST"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["PICKUP","WHEAT",3],["NORTH"],["WEST"],["NORTH"],["WATER"],["NORTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["NORTH"],["HARVEST"]],"market":[]},{"farmer":["CARE"],"hands":[["NORTH"],["FEED"],["WATER"],["SOUTH"],["COLLECT_FERTILIZER"],["WEST"],["EAST"],["WEST"],["FEED"],["FERTILIZE"],["WEST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["CARE"],["COLLECT_FERTILIZER"],["NORTH"],["FEED"],["NORTH"],["WATER"],["WATER"],["WATER"],["NORTH"],["WATER"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["NORTH"],"hands":[["HARVEST"],["WEST"],["FERTILIZE"],["CARE"],["FERTILIZE"],["WEST"],["EAST"],["HARVEST"],["COLLECT_FERTILIZER"],["WEST"],["HARVEST"]],"market":[]},{"farmer":["WATER"],"hands":[["EAST"],["WEST"],["WATER"],["WEST"],["WATER"],["WATER"],["FERTILIZE"],["PLANT","STRAWBERRY"],["FEED"],["WEST"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["FEED"],["FEED"],["EAST"],["NORTH"],["NORTH"],["HARVEST"],["WATER"],["WATER"],["CARE"],["WATER"],["WATER"]],"market":[]},{"farmer":["HARVEST"],"hands":[["CARE"],["CARE"],["FERTILIZE"],["NORTH"],["WATER"],["PLANT","WHEAT"],["NORTH"],["NORTH"],["NORTH"],["HARVEST"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["HARVEST"],["NORTH"],["WATER"],["NORTH"],["EAST"],["WATER"],["FERTILIZE"],["PLANT","WHEAT"],["FERTILIZE"],["NORTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["EAST"],"hands":[["WEST"],["EAST"],["NORTH"],["FEED"],["FERTILIZE"],["SOUTH"],["WATER"],["WATER"],["WATER"],["FEED"],["WEST"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["WEST"],["NORTH"],["FERTILIZE"],["CARE"],["WATER"],["SOUTH"],["NORTH"],["NORTH"],["WEST"],["CARE"],["WATER"]],"market":[["SELL","STRAWBERRY",6]]},{"farmer":["WATER"],"hands":[["SOUTH"],["NORTH"],["WATER"],["COLLECT_FERTILIZER"],["EAST"],["WATER"],["FERTILIZE"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["SOUTH"]],"market":[]},{"farmer":["WEST"],"hands":[["DROP"],["EAST"],["WEST"],["NORTH"],["FERTILIZE"],["WEST"],["WATER"],["WEST"],["FEED"],["HARVEST"],["WATER"]],"market":[]},{"farmer":["FEED"],"hands":[["WEST"],["EAST"],["FERTILIZE"],["HARVEST"],["WATER"],["WATER"],["NORTH"],["HARVEST"],["CARE"],["WEST"],["EAST"]],"market":[]},{"farmer":["CARE"],"hands":[["WEST"],["HARVEST"],["WATER"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"],["FERTILIZE"],["NORTH"],["COLLECT_FERTILIZER"],["WATER"],["WATER"]],"market":[["SELL","STRAWBERRY",6]]},{"farmer":["WEST"],"hands":[["HARVEST"],["SOUTH"],["PASS"],["NORTH"],["FERTILIZE"],["WATER"],["WATER"],["NORTH"],["NORTH"],["NORTH"],["SOUTH"]],"market":[]},{"farmer":["HARVEST"],"hands":[["PASS"],["SOUTH"],["WEST"],["HARVEST"],["WATER"],["HARVEST"],["NORTH"],["HARVEST"],["WEST"],["EAST"],["WATER"]],"market":[]},{"farmer":["SOUTH"],"hands":[["PASS"],["DROP"],["NORTH"],["WEST"],["EAST"],["PLANT","WHEAT"],["WATER"],["WATER"],["SOUTH"],["WATER"],["EAST"]],"market":[["SELL","EGG",8]]},{"farmer":["SOUTH"],"hands":[["PASS"],["PASS"],["NORTH"],["FERTILIZE"],["FERTILIZE"],["WATER"],["WEST"],["EAST"],["FEED"],["SOUTH"],["WATER"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["FERTILIZE"],"hands":[["PASS"],["PASS"],["WATER"],["EAST"],["SOUTH"],["NORTH"],["WEST"],["EAST"],["CARE"],["SOUTH"],["EAST"]],"market":[["SELL","WHEAT",6]]},{"farmer":["SOUTH"],"hands":[["PASS"],["PASS"],["EAST"],["EAST"],["SOUTH"],["WATER"],["WATER"],["EAST"],["PASS"],["PASS"],["WATER"]],"market":[["SELL","EGG",6]]},{"farmer":["HARVEST"],"hands":[],"market":[["SELL","MILK",6],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["PLACE","MILK",3],"hands":[["EAST"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["PICKUP","WHEAT",4],["EAST"],["WEST"],["EAST"],["NORTH"],["EAST"]],"market":[["SELL","MILK",3],["SELL","FERTILIZER",8],["HIRE"],["HIRE"],["BUY_SEED","TOMATO",1]]},{"farmer":["PICKUP","WHEAT",4],"hands":[["WATER"],["FEED"],["WEST"],["WEST"],["EAST"],["COLLECT_FERTILIZER"],["EAST"],["NORTH"],["EAST"],["HARVEST"],["NORTH"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["NORTH"],"hands":[["HARVEST"],["CARE"],["WEST"],["FEED"],["WATER"],["WEST"],["EAST"],["HARVEST"],["EAST"],["DROP"],["NORTH"]],"market":[["SELL","MILK",3]]},{"farmer":["FEED"],"hands":[["WEST"],["COLLECT_FERTILIZER"],["FEED"],["CARE"],["HARVEST"],["COLLECT_FERTILIZER"],["NORTH"],["SOUTH"],["WATER"],["COLLECT_FERTILIZER"],["NORTH"]],"market":[]},{"farmer":["CARE"],"hands":[["DROP"],["SOUTH"],["CARE"],["COLLECT_FERTILIZER"],["WEST"],["WEST"],["HARVEST"],["SOUTH"],["EAST"],["NORTH"],["HARVEST"]],"market":[["SELL","MELON",6]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["PICKUP","WHEAT",3],["FERTILIZE"],["HARVEST"],["WEST"],["WEST"],["FERTILIZE"],["WEST"],["DROP"],["HARVEST"],["COLLECT_FERTILIZER"],["NORTH"]],"market":[["SELL","MILK",3]]},{"farmer":["NORTH"],"hands":[["NORTH"],["WATER"],["WEST"],["FEED"],["DROP"],["WATER"],["WEST"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"],["HARVEST"]],"market":[["SELL","MELON",6]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FEED"],["SOUTH"],["FEED"],["CARE"],["PICKUP","WHEAT",2],["WEST"],["WEST"],["NORTH"],["HARVEST"],["COLLECT_FERTILIZER"],["SOUTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["CARE"],["WATER"],["CARE"],["COLLECT_FERTILIZER"],["EAST"],["FERTILIZE"],["DROP"],["WEST"],["WEST"],["EAST"],["SOUTH"]],"market":[["SELL","MELON",6]]},{"farmer":["NORTH"],"hands":[["NORTH"],["SOUTH"],["HARVEST"],["NORTH"],["PLANT","WHEAT"],["WATER"],["PICKUP","WHEAT",2],["WATER"],["HARVEST"],["HARVEST"],["SOUTH"]],"market":[["SELL","STRAWBERRY",6]]},{"farmer":["FEED"],"hands":[["FEED"],["WATER"],["NORTH"],["FERTILIZE"],["WATER"],["NORTH"],["NORTH"],["HARVEST"],["WEST"],["NORTH"],["SOUTH"]],"market":[]},{"farmer":["CARE"],"hands":[["CARE"],["SOUTH"],["EAST"],["WATER"],["EAST"],["WATER"],["HARVEST"],["PLANT","WHEAT"],["HARVEST"],["WATER"],["DROP"]],"market":[["SELL","STRAWBERRY",6]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["HARVEST"],["WATER"],["SOUTH"],["NORTH"],["PLANT","WHEAT"],["NORTH"],["EAST"],["WATER"],["WEST"],["EAST"],["PICKUP","WHEAT",2]],"market":[["SELL","STRAWBERRY",4],["BUY_SEED","TOMATO",1]]},{"farmer":["WEST"],"hands":[["WEST"],["WEST"],["SOUTH"],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["FEED"],["NORTH"],["SOUTH"],["HARVEST"],["WEST"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["NORTH"],["WATER"],["WATER"],["HARVEST"],["EAST"],["NORTH"],["CARE"],["WATER"],["WEST"],["NORTH"],["WEST"]],"market":[]},{"farmer":["WATER"],"hands":[["WEST"],["WEST"],["SOUTH"],["WEST"],["PLANT","WHEAT"],["WATER"],["COLLECT_FERTILIZER"],["NORTH"],["DROP"],["FERTILIZE"],["WEST"]],"market":[["SELL","STRAWBERRY",8]]},{"farmer":["WEST"],"hands":[["HARVEST"],["WATER"],["WATER"],["COLLECT_FERTILIZER"],["WATER"],["NORTH"],["HARVEST"],["WEST"],["WEST"],["WATER"],["WEST"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["WEST"],["HARVEST"],["NORTH"],["HARVEST"],["EAST"],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",2],["EAST"],["SOUTH"]],"market":[]},{"farmer":["WATER"],"hands":[["EAST"],["WATER"],["WEST"],["WEST"],["NORTH"],["NORTH"],["NORTH"],["WEST"],["FEED"],["HARVEST"],["SOUTH"]],"market":[]},{"farmer":["WEST"],"hands":[["WATER"],["NORTH"],["WATER"],["FERTILIZE"],["HARVEST"],["WATER"],["HARVEST"],["FERTILIZE"],["CARE"],["EAST"],["WATER"]],"market":[]},{"farmer":["HARVEST"],"hands":[["WEST"],["WATER"],["WEST"],["EAST"],["EAST"],["SOUTH"],["SOUTH"],["WATER"],["EAST"],["HARVEST"],["WEST"]],"market":[["SELL","WOOL",2]]},{"farmer":["SOUTH"],"hands":[["WEST"],["EAST"],["WATER"],["SOUTH"],["HARVEST"],["SOUTH"],["SOUTH"],["EAST"],["DROP"],["SOUTH"],["WATER"]],"market":[["SELL","EGG",6]]},{"farmer":["EAST"],"hands":[["CARE"],["WATER"],["SOUTH"],["FERTILIZE"],["NORTH"],["PASS"],["PASS"],["PASS"],["PASS"],["HARVEST"],["PASS"]],"market":[]},{"farmer":["PICKUP","WHEAT",4],"hands":[],"market":[["SELL","STRAWBERRY",12],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",3],["HARVEST"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",4],["EAST"],["SOUTH"],["SOUTH"],["WEST"],["NORTH"]],"market":[["SELL","MILK",4],["SELL","FERTILIZER",8],["HIRE"],["BUY_PRODUCT","WHEAT",6]]},{"farmer":["CARE"],"hands":[["FEED"],["DROP"],["WEST"],["FEED"],["EAST"],["HARVEST"],["SOUTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["FEED"],"hands":[["CARE"],["PICKUP","WHEAT",3],["WEST"],["CARE"],["EAST"],["WATER"],["SOUTH"],["WEST"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["HARVEST"],"hands":[["COLLECT_FERTILIZER"],["FEED"],["FEED"],["NORTH"],["EAST"],["WEST"],["WEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["CARE"],["CARE"],["FEED"],["WATER"],["WEST"],["HARVEST"],["WEST"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["FEED"],"hands":[["FEED"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["CARE"],["NORTH"],["WATER"],["WATER"],["WATER"],["WATER"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["CARE"],"hands":[["CARE"],["WEST"],["HARVEST"],["NORTH"],["WATER"],["NORTH"],["WEST"],["NORTH"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["EAST"],["WEST"],["WEST"],["FEED"],["NORTH"],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["WATER"],["NORTH"]],"market":[]},{"farmer":["WATER"],"hands":[["FEED"],["FEED"],["WEST"],["CARE"],["WATER"],["WEST"],["WEST"],["NORTH"],["EAST"],["COLLECT_FERTILIZER"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["HARVEST"],"hands":[["CARE"],["CARE"],["WATER"],["WEST"],["NORTH"],["WEST"],["WATER"],["COLLECT_FERTILIZER"],["WATER"],["HARVEST"]],"market":[]},{"farmer":["PLANT","WHEAT"],"hands":[["COLLECT_FERTILIZER"],["HARVEST"],["HARVEST"],["WATER"],["WATER"],["WATER"],["WEST"],["NORTH"],["SOUTH"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["EAST"],["SOUTH"],["PLANT","WHEAT"],["HARVEST"],["NORTH"],["HARVEST"],["WATER"],["HARVEST"],["WATER"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["WATER"],["SOUTH"],["WATER"],["PLANT","WHEAT"],["WATER"],["PLANT","WHEAT"],["WEST"],["WEST"],["HARVEST"],["WEST"]],"market":[["SELL","MILK",2],["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["EAST"],["WATER"],["SOUTH"],["WATER"],["WEST"],["WATER"],["WATER"],["FERTILIZE"],["PLANT","TOMATO"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["WATER"],["SOUTH"],["WATER"],["NORTH"],["WATER"],["NORTH"],["SOUTH"],["WATER"],["WATER"],["WEST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["SOUTH"],["SOUTH"],["FEED"],["WEST"],["WATER"],["WATER"],["SOUTH"],["SOUTH"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["WATER"],["FERTILIZE"],["FERTILIZE"],["CARE"],["WATER"],["NORTH"],["HARVEST"],["HARVEST"],["WATER"],["WEST"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["FEED"],"hands":[["NORTH"],["WATER"],["WATER"],["COLLECT_FERTILIZER"],["HARVEST"],["EAST"],["PLANT","TOMATO"],["EAST"],["SOUTH"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["WATER"],["EAST"],["HARVEST"],["EAST"],["SOUTH"],["NORTH"],["WATER"],["EAST"],["HARVEST"],["SOUTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["HARVEST"],["WATER"],["WEST"],["WATER"],["WATER"],["FEED"],["EAST"],["EAST"],["WEST"],["NORTH"]],"market":[]},{"farmer":["HARVEST"],"hands":[["SOUTH"],["EAST"],["WATER"],["NORTH"],["SOUTH"],["CARE"],["WATER"],["SOUTH"],["SOUTH"],["EAST"]],"market":[["SELL","MILK",2]]},{"farmer":["NORTH"],"hands":[["SOUTH"],["WATER"],["NORTH"],["FEED"],["WATER"],["WEST"],["NORTH"],["FERTILIZE"],["DROP"],["EAST"]],"market":[["SELL","EGG",10],["SELL","EGG",8]]},{"farmer":["EAST"],"hands":[["SOUTH"],["NORTH"],["WATER"],["CARE"],["SOUTH"],["SOUTH"],["PASS"],["EAST"],["PASS"],["PASS"]],"market":[["SELL","MELON",6],["SELL","FERTILIZER",2]]},{"farmer":["PICKUP","WHEAT",3],"hands":[],"market":[["SELL","STRAWBERRY",6],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["EAST"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["NORTH"],["SOUTH"],["PICKUP","FERTILIZER",3],["NORTH"],["NORTH"]],"market":[["SELL","FERTILIZER",8],["SELL","FERTILIZER",4],["HIRE"],["HIRE"],["BUY_SEED","TOMATO",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["EAST"],["FEED"],["WEST"],["WEST"],["NORTH"],["HARVEST"],["SOUTH"],["WEST"],["NORTH"],["PICKUP","WHEAT",3],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["NORTH"],"hands":[["EAST"],["CARE"],["WEST"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"],["SOUTH"],["WATER"],["NORTH"],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",3]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["EAST"],["COLLECT_FERTILIZER"],["FEED"],["WEST"],["HARVEST"],["WEST"],["WEST"],["WEST"],["NORTH"],["EAST"],["FEED"]],"market":[]},{"farmer":["HARVEST"],"hands":[["HARVEST"],["WEST"],["CARE"],["COLLECT_FERTILIZER"],["SOUTH"],["WATER"],["FERTILIZE"],["WEST"],["HARVEST"],["FERTILIZE"],["CARE"]],"market":[["SELL","STRAWBERRY",6]]},{"farmer":["NORTH"],"hands":[["NORTH"],["WEST"],["COLLECT_FERTILIZER"],["NORTH"],["EAST"],["SOUTH"],["WATER"],["WATER"],["EAST"],["WATER"],["NORTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["HARVEST"],["FEED"],["HARVEST"],["NORTH"],["HARVEST"],["WATER"],["HARVEST"],["HARVEST"],["EAST"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["FEED"],"hands":[["WEST"],["CARE"],["WEST"],["COLLECT_FERTILIZER"],["SOUTH"],["WEST"],["SOUTH"],["PLANT","WHEAT"],["WATER"],["FEED"],["FEED"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["HARVEST"],["COLLECT_FERTILIZER"],["PASS"],["NORTH"],["SOUTH"],["WATER"],["HARVEST"],["WATER"],["HARVEST"],["CARE"],["CARE"]],"market":[["SELL","MILK",2]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WEST"],["SOUTH"],["HARVEST"],["FEED"],["WEST"],["HARVEST"],["FERTILIZE"],["WEST"],["EAST"],["COLLECT_FERTILIZER"],["EAST"]],"market":[]},{"farmer":["WEST"],"hands":[["HARVEST"],["WEST"],["NORTH"],["CARE"],["DROP"],["PLANT","TOMATO"],["WATER"],["WATER"],["HARVEST"],["EAST"],["FEED"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WEST"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",2],["WATER"],["WEST"],["NORTH"],["SOUTH"],["SOUTH"],["CARE"]],"market":[]},{"farmer":["WEST"],"hands":[["SOUTH"],["FERTILIZE"],["NORTH"],["NORTH"],["NORTH"],["WEST"],["SOUTH"],["WATER"],["HARVEST"],["FERTILIZE"],["COLLECT_FERTILIZER"]],"market":[["SELL","STRAWBERRY",6]]},{"farmer":["WATER"],"hands":[["WEST"],["WATER"],["HARVEST"],["WEST"],["FEED"],["WATER"],["FERTILIZE"],["NORTH"],["SOUTH"],["WATER"],["HARVEST"]],"market":[]},{"farmer":["WEST"],"hands":[["DROP"],["SOUTH"],["WEST"],["HARVEST"],["CARE"],["HARVEST"],["WATER"],["HARVEST"],["HARVEST"],["EAST"],["NORTH"]],"market":[["SELL","STRAWBERRY",8]]},{"farmer":["DIG"],"hands":[["HARVEST"],["WATER"],["COLLECT_FERTILIZER"],["SOUTH"],["HARVEST"],["SOUTH"],["WEST"],["DIG"],["SOUTH"],["WATER"],["NORTH"]],"market":[["BUY_SEED","TOMATO",1]]},{"farmer":["PLANT","TOMATO"],"hands":[["DROP"],["SOUTH"],["HARVEST"],["WATER"],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["PASS"],["WEST"],["NORTH"],["EAST"]],"market":[["SELL","MILK",2],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["PICKUP","WHEAT",2],["WATER"],["EAST"],["EAST"],["SOUTH"],["EAST"],["HARVEST"],["PLANT","WHEAT"],["SOUTH"],["NORTH"],["FERTILIZE"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["FEED"],["EAST"],["EAST"],["EAST"],["DROP"],["WATER"],["WEST"],["WATER"],["WEST"],["EAST"],["WATER"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["CARE"],["EAST"],["FERTILIZE"],["HARVEST"],["EAST"],["EAST"],["WATER"],["SOUTH"],["WEST"],["HARVEST"],["EAST"]],"market":[]},{"farmer":["WATER"],"hands":[["WEST"],["FERTILIZE"],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"],["WEST"],["EAST"],["DROP"],["NORTH"],["SOUTH"]],"market":[["SELL","STRAWBERRY",6],["SELL","MILK",2]]},{"farmer":["SOUTH"],"hands":[["HARVEST"],["NORTH"],["EAST"],["EAST"],["HARVEST"],["NORTH"],["WATER"],["FEED"],["WEST"],["HARVEST"],["HARVEST"]],"market":[["SELL","TOMATO",6],["SELL","EGG",6]]},{"farmer":["SOUTH"],"hands":[["DROP"],["NORTH"],["WATER"],["PASS"],["EAST"],["PASS"],["PASS"],["CARE"],["PASS"],["NORTH"],["SOUTH"]],"market":[["SELL","WHEAT",13],["SELL","EGG",2]]},{"farmer":["PICKUP","WHEAT",3],"hands":[],"market":[["SELL","MILK",6],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",3],["HARVEST"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["PICKUP","FERTILIZER",4],["SOUTH"],["PICKUP","FERTILIZER",4],["WEST"],["PICKUP","FERTILIZER",2]],"market":[["SELL","WOOL",2],["HIRE"],["HIRE"],["BUY_PRODUCT","WHEAT",6],["BUY_PRODUCT","WHEAT",6]]},{"farmer":["FEED"],"hands":[["FEED"],["DROP"],["WEST"],["FEED"],["EAST"],["HARVEST"],["EAST"],["WEST"],["NORTH"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",2]],"market":[]},{"farmer":["CARE"],"hands":[["CARE"],["PICKUP","WHEAT",3],["WEST"],["CARE"],["WATER"],["SOUTH"],["EAST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["FEED"],["FEED"],["COLLECT_FERTILIZER"],["HARVEST"],["WATER"],["NORTH"],["WEST"],["NORTH"],["FEED"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["CARE"],["CARE"],["NORTH"],["PLANT","WHEAT"],["HARVEST"],["WATER"],["WATER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FEED"]],"market":[]},{"farmer":["FEED"],"hands":[["FEED"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"],["SOUTH"],["EAST"],["WEST"],["NORTH"],["NORTH"],["CARE"]],"market":[]},{"farmer":["CARE"],"hands":[["CARE"],["SOUTH"],["HARVEST"],["FEED"],["NORTH"],["WATER"],["WATER"],["FERTILIZE"],["FERTILIZE"],["WEST"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["NORTH"],"hands":[["HARVEST"],["FERTILIZE"],["SOUTH"],["CARE"],["COLLECT_FERTILIZER"],["HARVEST"],["EAST"],["WATER"],["WATER"],["WATER"],["HARVEST"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["NORTH"],["WATER"],["FERTILIZE"],["COLLECT_FERTILIZER"],["EAST"],["SOUTH"],["FERTILIZE"],["NORTH"],["NORTH"],["NORTH"],["WEST"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["WATER"],"hands":[["FEED"],["WEST"],["WATER"],["NORTH"],["FERTILIZE"],["WATER"],["WATER"],["NORTH"],["FERTILIZE"],["FEED"],["FERTILIZE"]],"market":[]},{"farmer":["NORTH"],"hands":[["CARE"],["WEST"],["WEST"],["NORTH"],["WATER"],["WEST"],["NORTH"],["HARVEST"],["WATER"],["CARE"],["WATER"]],"market":[]},{"farmer":["FEED"],"hands":[["EAST"],["WATER"],["WEST"],["COLLECT_FERTILIZER"],["EAST"],["WATER"],["FERTILIZE"],["DIG"],["EAST"],["COLLECT_FERTILIZER"],["WEST"]],"market":[]},{"farmer":["CARE"],"hands":[["FERTILIZE"],["SOUTH"],["WATER"],["HARVEST"],["FERTILIZE"],["HARVEST"],["WATER"],["PLANT","WHEAT"],["HARVEST"],["NORTH"],["WATER"]],"market":[["SELL","STRAWBERRY",4],["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["SOUTH"],["SOUTH"],["EAST"],["WATER"],["WEST"],["NORTH"],["WATER"],["EAST"],["HARVEST"],["HARVEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["WATER"],["WATER"],["EAST"],["NORTH"],["WATER"],["FERTILIZE"],["NORTH"],["HARVEST"],["DIG"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["HARVEST"],["HARVEST"],["EAST"],["FERTILIZE"],["HARVEST"],["WATER"],["EAST"],["FERTILIZE"],["PLANT","WHEAT"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["SOUTH"],["WEST"],["SOUTH"],["WATER"],["WATER"],["WEST"],["NORTH"],["HARVEST"],["EAST"],["WATER"],["SOUTH"]],"market":[["SELL","MILK",4]]},{"farmer":["NORTH"],"hands":[["EAST"],["WATER"],["WEST"],["SOUTH"],["WEST"],["HARVEST"],["FERTILIZE"],["DIG"],["FERTILIZE"],["WEST"],["WATER"]],"market":[["SELL","TOMATO",10]]},{"farmer":["HARVEST"],"hands":[["WATER"],["EAST"],["WATER"],["FERTILIZE"],["WEST"],["WATER"],["WATER"],["PLANT","WHEAT"],["WATER"],["SOUTH"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["DIG"],"hands":[["HARVEST"],["NORTH"],["SOUTH"],["WATER"],["SOUTH"],["WEST"],["NORTH"],["WATER"],["EAST"],["SOUTH"],["SOUTH"]],"market":[["SELL","EGG",8]]},{"farmer":["PLANT","WHEAT"],"hands":[["SOUTH"],["WATER"],["WATER"],["EAST"],["FEED"],["EAST"],["WATER"],["SOUTH"],["WEST"],["WEST"],["WATER"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["WATER"],"hands":[["SOUTH"],["EAST"],["NORTH"],["FERTILIZE"],["CARE"],["NORTH"],["HARVEST"],["COLLECT_FERTILIZER"],["SOUTH"],["FEED"],["PASS"]],"market":[["SELL","EGG",4]]},{"farmer":["WEST"],"hands":[["PASS"],["HARVEST"],["PASS"],["WATER"],["HARVEST"],["PASS"],["SOUTH"],["CARE"],["PASS"],["PASS"],["PASS"]],"market":[["SELL","TOMATO",3]]},{"farmer":["PICKUP","WHEAT",3],"hands":[],"market":[["SELL","TOMATO",13],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["PICKUP","WHEAT",2],["PICKUP","WHEAT",3],["EAST"],["SOUTH"],["SOUTH"],["NORTH"],["NORTH"]],"market":[["SELL","MILK",4],["SELL","FERTILIZER",8],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["FEED"],["FEED"],["WEST"],["FEED"],["EAST"],["HARVEST"],["SOUTH"],["COLLECT_FERTILIZER"],["NORTH"],["COLLECT_FERTILIZER"],["EAST"]],"market":[]},{"farmer":["CARE"],"hands":[["CARE"],["CARE"],["WEST"],["CARE"],["EAST"],["DIG"],["WEST"],["WEST"],["NORTH"],["WEST"],["EAST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FEED"],["NORTH"],["WATER"],["PLANT","WHEAT"],["HARVEST"],["WATER"],["HARVEST"],["WEST"],["WATER"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["WEST"],["CARE"],["NORTH"],["HARVEST"],["WATER"],["DIG"],["HARVEST"],["NORTH"],["COLLECT_FERTILIZER"],["HARVEST"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["FEED"],"hands":[["FEED"],["WEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["PLANT","WHEAT"],["WEST"],["PLANT","WHEAT"],["PLANT","WHEAT"],["HARVEST"],["WEST"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["CARE"],["FEED"],["HARVEST"],["HARVEST"],["WATER"],["HARVEST"],["WATER"],["WATER"],["EAST"],["WEST"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["COLLECT_FERTILIZER"],["CARE"],["WEST"],["NORTH"],["EAST"],["WATER"],["SOUTH"],["NORTH"],["WATER"],["WATER"],["NORTH"]],"market":[]},{"farmer":["WATER"],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["WEST"],["WATER"],["HARVEST"],["SOUTH"],["HARVEST"],["WATER"],["EAST"],["HARVEST"],["HARVEST"]],"market":[["SELL","STRAWBERRY",6]]},{"farmer":["HARVEST"],"hands":[["FEED"],["HARVEST"],["WATER"],["NORTH"],["NORTH"],["HARVEST"],["DIG"],["HARVEST"],["HARVEST"],["NORTH"],["WEST"]],"market":[]},{"farmer":["PLANT","WHEAT"],"hands":[["CARE"],["SOUTH"],["HARVEST"],["FEED"],["HARVEST"],["WATER"],["PLANT","WHEAT"],["PLANT","WHEAT"],["DIG"],["WATER"],["FEED"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["PLANT","WHEAT"],["CARE"],["WEST"],["SOUTH"],["WATER"],["WATER"],["PLANT","WHEAT"],["NORTH"],["CARE"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["HARVEST"],["FERTILIZE"],["WATER"],["COLLECT_FERTILIZER"],["HARVEST"],["WATER"],["WEST"],["NORTH"],["WATER"],["NORTH"],["COLLECT_FERTILIZER"]],"market":[["SELL","MILK",2],["SELL","STRAWBERRY",4]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["EAST"],["WATER"],["NORTH"],["WEST"],["WEST"],["SOUTH"],["SOUTH"],["COLLECT_FERTILIZER"],["EAST"],["FERTILIZE"],["HARVEST"]],"market":[["SELL","TOMATO",6]]},{"farmer":["HARVEST"],"hands":[["HARVEST"],["SOUTH"],["NORTH"],["WEST"],["WEST"],["WATER"],["WEST"],["HARVEST"],["HARVEST"],["WATER"],["WEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["SOUTH"],["HARVEST"],["FERTILIZE"],["WEST"],["SOUTH"],["HARVEST"],["WATER"],["WEST"],["EAST"],["NORTH"],["SOUTH"]],"market":[]},{"farmer":["FEED"],"hands":[["WEST"],["DIG"],["WATER"],["WATER"],["WEST"],["NORTH"],["HARVEST"],["SOUTH"],["HARVEST"],["WATER"],["DROP"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["CARE"],"hands":[["SOUTH"],["PLANT","WHEAT"],["SOUTH"],["EAST"],["DROP"],["WEST"],["WEST"],["SOUTH"],["SOUTH"],["HARVEST"],["EAST"]],"market":[["SELL","STRAWBERRY",6],["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["DROP"],["WATER"],["WEST"],["EAST"],["HARVEST"],["WATER"],["WATER"],["EAST"],["HARVEST"],["SOUTH"],["EAST"]],"market":[["SELL","EGG",8],["SELL","FERTILIZER",2]]},{"farmer":["SOUTH"],"hands":[["NORTH"],["SOUTH"],["SOUTH"],["FERTILIZE"],["DROP"],["HARVEST"],["HARVEST"],["EAST"],["SOUTH"],["EAST"],["NORTH"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["WEST"],"hands":[["HARVEST"],["FERTILIZE"],["SOUTH"],["WEST"],["NORTH"],["NORTH"],["WEST"],["SOUTH"],["HARVEST"],["SOUTH"],["NORTH"]],"market":[["SELL","MILK",3]]},{"farmer":["HARVEST"],"hands":[["SOUTH"],["WATER"],["WATER"],["FERTILIZE"],["SOUTH"],["WATER"],["NORTH"],["DROP"],["WEST"],["PASS"],["HARVEST"]],"market":[["SELL","WHEAT",13],["SELL","CARROT",6]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WEST"],["HARVEST"],["HARVEST"],["SOUTH"],["PASS"],["NORTH"],["WATER"],["HARVEST"],["HARVEST"],["PASS"],["NORTH"]],"market":[["SELL","STRAWBERRY",2],["SELL","EGG",6]]},{"farmer":["PICKUP","WHEAT",3],"hands":[],"market":[["SELL","TOMATO",13],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["PICKUP","WHEAT",3],["HARVEST"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["EAST"],["WEST"],["PICKUP","FERTILIZER",3],["WEST"],["NORTH"]],"market":[["SELL","MILK",4],["SELL","FERTILIZER",8],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["FEED"],["DROP"],["WEST"],["FEED"],["WATER"],["COLLECT_FERTILIZER"],["SOUTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3]],"market":[]},{"farmer":["CARE"],"hands":[["CARE"],["PICKUP","WHEAT",3],["WEST"],["CARE"],["EAST"],["WEST"],["SOUTH"],["WEST"],["NORTH"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["FEED"],["FEED"],["COLLECT_FERTILIZER"],["EAST"],["COLLECT_FERTILIZER"],["WEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["NORTH"],["FEED"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["CARE"],["CARE"],["WEST"],["EAST"],["WEST"],["SOUTH"],["WEST"],["NORTH"],["FEED"],["CARE"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["NORTH"],"hands":[["EAST"],["COLLECT_FERTILIZER"],["HARVEST"],["WEST"],["WATER"],["WEST"],["SOUTH"],["WATER"],["WATER"],["CARE"],["EAST"]],"market":[]},{"farmer":["NORTH"],"hands":[["FEED"],["SOUTH"],["SOUTH"],["NORTH"],["NORTH"],["FERTILIZE"],["FERTILIZE"],["NORTH"],["NORTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["FEED"],"hands":[["CARE"],["SOUTH"],["WATER"],["NORTH"],["WATER"],["WATER"],["WATER"],["WATER"],["WATER"],["NORTH"],["EAST"]],"market":[]},{"farmer":["CARE"],"hands":[["HARVEST"],["WEST"],["HARVEST"],["FEED"],["NORTH"],["SOUTH"],["WEST"],["HARVEST"],["EAST"],["NORTH"],["WATER"]],"market":[["SELL","MILK",2]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["HARVEST"],["WEST"],["CARE"],["WATER"],["HARVEST"],["HARVEST"],["PLANT","WHEAT"],["HARVEST"],["FEED"],["EAST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["WATER"],["FERTILIZE"],["WATER"],["COLLECT_FERTILIZER"],["NORTH"],["FERTILIZE"],["FERTILIZE"],["WATER"],["EAST"],["CARE"],["WATER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WEST"],["WATER"],["WEST"],["WEST"],["WATER"],["WATER"],["WATER"],["NORTH"],["EAST"],["COLLECT_FERTILIZER"],["NORTH"]],"market":[]},{"farmer":["HARVEST"],"hands":[["FEED"],["SOUTH"],["WATER"],["FEED"],["WEST"],["SOUTH"],["WEST"],["WEST"],["WATER"],["HARVEST"],["WATER"]],"market":[["SELL","STRAWBERRY",6],["SELL","STRAWBERRY",2]]},{"farmer":["NORTH"],"hands":[["CARE"],["WATER"],["HARVEST"],["CARE"],["HARVEST"],["WATER"],["HARVEST"],["FERTILIZE"],["EAST"],["WEST"],["WEST"]],"market":[]},{"farmer":["WATER"],"hands":[["HARVEST"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["WATER"],["SOUTH"],["DIG"],["WATER"],["FERTILIZE"],["WATER"],["FERTILIZE"]],"market":[]},{"farmer":["WEST"],"hands":[["SOUTH"],["HARVEST"],["EAST"],["NORTH"],["WEST"],["HARVEST"],["PLANT","WHEAT"],["NORTH"],["WATER"],["WEST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","CARROT",6]]},{"farmer":["WATER"],"hands":[["HARVEST"],["WATER"],["HARVEST"],["FERTILIZE"],["WATER"],["WATER"],["WATER"],["WATER"],["SOUTH"],["HARVEST"],["WEST"]],"market":[["SELL","MILK",2],["SELL","STRAWBERRY",1]]},{"farmer":["WEST"],"hands":[["SOUTH"],["WEST"],["FEED"],["WATER"],["HARVEST"],["SOUTH"],["WEST"],["HARVEST"],["SOUTH"],["PLANT","WHEAT"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["DROP"],["WATER"],["CARE"],["SOUTH"],["SOUTH"],["WATER"],["WATER"],["PLANT","WHEAT"],["SOUTH"],["WATER"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["DIG"],"hands":[["EAST"],["HARVEST"],["EAST"],["SOUTH"],["SOUTH"],["PASS"],["HARVEST"],["WATER"],["SOUTH"],["SOUTH"],["NORTH"]],"market":[["SELL","EGG",8]]},{"farmer":["PLANT","CARROT"],"hands":[["HARVEST"],["NORTH"],["EAST"],["WEST"],["SOUTH"],["NORTH"],["FERTILIZE"],["SOUTH"],["WEST"],["FEED"],["WATER"]],"market":[["SELL","MILK",5]]},{"farmer":["WATER"],"hands":[["PLANT","WHEAT"],["EAST"],["DROP"],["SOUTH"],["WEST"],["NORTH"],["PASS"],["SOUTH"],["FERTILIZE"],["CARE"],["EAST"]],"market":[["SELL","TOMATO",10],["SELL","EGG",8],["SELL","EGG",8]]},{"farmer":["SOUTH"],"hands":[["WATER"],["WATER"],["PASS"],["WATER"],["PASS"],["PASS"],["PASS"],["WATER"],["SOUTH"],["EAST"],["WATER"]],"market":[["SELL","TOMATO",6],["SELL","FERTILIZER",1]]},{"farmer":["PICKUP","WHEAT",2],"hands":[],"market":[["SELL","TOMATO",6],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["EAST"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",2],["PICKUP","WHEAT",3],["NORTH"],["SOUTH"],["EAST"],["NORTH"],["NORTH"]],"market":[["SELL","WOOL",4],["SELL","FERTILIZER",8],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["EAST"],["FEED"],["WEST"],["FEED"],["NORTH"],["SOUTH"],["EAST"],["COLLECT_FERTILIZER"],["NORTH"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3]],"market":[]},{"farmer":["CARE"],"hands":[["EAST"],["CARE"],["WEST"],["CARE"],["NORTH"],["SOUTH"],["EAST"],["NORTH"],["NORTH"],["FEED"],["NORTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["EAST"],["COLLECT_FERTILIZER"],["FEED"],["COLLECT_FERTILIZER"],["HARVEST"],["WATER"],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"],["CARE"],["NORTH"]],"market":[]},{"farmer":["WEST"],"hands":[["HARVEST"],["SOUTH"],["CARE"],["WEST"],["DIG"],["SOUTH"],["WATER"],["NORTH"],["HARVEST"],["COLLECT_FERTILIZER"],["FEED"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["FEED"],"hands":[["DIG"],["FERTILIZE"],["COLLECT_FERTILIZER"],["NORTH"],["PLANT","WHEAT"],["HARVEST"],["NORTH"],["FERTILIZE"],["DIG"],["NORTH"],["CARE"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["PLANT","WHEAT"],["WATER"],["WEST"],["FERTILIZE"],["WATER"],["WEST"],["HARVEST"],["WATER"],["PLANT","WHEAT"],["FEED"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["WATER"],["SOUTH"],["FEED"],["WATER"],["EAST"],["HARVEST"],["DIG"],["WEST"],["WATER"],["CARE"],["NORTH"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["WATER"],["CARE"],["WEST"],["EAST"],["DIG"],["PLANT","WHEAT"],["COLLECT_FERTILIZER"],["EAST"],["COLLECT_FERTILIZER"],["NORTH"]],"market":[["SELL","MILK",2],["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["HARVEST"],["WEST"],["COLLECT_FERTILIZER"],["WATER"],["HARVEST"],["PLANT","CARROT"],["WATER"],["HARVEST"],["EAST"],["EAST"],["FEED"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FERTILIZE"],"hands":[["DIG"],["HARVEST"],["SOUTH"],["NORTH"],["DIG"],["WATER"],["NORTH"],["SOUTH"],["WATER"],["FEED"],["CARE"]],"market":[]},{"farmer":["WATER"],"hands":[["PLANT","WHEAT"],["DIG"],["FERTILIZE"],["FEED"],["PLANT","WHEAT"],["WEST"],["HARVEST"],["FERTILIZE"],["EAST"],["CARE"],["COLLECT_FERTILIZER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["WATER"],["PLANT","CARROT"],["WATER"],["CARE"],["WATER"],["WEST"],["DIG"],["WATER"],["HARVEST"],["COLLECT_FERTILIZER"],["WEST"]],"market":[["SELL","MILK",2],["BUY_SEED","WHEAT",1]]},{"farmer":["FERTILIZE"],"hands":[["NORTH"],["WATER"],["WEST"],["COLLECT_FERTILIZER"],["SOUTH"],["HARVEST"],["PLANT","WHEAT"],["SOUTH"],["DIG"],["EAST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","CARROT",6]]},{"farmer":["WATER"],"hands":[["HARVEST"],["SOUTH"],["WATER"],["HARVEST"],["HARVEST"],["DIG"],["WATER"],["WEST"],["PLANT","WHEAT"],["HARVEST"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["DIG"],["HARVEST"],["HARVEST"],["NORTH"],["DIG"],["PLANT","CARROT"],["NORTH"],["SOUTH"],["WATER"],["DIG"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["PLANT","CARROT"],["WEST"],["WEST"],["FEED"],["PLANT","WHEAT"],["WATER"],["HARVEST"],["SOUTH"],["EAST"],["PLANT","WHEAT"],["WATER"]],"market":[["SELL","STRAWBERRY",2],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WATER"],["HARVEST"],["HARVEST"],["CARE"],["WATER"],["NORTH"],["DIG"],["WEST"],["HARVEST"],["WATER"],["SOUTH"]],"market":[["SELL","TOMATO",6]]},{"farmer":["HARVEST"],"hands":[["NORTH"],["DIG"],["DIG"],["COLLECT_FERTILIZER"],["WEST"],["WATER"],["PLANT","CARROT"],["FERTILIZE"],["DIG"],["SOUTH"],["FEED"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PLANT","WHEAT"],"hands":[["HARVEST"],["PLANT","CARROT"],["PLANT","CARROT"],["WEST"],["HARVEST"],["HARVEST"],["WATER"],["WATER"],["PLANT","CARROT"],["FERTILIZE"],["CARE"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["DIG"],["WATER"],["WATER"],["WATER"],["DIG"],["WEST"],["WEST"],["NORTH"],["WATER"],["WATER"],["EAST"]],"market":[["SELL","STRAWBERRY",2],["BUY_SEED","CARROT",6]]},{"farmer":["EAST"],"hands":[["PLANT","CARROT"],["NORTH"],["SOUTH"],["SOUTH"],["PLANT","WHEAT"],["WATER"],["WEST"],["NORTH"],["SOUTH"],["WEST"],["SOUTH"]],"market":[["SELL","WHEAT",10]]},{"farmer":["PASS"],"hands":[["WATER"],["WATER"],["HARVEST"],["COLLECT_FERTILIZER"],["WATER"],["NORTH"],["WATER"],["NORTH"],["PASS"],["FERTILIZE"],["EAST"]],"market":[["SELL","TOMATO",2]]},{"farmer":["PICKUP","WHEAT",2],"hands":[],"market":[["SELL","TOMATO",10],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",3],["HARVEST"],["PICKUP","WHEAT",2],["PICKUP","WHEAT",3],["EAST"],["SOUTH"],["PICKUP","FERTILIZER",3],["WEST"],["NORTH"]],"market":[["SELL","MILK",4],["SELL","STRAWBERRY",4],["HIRE"],["HIRE"]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FEED"],["DROP"],["WEST"],["FEED"],["WATER"],["WATER"],["SOUTH"],["WEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["EAST"]],"market":[["SELL","FERTILIZER",3]]},{"farmer":["NORTH"],"hands":[["CARE"],["COLLECT_FERTILIZER"],["WEST"],["CARE"],["EAST"],["HARVEST"],["SOUTH"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"],["EAST"]],"market":[]},{"farmer":["WATER"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["FEED"],["NORTH"],["WATER"],["PLANT","CARROT"],["WEST"],["WEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["EAST"]],"market":[]},{"farmer":["HARVEST"],"hands":[["NORTH"],["WEST"],["CARE"],["FEED"],["HARVEST"],["WATER"],["FERTILIZE"],["WATER"],["HARVEST"],["NORTH"],["WATER"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["PLANT","WHEAT"],"hands":[["FEED"],["COLLECT_FERTILIZER"],["HARVEST"],["NORTH"],["PLANT","WHEAT"],["WEST"],["WATER"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["CARE"],["HARVEST"],["COLLECT_FERTILIZER"],["FEED"],["WATER"],["HARVEST"],["SOUTH"],["HARVEST"],["NORTH"],["WEST"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["HARVEST"],["WEST"],["WEST"],["CARE"],["WEST"],["DIG"],["FERTILIZE"],["DIG"],["EAST"],["WATER"],["WATER"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["NORTH"],["WATER"],["FEED"],["NORTH"],["NORTH"],["PLANT","WHEAT"],["WATER"],["PLANT","WHEAT"],["FERTILIZE"],["HARVEST"],["WEST"]],"market":[["SELL","STRAWBERRY",4],["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["FEED"],["HARVEST"],["CARE"],["HARVEST"],["FEED"],["WATER"],["SOUTH"],["WATER"],["WATER"],["PLANT","WHEAT"],["WEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["CARE"],["PLANT","WHEAT"],["SOUTH"],["WEST"],["CARE"],["EAST"],["WATER"],["NORTH"],["HARVEST"],["WATER"],["WEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["WEST"],["WATER"],["WEST"],["COLLECT_FERTILIZER"],["HARVEST"],["NORTH"],["WEST"],["NORTH"],["EAST"],["WEST"],["HARVEST"]],"market":[]},{"farmer":["CARE"],"hands":[["NORTH"],["SOUTH"],["HARVEST"],["WEST"],["COLLECT_FERTILIZER"],["FEED"],["WEST"],["WATER"],["FERTILIZE"],["WEST"],["DROP"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["FERTILIZE"],["SOUTH"],["COLLECT_FERTILIZER"],["WEST"],["CARE"],["WATER"],["HARVEST"],["WATER"],["FEED"],["PICKUP","WHEAT",2]],"market":[["SELL","TOMATO",6]]},{"farmer":["NORTH"],"hands":[["COLLECT_FERTILIZER"],["WATER"],["DIG"],["HARVEST"],["SOUTH"],["DROP"],["WEST"],["PLANT","WHEAT"],["HARVEST"],["CARE"],["WEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["HARVEST"],["WEST"],["PLANT","CARROT"],["NORTH"],["DROP"],["SOUTH"],["WEST"],["WATER"],["PLANT","WHEAT"],["COLLECT_FERTILIZER"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","CARROT",6]]},{"farmer":["CARE"],"hands":[["SOUTH"],["SOUTH"],["WATER"],["FERTILIZE"],["WEST"],["SOUTH"],["WATER"],["NORTH"],["WATER"],["SOUTH"],["DROP"]],"market":[["SELL","MILK",6],["SELL","STRAWBERRY",2]]},{"farmer":["EAST"],"hands":[["SOUTH"],["FERTILIZE"],["SOUTH"],["WATER"],["SOUTH"],["WEST"],["NORTH"],["FERTILIZE"],["WEST"],["FERTILIZE"],["PICKUP","WHEAT",2]],"market":[["SELL","EGG",8]]},{"farmer":["FEED"],"hands":[["SOUTH"],["WATER"],["HARVEST"],["WEST"],["SOUTH"],["SOUTH"],["HARVEST"],["WATER"],["WEST"],["WATER"],["NORTH"]],"market":[["SELL","TOMATO",3]]},{"farmer":["CARE"],"hands":[["SOUTH"],["SOUTH"],["DIG"],["WATER"],["WEST"],["WATER"],["DIG"],["NORTH"],["WEST"],["NORTH"],["CARE"]],"market":[]},{"farmer":["EAST"],"hands":[["DROP"],["PLANT","CARROT"],["PLANT","CARROT"],["SOUTH"],["WEST"],["WEST"],["SOUTH"],["WATER"],["FEED"],["HARVEST"],["SOUTH"]],"market":[["SELL","MILK",6],["SELL","STRAWBERRY",2]]},{"farmer":["EAST"],"hands":[["PASS"],["WATER"],["WATER"],["WATER"],["HARVEST"],["NORTH"],["EAST"],["SOUTH"],["CARE"],["SOUTH"],["DROP"]],"market":[["SELL","WHEAT",10],["SELL","FERTILIZER",3]]},{"farmer":["FERTILIZE"],"hands":[["PASS"],["PASS"],["EAST"],["HARVEST"],["SOUTH"],["WATER"],["WATER"],["SOUTH"],["PASS"],["PASS"],["PASS"]],"market":[["SELL","WHEAT",5],["SELL","EGG",4]]},{"farmer":["PICKUP","WHEAT",2],"hands":[],"market":[["SELL","TOMATO",6],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["PICKUP","WHEAT",2],["HARVEST"],["PICKUP","FERTILIZER",4],["SOUTH"],["PICKUP","FERTILIZER",2],["NORTH"],["NORTH"]],"market":[["SELL","MILK",2],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["FEED"],["FEED"],["WEST"],["PLACE","MILK",3],["EAST"],["SOUTH"],["EAST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["CARE"]],"market":[]},{"farmer":["CARE"],"hands":[["CARE"],["COLLECT_FERTILIZER"],["WEST"],["PICKUP","WHEAT",3],["WATER"],["WATER"],["NORTH"],["WEST"],["NORTH"],["WEST"],["SOUTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["FEED"],["FEED"],["NORTH"],["HARVEST"],["HARVEST"],["WEST"],["COLLECT_FERTILIZER"],["WEST"],["SOUTH"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["WEST"],["CARE"],["CARE"],["COLLECT_FERTILIZER"],["PLANT","CARROT"],["PLANT","WHEAT"],["WATER"],["NORTH"],["COLLECT_FERTILIZER"],["SOUTH"]],"market":[["SELL","MILK",2]]},{"farmer":["FEED"],"hands":[["FEED"],["FEED"],["COLLECT_FERTILIZER"],["NORTH"],["EAST"],["WATER"],["WATER"],["HARVEST"],["WATER"],["WEST"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["CARE"],["CARE"],["HARVEST"],["NORTH"],["FERTILIZE"],["WEST"],["NORTH"],["PLANT","WHEAT"],["NORTH"],["FERTILIZE"],["HARVEST"]],"market":[["SELL","WHEAT",8],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["SOUTH"],["FEED"],["WATER"],["WATER"],["FEED"],["NORTH"],["FERTILIZE"],["WATER"],["PLANT","CARROT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["FEED"],["HARVEST"],["WEST"],["CARE"],["EAST"],["HARVEST"],["CARE"],["FEED"],["WATER"],["NORTH"],["WATER"]],"market":[["SELL","MILK",2]]},{"farmer":["WATER"],"hands":[["CARE"],["WEST"],["WATER"],["COLLECT_FERTILIZER"],["FERTILIZE"],["PLANT","CARROT"],["HARVEST"],["CARE"],["EAST"],["WEST"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["EAST"],["WEST"],["WEST"],["HARVEST"],["WATER"],["WATER"],["NORTH"],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["HARVEST"]],"market":[]},{"farmer":["PLANT","WHEAT"],"hands":[["FERTILIZE"],["FERTILIZE"],["HARVEST"],["NORTH"],["EAST"],["NORTH"],["NORTH"],["HARVEST"],["EAST"],["NORTH"],["WEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WATER"],["WATER"],["DIG"],["WATER"],["FERTILIZE"],["NORTH"],["FERTILIZE"],["NORTH"],["EAST"],["NORTH"],["WATER"]],"market":[["SELL","STRAWBERRY",4],["SELL","STRAWBERRY",2]]},{"farmer":["NORTH"],"hands":[["EAST"],["SOUTH"],["PLANT","WHEAT"],["NORTH"],["WATER"],["EAST"],["WATER"],["FEED"],["FERTILIZE"],["WATER"],["WEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["WATER"],["WATER"],["WATER"],["FEED"],["SOUTH"],["DROP"],["EAST"],["CARE"],["WATER"],["HARVEST"],["WATER"]],"market":[["SELL","EGG",8]]},{"farmer":["CARE"],"hands":[["EAST"],["SOUTH"],["SOUTH"],["CARE"],["FERTILIZE"],["HARVEST"],["FERTILIZE"],["COLLECT_FERTILIZER"],["EAST"],["PLANT","WHEAT"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","CARROT",6]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["HARVEST"],["SOUTH"],["COLLECT_FERTILIZER"],["WATER"],["DROP"],["WATER"],["EAST"],["WATER"],["WATER"],["PLANT","CARROT"]],"market":[["SELL","STRAWBERRY",4],["SELL","STRAWBERRY",2]]},{"farmer":["HARVEST"],"hands":[["HARVEST"],["WATER"],["SOUTH"],["WEST"],["NORTH"],["SOUTH"],["EAST"],["FEED"],["HARVEST"],["NORTH"],["WATER"]],"market":[["SELL","WHEAT",10]]},{"farmer":["NORTH"],"hands":[["PLANT","CARROT"],["SOUTH"],["WATER"],["FERTILIZE"],["NORTH"],["SOUTH"],["WATER"],["CARE"],["PLANT","CARROT"],["WATER"],["NORTH"]],"market":[["SELL","TOMATO",2]]},{"farmer":["PLANT","CARROT"],"hands":[["WATER"],["SOUTH"],["WEST"],["WATER"],["FERTILIZE"],["WEST"],["HARVEST"],["HARVEST"],["WATER"],["HARVEST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["EAST"],["FERTILIZE"],["NORTH"],["WEST"],["WATER"],["SOUTH"],["PLANT","CARROT"],["COLLECT_FERTILIZER"],["SOUTH"],["PLANT","CARROT"],["HARVEST"]],"market":[["SELL","MILK",2],["SELL","STRAWBERRY",2]]},{"farmer":["NORTH"],"hands":[["NORTH"],["WATER"],["FERTILIZE"],["WATER"],["NORTH"],["HARVEST"],["WATER"],["SOUTH"],["WATER"],["WATER"],["PLANT","CARROT"]],"market":[["SELL","EGG",5],["SELL","CARROT",2]]},{"farmer":["WATER"],"hands":[["PASS"],["PASS"],["WATER"],["SOUTH"],["SOUTH"],["WEST"],["SOUTH"],["FERTILIZE"],["SOUTH"],["EAST"],["WATER"]],"market":[["SELL","TOMATO",2],["SELL","WHEAT",2]]},{"farmer":["PICKUP","WHEAT",2],"hands":[],"market":[["SELL","CARROT",6],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["PICKUP","WHEAT",2],["PICKUP","WHEAT",3],["NORTH"],["WEST"],["PICKUP","FERTILIZER",3],["WEST"],["NORTH"]],"market":[["SELL","MILK",2],["SELL","WOOL",1],["HIRE"],["HIRE"]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FEED"],["FEED"],["WEST"],["FEED"],["HARVEST"],["COLLECT_FERTILIZER"],["SOUTH"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["EAST"]],"market":[]},{"farmer":["NORTH"],"hands":[["CARE"],["CARE"],["WEST"],["CARE"],["COLLECT_FERTILIZER"],["WEST"],["SOUTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["NORTH"],["EAST"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FEED"],["NORTH"],["EAST"],["COLLECT_FERTILIZER"],["WEST"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["EAST"]],"market":[]},{"farmer":["WATER"],"hands":[["NORTH"],["SOUTH"],["CARE"],["NORTH"],["COLLECT_FERTILIZER"],["WEST"],["SOUTH"],["HARVEST"],["WATER"],["NORTH"],["WATER"]],"market":[["SELL","MILK",2]]},{"farmer":["NORTH"],"hands":[["FEED"],["FERTILIZE"],["HARVEST"],["FEED"],["EAST"],["FERTILIZE"],["SOUTH"],["WEST"],["HARVEST"],["NORTH"],["EAST"]],"market":[]},{"farmer":["WATER"],"hands":[["CARE"],["WATER"],["WEST"],["CARE"],["WATER"],["WATER"],["FERTILIZE"],["FERTILIZE"],["PLANT","WHEAT"],["HARVEST"],["WATER"]],"market":[]},{"farmer":["WEST"],"hands":[["EAST"],["WEST"],["FEED"],["COLLECT_FERTILIZER"],["HARVEST"],["WEST"],["WATER"],["WATER"],["WATER"],["NORTH"],["HARVEST"]],"market":[]},{"farmer":["FEED"],"hands":[["FEED"],["WATER"],["CARE"],["NORTH"],["PLANT","WHEAT"],["WATER"],["WEST"],["NORTH"],["NORTH"],["COLLECT_FERTILIZER"],["PLANT","CARROT"]],"market":[["SELL","MILK",2],["SELL","STRAWBERRY",2]]},{"farmer":["CARE"],"hands":[["CARE"],["WEST"],["HARVEST"],["WEST"],["WATER"],["HARVEST"],["WATER"],["HARVEST"],["WATER"],["HARVEST"],["WATER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["HARVEST"],["SOUTH"],["FEED"],["SOUTH"],["PLANT","WHEAT"],["HARVEST"],["NORTH"],["HARVEST"],["WEST"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["WATER"],["SOUTH"],["SOUTH"],["CARE"],["FERTILIZE"],["WATER"],["PLANT","CARROT"],["WATER"],["PLANT","WHEAT"],["WATER"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["EAST"],["WATER"],["WEST"],["COLLECT_FERTILIZER"],["WATER"],["SOUTH"],["WATER"],["HARVEST"],["WATER"],["HARVEST"],["NORTH"]],"market":[["SELL","MILK",4],["SELL","STRAWBERRY",2]]},{"farmer":["CARE"],"hands":[["FERTILIZE"],["SOUTH"],["WATER"],["WEST"],["WEST"],["WATER"],["NORTH"],["PLANT","WHEAT"],["EAST"],["PLANT","WHEAT"],["WATER"]],"market":[["SELL","WHEAT",10],["SELL","FERTILIZER",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["WEST"],["WEST"],["HARVEST"],["WEST"],["HARVEST"],["FERTILIZE"],["WATER"],["HARVEST"],["WATER"],["HARVEST"]],"market":[["SELL","FERTILIZER",3]]},{"farmer":["NORTH"],"hands":[["NORTH"],["WATER"],["WATER"],["COLLECT_FERTILIZER"],["DROP"],["PLANT","WHEAT"],["WATER"],["EAST"],["DIG"],["EAST"],["PLANT","CARROT"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","CARROT",6]]},{"farmer":["NORTH"],"hands":[["WATER"],["SOUTH"],["SOUTH"],["NORTH"],["HARVEST"],["WATER"],["WEST"],["EAST"],["PLANT","CARROT"],["FEED"],["WATER"]],"market":[["SELL","STRAWBERRY",4],["SELL","STRAWBERRY",2]]},{"farmer":["FERTILIZE"],"hands":[["HARVEST"],["WATER"],["WATER"],["WATER"],["DROP"],["EAST"],["NORTH"],["EAST"],["WATER"],["CARE"],["NORTH"]],"market":[["SELL","EGG",8]]},{"farmer":["WATER"],"hands":[["PLANT","CARROT"],["HARVEST"],["HARVEST"],["HARVEST"],["EAST"],["FERTILIZE"],["FERTILIZE"],["SOUTH"],["EAST"],["SOUTH"],["WATER"]],"market":[["SELL","WHEAT",10]]},{"farmer":["WEST"],"hands":[["WATER"],["PLANT","CARROT"],["PLANT","CARROT"],["PLANT","CARROT"],["EAST"],["EAST"],["EAST"],["EAST"],["FERTILIZE"],["SOUTH"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FERTILIZE"],"hands":[["WEST"],["WATER"],["WATER"],["WATER"],["EAST"],["EAST"],["NORTH"],["SOUTH"],["WATER"],["SOUTH"],["PLANT","CARROT"]],"market":[["SELL","MILK",4]]},{"farmer":["SOUTH"],"hands":[["WATER"],["WEST"],["SOUTH"],["SOUTH"],["NORTH"],["SOUTH"],["SOUTH"],["DROP"],["EAST"],["SOUTH"],["WATER"]],"market":[["SELL","CARROT",3],["SELL","TOMATO",2]]},{"farmer":["WATER"],"hands":[["HARVEST"],["WATER"],["PASS"],["CARE"],["WATER"],["WATER"],["PASS"],["PASS"],["WATER"],["DROP"],["NORTH"]],"market":[["SELL","WHEAT",3],["SELL","FERTILIZER",2],["SELL","EGG",4]]},{"farmer":["HARVEST"],"hands":[],"market":[["SELL","CARROT",13],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["PLACE","MILK",3],"hands":[["HARVEST"],["HARVEST"],["PICKUP","WHEAT",2],["PICKUP","WHEAT",3],["NORTH"],["SOUTH"],["PICKUP","FERTILIZER",3],["NORTH"],["NORTH"]],"market":[["SELL","MILK",4],["SELL","WHEAT",13],["HIRE"],["HIRE"]]},{"farmer":["PICKUP","WHEAT",3],"hands":[["PLACE","MILK",3],["DROP"],["WEST"],["FEED"],["COLLECT_FERTILIZER"],["WATER"],["WEST"],["DIG"],["NORTH"],["EAST"],["WEST"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["CARE"],"hands":[["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["WEST"],["WEST"],["EAST"],["HARVEST"],["SOUTH"],["PLANT","WHEAT"],["COLLECT_FERTILIZER"],["EAST"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FEED"],["FEED"],["FEED"],["FEED"],["COLLECT_FERTILIZER"],["PLANT","WHEAT"],["SOUTH"],["WATER"],["HARVEST"],["WATER"],["WEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["CARE"],["CARE"],["CARE"],["COLLECT_FERTILIZER"],["HARVEST"],["WATER"],["FERTILIZE"],["WEST"],["EAST"],["HARVEST"],["COLLECT_FERTILIZER"]],"market":[["SELL","MILK",2]]},{"farmer":["NORTH"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WEST"],["WEST"],["EAST"],["WEST"],["WATER"],["WATER"],["WATER"],["PLANT","WHEAT"],["SOUTH"]],"market":[]},{"farmer":["FEED"],"hands":[["EAST"],["WEST"],["FEED"],["COLLECT_FERTILIZER"],["EAST"],["WATER"],["SOUTH"],["HARVEST"],["HARVEST"],["WATER"],["FERTILIZE"]],"market":[]},{"farmer":["CARE"],"hands":[["FERTILIZE"],["HARVEST"],["CARE"],["WEST"],["WATER"],["HARVEST"],["FERTILIZE"],["PLANT","WHEAT"],["PLANT","WHEAT"],["EAST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["WEST"],["WEST"],["WATER"],["HARVEST"],["PLANT","WHEAT"],["WATER"],["WATER"],["WATER"],["WATER"],["WEST"]],"market":[["SELL","MILK",2],["SELL","STRAWBERRY",2]]},{"farmer":["NORTH"],"hands":[["NORTH"],["HARVEST"],["WATER"],["NORTH"],["PLANT","WHEAT"],["WATER"],["SOUTH"],["NORTH"],["NORTH"],["HARVEST"],["WATER"]],"market":[["SELL","WHEAT",8],["BUY_SEED","WHEAT",1]]},{"farmer":["FERTILIZE"],"hands":[["FEED"],["NORTH"],["HARVEST"],["FERTILIZE"],["WATER"],["SOUTH"],["HARVEST"],["WATER"],["WATER"],["PLANT","WHEAT"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","CARROT",6]]},{"farmer":["WATER"],"hands":[["CARE"],["NORTH"],["PLANT","WHEAT"],["WATER"],["NORTH"],["WATER"],["WEST"],["HARVEST"],["HARVEST"],["WATER"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["WEST"],["FERTILIZE"],["WATER"],["WEST"],["FERTILIZE"],["WEST"],["WEST"],["PLANT","WHEAT"],["WEST"],["NORTH"],["HARVEST"]],"market":[["SELL","MILK",4],["SELL","STRAWBERRY",2]]},{"farmer":["FEED"],"hands":[["FEED"],["WATER"],["NORTH"],["FERTILIZE"],["WATER"],["WATER"],["FERTILIZE"],["WATER"],["SOUTH"],["EAST"],["PLANT","CARROT"]],"market":[["SELL","TOMATO",2],["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["CARE"],["NORTH"],["NORTH"],["WATER"],["NORTH"],["HARVEST"],["WATER"],["NORTH"],["FEED"],["WATER"],["WATER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["EAST"],["FEED"],["NORTH"],["NORTH"],["FERTILIZE"],["EAST"],["WEST"],["FEED"],["CARE"],["HARVEST"],["SOUTH"]],"market":[]},{"farmer":["EAST"],"hands":[["NORTH"],["CARE"],["FEED"],["NORTH"],["WATER"],["NORTH"],["WEST"],["CARE"],["SOUTH"],["PLANT","CARROT"],["WATER"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["EAST"],"hands":[["EAST"],["COLLECT_FERTILIZER"],["CARE"],["WATER"],["NORTH"],["EAST"],["WATER"],["COLLECT_FERTILIZER"],["SOUTH"],["WATER"],["HARVEST"]],"market":[["SELL","EGG",8]]},{"farmer":["EAST"],"hands":[["WATER"],["HARVEST"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"],["NORTH"],["HARVEST"],["HARVEST"],["DROP"],["WEST"],["PLANT","CARROT"]],"market":[["SELL","EGG",8]]},{"farmer":["WATER"],"hands":[["HARVEST"],["NORTH"],["HARVEST"],["WATER"],["HARVEST"],["DROP"],["NORTH"],["WEST"],["NORTH"],["WEST"],["WATER"]],"market":[["SELL","CARROT",7]]},{"farmer":["HARVEST"],"hands":[["PLANT","CARROT"],["FEED"],["NORTH"],["EAST"],["PLANT","CARROT"],["SOUTH"],["NORTH"],["WEST"],["HARVEST"],["WEST"],["EAST"]],"market":[["SELL","STRAWBERRY",4],["SELL","WHEAT",10]]},{"farmer":["PLANT","CARROT"],"hands":[["WATER"],["CARE"],["FERTILIZE"],["WATER"],["WATER"],["SOUTH"],["HARVEST"],["PASS"],["SOUTH"],["SOUTH"],["FERTILIZE"]],"market":[["SELL","TOMATO",3],["SELL","CARROT",2]]},{"farmer":["WATER"],"hands":[["PASS"],["COLLECT_FERTILIZER"],["WATER"],["HARVEST"],["EAST"],["PASS"],["WATER"],["PASS"],["DROP"],["WEST"],["WATER"]],"market":[["SELL","TOMATO",2],["SELL","EGG",2]]},{"farmer":["PICKUP","WHEAT",2],"hands":[],"market":[["SELL","WHEAT",16],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["PICKUP","FERTILIZER",3],["PICKUP","WHEAT",3],["PICKUP","FERTILIZER",3],["SOUTH"],["PASS"],["WEST"],["NORTH"]],"market":[["SELL","MILK",4],["SELL","WHEAT",13],["HIRE"],["HIRE"]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FEED"],["FEED"],["WEST"],["FEED"],["EAST"],["SOUTH"],["WEST"],["WEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",2]],"market":[]},{"farmer":["NORTH"],"hands":[["CARE"],["CARE"],["WEST"],["CARE"],["WATER"],["WATER"],["WEST"],["DIG"],["NORTH"],["NORTH"],["WEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["HARVEST"],["HARVEST"],["COLLECT_FERTILIZER"],["PLANT","WHEAT"],["COLLECT_FERTILIZER"],["NORTH"],["FEED"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["WEST"],["WEST"],["NORTH"],["PLANT","WHEAT"],["PLANT","CARROT"],["SOUTH"],["WATER"],["NORTH"],["COLLECT_FERTILIZER"],["CARE"]],"market":[["SELL","MILK",2]]},{"farmer":["FEED"],"hands":[["FEED"],["WEST"],["WEST"],["FEED"],["WATER"],["WATER"],["SOUTH"],["WEST"],["FERTILIZE"],["NORTH"],["HARVEST"]],"market":[]},{"farmer":["CARE"],"hands":[["CARE"],["FEED"],["FERTILIZE"],["CARE"],["NORTH"],["SOUTH"],["WATER"],["HARVEST"],["WATER"],["HARVEST"],["WEST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["HARVEST"],["CARE"],["WATER"],["HARVEST"],["FEED"],["WATER"],["HARVEST"],["NORTH"],["EAST"],["NORTH"],["PASS"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["SOUTH"],["WEST"],["CARE"],["HARVEST"],["PLANT","CARROT"],["WATER"],["FERTILIZE"],["COLLECT_FERTILIZER"],["PASS"]],"market":[["SELL","MILK",2]]},{"farmer":["FEED"],"hands":[["FEED"],["SOUTH"],["FERTILIZE"],["WEST"],["COLLECT_FERTILIZER"],["PLANT","CARROT"],["WATER"],["HARVEST"],["WATER"],["HARVEST"],["HARVEST"]],"market":[["SELL","TOMATO",2]]},{"farmer":["CARE"],"hands":[["CARE"],["HARVEST"],["WATER"],["FEED"],["EAST"],["WATER"],["SOUTH"],["PLANT","WHEAT"],["HARVEST"],["EAST"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["HARVEST"],["SOUTH"],["SOUTH"],["CARE"],["FERTILIZE"],["SOUTH"],["WATER"],["WATER"],["EAST"],["FERTILIZE"],["NORTH"]],"market":[]},{"farmer":["HARVEST"],"hands":[["EAST"],["WATER"],["FERTILIZE"],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["HARVEST"],["NORTH"],["WATER"],["WATER"],["WATER"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["NORTH"],"hands":[["EAST"],["HARVEST"],["WATER"],["WEST"],["EAST"],["WEST"],["WEST"],["FEED"],["EAST"],["EAST"],["HARVEST"]],"market":[["SELL","TOMATO",2]]},{"farmer":["FERTILIZE"],"hands":[["EAST"],["WEST"],["SOUTH"],["WEST"],["EAST"],["WATER"],["WATER"],["NORTH"],["WATER"],["FERTILIZE"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WATER"],["NORTH"],["WATER"],["FERTILIZE"],["SOUTH"],["WEST"],["HARVEST"],["WATER"],["HARVEST"],["WATER"],["WATER"]],"market":[]},{"farmer":["EAST"],"hands":[["HARVEST"],["WATER"],["SOUTH"],["WATER"],["FERTILIZE"],["WATER"],["PLANT","WHEAT"],["HARVEST"],["SOUTH"],["SOUTH"],["EAST"]],"market":[["SELL","STRAWBERRY",2],["SELL","MILK",1]]},{"farmer":["FERTILIZE"],"hands":[["PLANT","WHEAT"],["HARVEST"],["WATER"],["SOUTH"],["WATER"],["HARVEST"],["WATER"],["PLANT","WHEAT"],["EAST"],["SOUTH"],["EAST"]],"market":[["SELL","CARROT",8],["SELL","WHEAT",8]]},{"farmer":["WATER"],"hands":[["WATER"],["NORTH"],["HARVEST"],["HARVEST"],["WEST"],["WEST"],["WEST"],["WATER"],["WATER"],["SOUTH"],["SOUTH"]],"market":[["SELL","TOMATO",2]]},{"farmer":["WEST"],"hands":[["NORTH"],["WEST"],["NORTH"],["SOUTH"],["FERTILIZE"],["WATER"],["FERTILIZE"],["NORTH"],["NORTH"],["HARVEST"],["DROP"]],"market":[["SELL","EGG",8]]},{"farmer":["WEST"],"hands":[["EAST"],["EAST"],["HARVEST"],["WATER"],["WEST"],["HARVEST"],["NORTH"],["WATER"],["WATER"],["WEST"],["NORTH"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["WEST"],"hands":[["SOUTH"],["FERTILIZE"],["EAST"],["HARVEST"],["FERTILIZE"],["NORTH"],["WATER"],["WEST"],["SOUTH"],["SOUTH"],["WEST"]],"market":[["SELL","WHEAT",8],["SELL","EGG",4]]},{"farmer":["HARVEST"],"hands":[["SOUTH"],["PASS"],["WATER"],["PASS"],["PASS"],["PASS"],["PASS"],["PASS"],["SOUTH"],["DROP"],["PASS"]],"market":[["SELL","MILK",3],["SELL","EGG",4]]},{"farmer":["HARVEST"],"hands":[],"market":[["SELL","CARROT",20],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["PLACE","MILK",3],"hands":[["HARVEST"],["HARVEST"],["PICKUP","WHEAT",2],["COLLECT_FERTILIZER"],["NORTH"],["SOUTH"],["PICKUP","FERTILIZER",3],["NORTH"],["NORTH"]],"market":[["SELL","MILK",6],["SELL","WHEAT",13],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["PLACE","MILK",3],["DROP"],["WEST"],["WEST"],["COLLECT_FERTILIZER"],["WATER"],["NORTH"],["NORTH"],["NORTH"],["EAST"],["WEST"]],"market":[["SELL","CARROT",13]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WEST"],["WEST"],["EAST"],["SOUTH"],["NORTH"],["HARVEST"],["COLLECT_FERTILIZER"],["EAST"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["NORTH"],"hands":[["EAST"],["SOUTH"],["FEED"],["WEST"],["COLLECT_FERTILIZER"],["SOUTH"],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"],["WEST"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["EAST"],["WEST"],["HARVEST"],["FERTILIZE"],["EAST"],["SOUTH"],["HARVEST"],["NORTH"],["WATER"],["EAST"],["COLLECT_FERTILIZER"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["WATER"],"hands":[["EAST"],["FERTILIZE"],["CARE"],["WATER"],["WATER"],["HARVEST"],["EAST"],["WATER"],["HARVEST"],["WATER"],["WEST"]],"market":[]},{"farmer":["NORTH"],"hands":[["EAST"],["WATER"],["WEST"],["NORTH"],["HARVEST"],["WEST"],["FERTILIZE"],["WEST"],["NORTH"],["EAST"],["WATER"]],"market":[]},{"farmer":["WATER"],"hands":[["WATER"],["WEST"],["HARVEST"],["WEST"],["EAST"],["WATER"],["WATER"],["HARVEST"],["WATER"],["NORTH"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["HARVEST"],["WATER"],["FEED"],["WATER"],["FERTILIZE"],["HARVEST"],["NORTH"],["COLLECT_FERTILIZER"],["HARVEST"],["WATER"],["WATER"]],"market":[["SELL","MILK",5],["SELL","STRAWBERRY",2]]},{"farmer":["HARVEST"],"hands":[["NORTH"],["SOUTH"],["CARE"],["NORTH"],["WATER"],["NORTH"],["HARVEST"],["NORTH"],["WEST"],["NORTH"],["HARVEST"]],"market":[["SELL","TOMATO",3]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["HARVEST"],["HARVEST"],["WEST"],["WATER"],["WEST"],["HARVEST"],["NORTH"],["WATER"],["FEED"],["WATER"],["SOUTH"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["WATER"],["SOUTH"],["HARVEST"],["NORTH"],["NORTH"],["WATER"],["HARVEST"],["COLLECT_FERTILIZER"],["HARVEST"],["WATER"]],"market":[]},{"farmer":["HARVEST"],"hands":[["NORTH"],["WEST"],["SOUTH"],["NORTH"],["FERTILIZE"],["NORTH"],["HARVEST"],["WEST"],["SOUTH"],["NORTH"],["HARVEST"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FERTILIZE"],["WATER"],["SOUTH"],["WATER"],["WATER"],["EAST"],["EAST"],["WATER"],["SOUTH"],["WEST"],["SOUTH"]],"market":[["SELL","TOMATO",2]]},{"farmer":["EAST"],"hands":[["WATER"],["HARVEST"],["WATER"],["HARVEST"],["SOUTH"],["NORTH"],["FERTILIZE"],["HARVEST"],["SOUTH"],["NORTH"],["HARVEST"]],"market":[]},{"farmer":["EAST"],"hands":[["HARVEST"],["NORTH"],["HARVEST"],["EAST"],["WEST"],["DROP"],["WATER"],["SOUTH"],["FERTILIZE"],["WATER"],["NORTH"]],"market":[["SELL","CARROT",7]]},{"farmer":["SOUTH"],"hands":[["SOUTH"],["EAST"],["SOUTH"],["NORTH"],["HARVEST"],["SOUTH"],["HARVEST"],["FEED"],["WATER"],["HARVEST"],["EAST"]],"market":[["SELL","STRAWBERRY",6],["SELL","STRAWBERRY",2]]},{"farmer":["EAST"],"hands":[["SOUTH"],["EAST"],["WEST"],["HARVEST"],["FEED"],["SOUTH"],["SOUTH"],["COLLECT_FERTILIZER"],["SOUTH"],["SOUTH"],["EAST"]],"market":[["SELL","TOMATO",2],["SELL","EGG",8]]},{"farmer":["SOUTH"],"hands":[["WEST"],["EAST"],["HARVEST"],["WATER"],["WEST"],["SOUTH"],["FERTILIZE"],["SOUTH"],["DROP"],["SOUTH"],["EAST"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["DROP"],"hands":[["WEST"],["NORTH"],["NORTH"],["SOUTH"],["HARVEST"],["WATER"],["WATER"],["EAST"],["NORTH"],["WEST"],["EAST"]],"market":[["SELL","MILK",6],["SELL","FERTILIZER",2]]},{"farmer":["NORTH"],"hands":[["WEST"],["DROP"],["SOUTH"],["WATER"],["SOUTH"],["NORTH"],["HARVEST"],["SOUTH"],["SOUTH"],["SOUTH"],["NORTH"]],"market":[["SELL","CARROT",7],["SELL","WHEAT",13]]},{"farmer":["SOUTH"],"hands":[["WEST"],["PASS"],["PASS"],["SOUTH"],["DROP"],["WEST"],["SOUTH"],["EAST"],["PASS"],["SOUTH"],["DROP"]],"market":[["SELL","TOMATO",2],["SELL","FERTILIZER",2]]},{"farmer":["WEST"],"hands":[["SOUTH"],["PASS"],["WATER"],["SOUTH"],["EAST"],["WATER"],["SOUTH"],["SOUTH"],["PASS"],["PASS"],["PASS"]],"market":[["SELL","WHEAT",13],["SELL","EGG",4]]},{"farmer":["WEST"],"hands":[],"market":[["SELL","CARROT",20],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["NORTH"],["EAST"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["EAST"],["SOUTH"],["WEST"],["NORTH"]],"market":[["SELL","CARROT",12],["SELL","WHEAT",10],["HIRE"]]},{"farmer":["WATER"],"hands":[["WATER"],["WATER"],["WEST"],["WEST"],["NORTH"],["EAST"],["WATER"],["WEST"],["NORTH"],["WEST"]],"market":[["SELL","TOMATO",6],["SELL","FERTILIZER",3]]},{"farmer":["HARVEST"],"hands":[["HARVEST"],["HARVEST"],["COLLECT_FERTILIZER"],["HARVEST"],["COLLECT_FERTILIZER"],["WATER"],["HARVEST"],["WEST"],["NORTH"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["WEST"],["NORTH"],["SOUTH"],["SOUTH"],["WEST"],["HARVEST"],["SOUTH"],["COLLECT_FERTILIZER"],["HARVEST"],["WEST"]],"market":[]},{"farmer":["HARVEST"],"hands":[["WATER"],["HARVEST"],["WEST"],["WATER"],["WATER"],["EAST"],["WATER"],["HARVEST"],["NORTH"],["NORTH"]],"market":[["SELL","MILK",5]]},{"farmer":["SOUTH"],"hands":[["HARVEST"],["COLLECT_FERTILIZER"],["HARVEST"],["HARVEST"],["HARVEST"],["WATER"],["HARVEST"],["WEST"],["HARVEST"],["WATER"]],"market":[]},{"farmer":["WATER"],"hands":[["WEST"],["NORTH"],["SOUTH"],["SOUTH"],["WEST"],["HARVEST"],["SOUTH"],["NORTH"],["COLLECT_FERTILIZER"],["HARVEST"]],"market":[]},{"farmer":["HARVEST"],"hands":[["WATER"],["WATER"],["HARVEST"],["WATER"],["NORTH"],["NORTH"],["WATER"],["NORTH"],["WEST"],["WEST"]],"market":[]},{"farmer":["EAST"],"hands":[["HARVEST"],["HARVEST"],["SOUTH"],["HARVEST"],["HARVEST"],["WATER"],["HARVEST"],["NORTH"],["SOUTH"],["HARVEST"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["EAST"],"hands":[["EAST"],["EAST"],["WATER"],["NORTH"],["COLLECT_FERTILIZER"],["HARVEST"],["NORTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["EAST"]],"market":[]},{"farmer":["EAST"],"hands":[["EAST"],["WATER"],["HARVEST"],["EAST"],["SOUTH"],["WEST"],["NORTH"],["NORTH"],["SOUTH"],["EAST"]],"market":[]},{"farmer":["DROP"],"hands":[["SOUTH"],["HARVEST"],["NORTH"],["NORTH"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["WATER"],["SOUTH"],["EAST"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["HARVEST"],"hands":[["DROP"],["SOUTH"],["NORTH"],["DROP"],["EAST"],["WEST"],["DROP"],["HARVEST"],["EAST"],["EAST"]],"market":[["SELL","STRAWBERRY",6],["SELL","MILK",2]]},{"farmer":["DROP"],"hands":[["NORTH"],["WEST"],["EAST"],["SOUTH"],["SOUTH"],["HARVEST"],["NORTH"],["SOUTH"],["SOUTH"],["SOUTH"]],"market":[["SELL","WHEAT",13],["SELL","CARROT",6]]},{"farmer":["SOUTH"],"hands":[["NORTH"],["WEST"],["EAST"],["SOUTH"],["EAST"],["SOUTH"],["NORTH"],["SOUTH"],["DROP"],["DROP"]],"market":[["SELL","MILK",3],["SELL","TOMATO",2]]},{"farmer":["SOUTH"],"hands":[["EAST"],["SOUTH"],["NORTH"],["SOUTH"],["SOUTH"],["DROP"],["NORTH"],["EAST"],["NORTH"],["NORTH"]],"market":[["SELL","WHEAT",13],["SELL","FERTILIZER",2]]},{"farmer":["SOUTH"],"hands":[["COLLECT_FERTILIZER"],["DROP"],["DROP"],["SOUTH"],["DROP"],["NORTH"],["CARE"],["EAST"],["NORTH"],["NORTH"]],"market":[["SELL","STRAWBERRY",6],["SELL","MILK",3],["SELL","CARROT",12]]},{"farmer":["WEST"],"hands":[["HARVEST"],["NORTH"],["PASS"],["PASS"],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"],["EAST"],["EAST"],["NORTH"]],"market":[["SELL","CARROT",6],["SELL","WHEAT",13],["SELL","FERTILIZER",6]]},{"farmer":["WEST"],"hands":[["SOUTH"],["NORTH"],["NORTH"],["NORTH"],["NORTH"],["SOUTH"],["NORTH"],["SOUTH"],["EAST"],["WEST"]],"market":[["SELL","WHEAT",13],["SELL","TOMATO",1]]},{"farmer":["SOUTH"],"hands":[["SOUTH"],["EAST"],["PASS"],["SOUTH"],["EAST"],["DROP"],["SOUTH"],["DROP"],["EAST"],["WEST"]],"market":[["SELL","EGG",8],["SELL","EGG",4]]},{"farmer":["PASS"],"hands":[["DROP"],["EAST"],["PASS"],["PASS"],["EAST"],["PASS"],["EAST"],["PASS"],["EAST"],["NORTH"]],"market":[["SELL","STRAWBERRY",2],["SELL","FERTILIZER",3]]},{"farmer":["PASS"],"hands":[["PASS"],["EAST"],["PASS"],["PASS"],["EAST"],["PASS"],["EAST"],["PASS"],["WATER"],["WEST"]],"market":[["SELL","WHEAT",10],["SELL","EGG",8]]}]')
_PROXY=make_agent({0:_DEMO})
def archived_proxy_agent(observation,configuration=None):
    return _PROXY(observation,configuration)
archived_proxy_agent.telemetry=_PROXY.chassis.diagnostics
agent=archived_proxy_agent
