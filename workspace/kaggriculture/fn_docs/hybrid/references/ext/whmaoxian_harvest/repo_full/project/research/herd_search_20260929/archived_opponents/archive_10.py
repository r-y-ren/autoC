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
_DEMO=json.loads('[{"farmer":["PASS"],"hands":[],"market":[["BUY_PRODUCT","WHEAT",5],["BUY_ANIMAL","COW",1]]},{"farmer":["PICKUP","COW",1],"hands":[],"market":[["SELL","WHEAT",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["BUY_ANIMAL","COW",1],["BUY_ANIMAL","SHEEP",3]]},{"farmer":["BUILD_PASTURE"],"hands":[["PICKUP","SHEEP",1],["PICKUP","SHEEP",1],["PICKUP","COW",1],["PICKUP","SHEEP",1]],"market":[["SELL","WHEAT",1]]},{"farmer":["PLACE","COW",1],"hands":[["NORTH"],["NORTH"],["NORTH"],["WEST"]],"market":[["SELL","WHEAT",1],["BUY_PRODUCT","WHEAT",1]]},{"farmer":["PICKUP","WHEAT",3],"hands":[["WEST"],["WEST"],["NORTH"],["BUILD_PASTURE"]],"market":[["SELL","WHEAT",1],["BUY_PRODUCT","WHEAT",1]]},{"farmer":["FEED"],"hands":[["BUILD_PASTURE"],["WEST"],["NORTH"],["PLACE","SHEEP",1]],"market":[["SELL","WHEAT",1],["BUY_PRODUCT","WHEAT",1]]},{"farmer":["WEST"],"hands":[["PLACE","SHEEP",1],["BUILD_PASTURE"],["PASS"],["CARE"]],"market":[["BUY_SEED","MELON",2],["BUY_PRODUCT","WHEAT",1]]},{"farmer":["FEED"],"hands":[["CARE"],["PLACE","SHEEP",1],["WEST"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["SOUTH"],["WEST"],["BUILD_PASTURE"],["WEST"]],"market":[["BUY_SEED","MELON",2]]},{"farmer":["FEED"],"hands":[["PICKUP","WHEAT",1],["NORTH"],["PLACE","COW",1],["NORTH"]],"market":[]},{"farmer":["CARE"],"hands":[["CARE"],["PLANT","MELON"],["NORTH"],["PASS"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["WATER"],["PLANT","MELON"],["NORTH"]],"market":[["BUY_SEED","MELON",2]]},{"farmer":["PLANT","MELON"],"hands":[["FEED"],["NORTH"],["WATER"],["NORTH"]],"market":[["BUY_SEED","WHEAT",2]]},{"farmer":["WATER"],"hands":[["NORTH"],["PLANT","MELON"],["WEST"],["PLANT","WHEAT"]],"market":[["SELL","WHEAT",1],["BUY_SEED","WHEAT",5],["BUY_SEED","MELON",2]]},{"farmer":["EAST"],"hands":[["WEST"],["WATER"],["PLANT","MELON"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","MELON",2]]},{"farmer":["WEST"],"hands":[["PLANT","MELON"],["NORTH"],["WATER"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PASS"],"hands":[["WATER"],["WEST"],["WEST"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PASS"],"hands":[["WEST"],["PLANT","WHEAT"],["PLANT","WHEAT"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PASS"],"hands":[["PLANT","WHEAT"],["WATER"],["WATER"],["WEST"]],"market":[["BUY_ANIMAL","COW",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["WATER"],["SOUTH"],["NORTH"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PLANT","WHEAT"],"hands":[["WEST"],["PLANT","WHEAT"],["PLANT","WHEAT"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["SOUTH"],["WATER"],["WATER"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["WEST"],["SOUTH"],["SOUTH"],["SOUTH"]],"market":[]},{"farmer":["SOUTH"],"hands":[["SOUTH"],["SOUTH"],["SOUTH"],["SOUTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[],"market":[["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["DROP"],"hands":[["NORTH"],["NORTH"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["CARE"],"hands":[["WEST"],["CARE"],["WEST"],["CARE"]],"market":[["SELL","FERTILIZER",1],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["WEST"],"hands":[["NORTH"],["WEST"],["WEST"],["PASS"]],"market":[]},{"farmer":["CARE"],"hands":[["CARE"],["CARE"],["WEST"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["CARE"],["SOUTH"]],"market":[["BUY_SEED","MELON",2]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["SOUTH"],["EAST"],["EAST"],["PLACE","FERTILIZER",1000]],"market":[["BUY_SEED","MELON",2],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["EAST"],"hands":[["SOUTH"],["COLLECT_FERTILIZER"],["WEST"],["PICKUP","WHEAT",2]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","MELON",2]]},{"farmer":["EAST"],"hands":[["PLACE","FERTILIZER",1000],["EAST"],["PASS"],["NORTH"]],"market":[["BUY_SEED","MELON",2],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["PLACE","FERTILIZER",1000],"hands":[["PICKUP","WHEAT",2],["PLACE","FERTILIZER",1000],["PASS"],["FEED"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","MELON",2]]},{"farmer":["PASS"],"hands":[["FEED"],["PASS"],["PASS"],["NORTH"]],"market":[["SELL","FERTILIZER",2],["BUY_PRODUCT","WHEAT",2],["BUY_SEED","MELON",2]]},{"farmer":["PICKUP","WHEAT",2],"hands":[["WEST"],["PICKUP","WHEAT",2],["PASS"],["FEED"]],"market":[["BUY_SEED","MELON",2],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["WEST"],"hands":[["FEED"],["PASS"],["PASS"],["NORTH"]],"market":[["BUY_SEED","MELON",4],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["WEST"],"hands":[["NORTH"],["PASS"],["PASS"],["NORTH"]],"market":[]},{"farmer":["FEED"],"hands":[["PLANT","MELON"],["PASS"],["WEST"],["PLANT","MELON"]],"market":[]},{"farmer":["NORTH"],"hands":[["WEST"],["PASS"],["EAST"],["WATER"]],"market":[["BUY_SEED","MELON",1]]},{"farmer":["PLANT","MELON"],"hands":[["PLANT","MELON"],["PASS"],["PASS"],["WEST"]],"market":[]},{"farmer":["SOUTH"],"hands":[["WEST"],["PASS"],["PASS"],["PLANT","MELON"]],"market":[]},{"farmer":["PASS"],"hands":[["WEST"],["PASS"],["NORTH"],["WATER"]],"market":[]},{"farmer":["PASS"],"hands":[["PLANT","WHEAT"],["PASS"],["WATER"],["SOUTH"]],"market":[]},{"farmer":["PASS"],"hands":[["WATER"],["PASS"],["EAST"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["SOUTH"],["PASS"],["WATER"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["SOUTH"],["PASS"],["SOUTH"],["SOUTH"]],"market":[]},{"farmer":["SOUTH"],"hands":[["SOUTH"],["SOUTH"],["SOUTH"],["SOUTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[],"market":[["SELL","WHEAT",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["BUY_PRODUCT","WHEAT",1]]},{"farmer":["DROP"],"hands":[["NORTH"],["NORTH"],["WEST"],["NORTH"],["NORTH"],["WEST"]],"market":[]},{"farmer":["CARE"],"hands":[["WEST"],["CARE"],["WEST"],["CARE"],["NORTH"],["NORTH"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["PASS"],"hands":[["NORTH"],["WEST"],["WEST"],["NORTH"],["WEST"],["WEST"]],"market":[]},{"farmer":["PASS"],"hands":[["CARE"],["CARE"],["NORTH"],["CARE"],["NORTH"],["WEST"]],"market":[["BUY_PRODUCT","WHEAT",2]]},{"farmer":["PICKUP","WHEAT",2],"hands":[["COLLECT_FERTILIZER"],["WEST"],["CARE"],["NORTH"],["WATER"],["WATER"]],"market":[]},{"farmer":["WEST"],"hands":[["SOUTH"],["COLLECT_FERTILIZER"],["EAST"],["WEST"],["NORTH"],["NORTH"]],"market":[["BUY_PRODUCT","WHEAT",2]]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["EAST"],["COLLECT_FERTILIZER"],["WATER"],["WEST"],["WATER"]],"market":[["BUY_SEED","MELON",1]]},{"farmer":["WEST"],"hands":[["SOUTH"],["EAST"],["EAST"],["WEST"],["WEST"],["NORTH"]],"market":[["BUY_SEED","MELON",1]]},{"farmer":["FEED"],"hands":[["PLACE","FERTILIZER",1000],["PLACE","FERTILIZER",1000],["PLACE","FERTILIZER",1000],["WATER"],["WATER"],["WATER"]],"market":[["BUY_SEED","MELON",1]]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",1],["PASS"],["WEST"],["WEST"],["WEST"],["WEST"]],"market":[["SELL","FERTILIZER",4],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WEST"],"hands":[["NORTH"],["PASS"],["WEST"],["WATER"],["WATER"],["SOUTH"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WATER"],"hands":[["FEED"],["WEST"],["NORTH"],["NORTH"],["HARVEST"],["NORTH"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["HARVEST"],"hands":[["NORTH"],["WEST"],["NORTH"],["PASS"],["WEST"],["WATER"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PLANT","STRAWBERRY"],"hands":[["WEST"],["PASS"],["WATER"],["PASS"],["WATER"],["NORTH"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WATER"],"hands":[["WATER"],["PASS"],["HARVEST"],["PASS"],["HARVEST"],["WATER"]],"market":[]},{"farmer":["PASS"],"hands":[["WEST"],["PASS"],["PASS"],["PASS"],["PLANT","STRAWBERRY"],["EAST"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PASS"],"hands":[["NORTH"],["PASS"],["PASS"],["PASS"],["WATER"],["HARVEST"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PASS"],"hands":[["NORTH"],["PASS"],["PASS"],["PASS"],["SOUTH"],["PLANT","STRAWBERRY"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"],["EAST"],["WATER"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"],["WEST"],["WEST"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"],["HARVEST"],["HARVEST"]],"market":[]},{"farmer":["SOUTH"],"hands":[["SOUTH"],["PASS"],["PASS"],["PASS"],["PLANT","STRAWBERRY"],["EAST"]],"market":[]},{"farmer":["SOUTH"],"hands":[["SOUTH"],["EAST"],["SOUTH"],["SOUTH"],["WATER"],["SOUTH"]],"market":[]},{"farmer":["PICKUP","WHEAT",3],"hands":[],"market":[["SELL","WHEAT",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["WEST"],["NORTH"],["WEST"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"]],"market":[["SELL","WHEAT",2],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["CARE"],"hands":[["CARE"],["CARE"],["WEST"],["PLACE","FERTILIZER",1000],["NORTH"],["WEST"]],"market":[["SELL","WHEAT",2],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WEST"],"hands":[["NORTH"],["WEST"],["WEST"],["NORTH"],["NORTH"],["WEST"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["CARE"],"hands":[["CARE"],["COLLECT_FERTILIZER"],["NORTH"],["CARE"],["NORTH"],["WEST"]],"market":[]},{"farmer":["FEED"],"hands":[["NORTH"],["EAST"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["EAST"],"hands":[["COLLECT_FERTILIZER"],["PLACE","FERTILIZER",1000],["EAST"],["WEST"],["WATER"],["WEST"]],"market":[]},{"farmer":["FEED"],"hands":[["SOUTH"],["PICKUP","WHEAT",4],["EAST"],["WEST"],["WEST"],["WATER"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["EAST"],"hands":[["COLLECT_FERTILIZER"],["FEED"],["PLACE","FERTILIZER",1000],["PLANT","STRAWBERRY"],["WATER"],["HARVEST"]],"market":[]},{"farmer":["WEST"],"hands":[["SOUTH"],["NORTH"],["WEST"],["WATER"],["WEST"],["PLANT","STRAWBERRY"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PASS"],"hands":[["PLACE","FERTILIZER",1000],["NORTH"],["WEST"],["NORTH"],["WATER"],["WATER"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PASS"],"hands":[["PASS"],["FEED"],["PASS"],["WATER"],["HARVEST"],["NORTH"]],"market":[["SELL","FERTILIZER",2],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PASS"],"hands":[["PASS"],["CARE"],["PASS"],["HARVEST"],["PLANT","STRAWBERRY"],["WATER"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PASS"],"hands":[["PASS"],["SOUTH"],["PASS"],["PLANT","STRAWBERRY"],["WATER"],["HARVEST"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PASS"],"hands":[["PASS"],["FEED"],["PASS"],["WATER"],["WEST"],["PLANT","STRAWBERRY"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["NORTH"],["PASS"],["PLANT","STRAWBERRY"],["WATER"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["EAST"],["PASS"],["WATER"],["SOUTH"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"],["EAST"],["SOUTH"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["SOUTH"],["EAST"],["PASS"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["SOUTH"],["SOUTH"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["WATER"],["WATER"],["WEST"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["WEST"],["SOUTH"],["SOUTH"],["PASS"]],"market":[]},{"farmer":["SOUTH"],"hands":[["PASS"],["PASS"],["WEST"],["PASS"],["SOUTH"],["PASS"]],"market":[]},{"farmer":["SOUTH"],"hands":[["SOUTH"],["SOUTH"],["SOUTH"],["SOUTH"],["SOUTH"],["WATER"]],"market":[]},{"farmer":["PICKUP","WHEAT",4],"hands":[],"market":[["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",4],["NORTH"],["SOUTH"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["CARE"],"hands":[["NORTH"],["CARE"],["SOUTH"],["PLACE","FERTILIZER",1000]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["NORTH"],["SOUTH"],["NORTH"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["CARE"],"hands":[["WEST"],["NORTH"],["EAST"],["NORTH"]],"market":[]},{"farmer":["FEED"],"hands":[["CARE"],["NORTH"],["SOUTH"],["NORTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["WATER"],["WEST"],["PASS"]],"market":[]},{"farmer":["WEST"],"hands":[["SOUTH"],["WEST"],["NORTH"],["WEST"]],"market":[]},{"farmer":["WATER"],"hands":[["CARE"],["WATER"],["WEST"],["WEST"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["EAST"],"hands":[["COLLECT_FERTILIZER"],["SOUTH"],["NORTH"],["WEST"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["EAST"],"hands":[["SOUTH"],["WATER"],["SOUTH"],["WATER"]],"market":[]},{"farmer":["FEED"],"hands":[["PLACE","FERTILIZER",1000],["WEST"],["NORTH"],["WEST"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FEED"],["WEST"],["NORTH"],["WATER"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["EAST"],"hands":[["NORTH"],["WATER"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["PLACE","FERTILIZER",1000],"hands":[["FEED"],["SOUTH"],["NORTH"],["WATER"]],"market":[]},{"farmer":["PASS"],"hands":[["NORTH"],["WATER"],["PASS"],["SOUTH"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["PASS"],"hands":[["FEED"],["SOUTH"],["PASS"],["SOUTH"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["SOUTH"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["WEST"],["PASS"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"]],"market":[]},{"farmer":["SOUTH"],"hands":[["SOUTH"],["PASS"],["SOUTH"],["SOUTH"]],"market":[]},{"farmer":["PICKUP","WHEAT",3],"hands":[],"market":[["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["BUY_PRODUCT","WHEAT",2]]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",4],["NORTH"],["WEST"],["CARE"],["WEST"],["NORTH"]],"market":[]},{"farmer":["CARE"],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["WEST"],["PASS"],["NORTH"],["WEST"]],"market":[["SELL","WHEAT",2]]},{"farmer":["WEST"],"hands":[["WEST"],["PLACE","FERTILIZER",1000],["WEST"],["PASS"],["NORTH"],["WEST"]],"market":[]},{"farmer":["CARE"],"hands":[["CARE"],["PASS"],["NORTH"],["PASS"],["NORTH"],["WEST"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["FEED"],"hands":[["NORTH"],["NORTH"],["EAST"],["PASS"],["NORTH"],["WEST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["CARE"],["WEST"],["COLLECT_FERTILIZER"],["PASS"],["WATER"],["WATER"]],"market":[]},{"farmer":["EAST"],"hands":[["COLLECT_FERTILIZER"],["SOUTH"],["EAST"],["PASS"],["WEST"],["NORTH"]],"market":[]},{"farmer":["EAST"],"hands":[["FEED"],["EAST"],["PLACE","FERTILIZER",1000],["PASS"],["WATER"],["WATER"]],"market":[]},{"farmer":["PLACE","FERTILIZER",1000],"hands":[["SOUTH"],["PASS"],["PASS"],["PASS"],["WEST"],["NORTH"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["FEED"],"hands":[["SOUTH"],["PASS"],["PASS"],["PASS"],["WATER"],["WATER"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["PASS"],"hands":[["PLACE","FERTILIZER",1000],["PASS"],["PASS"],["PASS"],["SOUTH"],["EAST"]],"market":[]},{"farmer":["WEST"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"],["WATER"],["EAST"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["FEED"],"hands":[["NORTH"],["PASS"],["PASS"],["PASS"],["WEST"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["COLLECT_FERTILIZER"],["PASS"],["PASS"],["PASS"],["NORTH"],["SOUTH"]],"market":[]},{"farmer":["PASS"],"hands":[["SOUTH"],["PASS"],["PASS"],["PASS"],["WATER"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PLACE","FERTILIZER",1000],["PASS"],["PASS"],["PASS"],["SOUTH"],["PASS"]],"market":[]},{"farmer":["WATER"],"hands":[["NORTH"],["PASS"],["PASS"],["PASS"],["SOUTH"],["WATER"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["PASS"],"hands":[["FEED"],["PASS"],["PASS"],["PASS"],["SOUTH"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"],["SOUTH"],["PASS"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"],["SOUTH"],["WEST"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"],["SOUTH"],["SOUTH"]],"market":[]},{"farmer":["SOUTH"],"hands":[["PASS"],["PASS"],["PASS"],["PASS"],["SOUTH"],["SOUTH"]],"market":[]},{"farmer":["SOUTH"],"hands":[["SOUTH"],["PASS"],["PASS"],["EAST"],["SOUTH"],["SOUTH"]],"market":[]},{"farmer":["NORTH"],"hands":[],"market":[["SELL","WHEAT",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["BUY_PRODUCT","WHEAT",4]]},{"farmer":["HARVEST"],"hands":[["WEST"],["PICKUP","WHEAT",1],["PICKUP","WHEAT",1],["NORTH"],["NORTH"],["WEST"],["NORTH"],["NORTH"]],"market":[["SELL","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["WEST"],["NORTH"],["NORTH"],["WEST"],["NORTH"],["WEST"],["WEST"],["WEST"]],"market":[]},{"farmer":["DROP"],"hands":[["HARVEST"],["NORTH"],["FEED"],["NORTH"],["WEST"],["HARVEST"],["WEST"],["WEST"]],"market":[["SELL","WOOL",6]]},{"farmer":["PICKUP","WHEAT",3],"hands":[["EAST"],["WEST"],["CARE"],["COLLECT_FERTILIZER"],["WATER"],["EAST"],["WEST"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["WEST"],"hands":[["EAST"],["FEED"],["COLLECT_FERTILIZER"],["SOUTH"],["NORTH"],["DROP"],["WATER"],["EAST"]],"market":[["SELL","WOOL",6],["BUY_LAND"]]},{"farmer":["FEED"],"hands":[["DROP"],["CARE"],["PLACE","FERTILIZER",1000],["PLACE","FERTILIZER",1000],["WATER"],["NORTH"],["NORTH"],["PLACE","FERTILIZER",1000]],"market":[["SELL","WOOL",6],["BUY_ANIMAL","COW",1],["BUY_SEED","STRAWBERRY",8]]},{"farmer":["CARE"],"hands":[["PICKUP","COW",1],["COLLECT_FERTILIZER"],["PICKUP","COW",1],["PICKUP","COW",1],["EAST"],["NORTH"],["WATER"],["PICKUP","COW",1]],"market":[["SELL","FERTILIZER",3]]},{"farmer":["WEST"],"hands":[["EAST"],["SOUTH"],["EAST"],["PASS"],["EAST"],["NORTH"],["NORTH"],["NORTH"]],"market":[["BUY_ANIMAL","GOOSE",1],["BUY_ANIMAL","COW",2]]},{"farmer":["FEED"],"hands":[["BUILD_PASTURE"],["SOUTH"],["PICKUP","COW",1],["PICKUP","COW",1],["PLANT","STRAWBERRY"],["WATER"],["WATER"],["SOUTH"]],"market":[]},{"farmer":["CARE"],"hands":[["PLACE","COW",1],["PLACE","FERTILIZER",1000],["PLACE","COW",1],["EAST"],["WATER"],["EAST"],["NORTH"],["PICKUP","GOOSE",1]],"market":[["BUY_ANIMAL","COW",1],["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["PICKUP","COW",1],["PICKUP","COW",1],["PICKUP","COW",1],["EAST"],["EAST"],["NORTH"],["WATER"],["EAST"]],"market":[["SELL","FERTILIZER",1],["BUY_ANIMAL","GOOSE",1],["BUY_ANIMAL","COW",1]]},{"farmer":["EAST"],"hands":[["NORTH"],["EAST"],["PICKUP","COW",1],["BUILD_PASTURE"],["PLANT","STRAWBERRY"],["PLANT","STRAWBERRY"],["WEST"],["EAST"]],"market":[["BUY_ANIMAL","COW",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["EAST"],"hands":[["BUILD_PASTURE"],["NORTH"],["NORTH"],["PLACE","COW",1],["WATER"],["WATER"],["WATER"],["EAST"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PLACE","FERTILIZER",1000],"hands":[["EAST"],["PLACE","COW",1],["PLACE","COW",1],["NORTH"],["EAST"],["EAST"],["NORTH"],["BUILD_COOP"]],"market":[["BUY_ANIMAL","COW",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["NORTH"],"hands":[["BUILD_PASTURE"],["SOUTH"],["NORTH"],["EAST"],["PLANT","STRAWBERRY"],["EAST"],["WATER"],["PLACE","GOOSE",1]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["FEED"],"hands":[["PLACE","COW",1],["PICKUP","GOOSE",1],["BUILD_PASTURE"],["PLANT","STRAWBERRY"],["WATER"],["PLANT","STRAWBERRY"],["EAST"],["EAST"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["CARE"],"hands":[["NORTH"],["EAST"],["PLACE","COW",1],["WATER"],["EAST"],["WATER"],["WATER"],["EAST"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["SOUTH"],"hands":[["EAST"],["EAST"],["NORTH"],["NORTH"],["PLANT","STRAWBERRY"],["EAST"],["EAST"],["NORTH"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PASS"],"hands":[["PLANT","WHEAT"],["EAST"],["NORTH"],["EAST"],["WATER"],["PLANT","STRAWBERRY"],["EAST"],["PLANT","STRAWBERRY"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PASS"],"hands":[["WATER"],["BUILD_COOP"],["EAST"],["PLANT","STRAWBERRY"],["EAST"],["WATER"],["WEST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PASS"],"hands":[["WEST"],["PLACE","GOOSE",1],["PLANT","STRAWBERRY"],["WATER"],["PLANT","WHEAT"],["EAST"],["WATER"],["SOUTH"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PASS"],"hands":[["SOUTH"],["PASS"],["PASS"],["SOUTH"],["WATER"],["PASS"],["SOUTH"],["WEST"]],"market":[]},{"farmer":["PASS"],"hands":[["SOUTH"],["PASS"],["SOUTH"],["SOUTH"],["SOUTH"],["SOUTH"],["WATER"],["PASS"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[],"market":[["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["PLACE","FERTILIZER",1000],"hands":[["CARE"],["NORTH"],["NORTH"],["NORTH"],["COLLECT_FERTILIZER"]],"market":[["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["CARE"],"hands":[["NORTH"],["CARE"],["EAST"],["CARE"],["PLACE","FERTILIZER",1000]],"market":[["SELL","FERTILIZER",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"],["NORTH"],["NORTH"],["NORTH"]],"market":[["SELL","FERTILIZER",1],["BUY_PRODUCT","WHEAT",4]]},{"farmer":["NORTH"],"hands":[["SOUTH"],["COLLECT_FERTILIZER"],["WEST"],["SOUTH"],["NORTH"],["WEST"],["EAST"],["NORTH"],["PICKUP","WHEAT",3]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["PLACE","FERTILIZER",1000],["EAST"],["PLACE","FERTILIZER",1000],["PLACE","FERTILIZER",1000],["COLLECT_FERTILIZER"],["WEST"],["EAST"],["EAST"],["FEED"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["SOUTH"],"hands":[["NORTH"],["PLACE","FERTILIZER",1000],["EAST"],["NORTH"],["SOUTH"],["WEST"],["COLLECT_FERTILIZER"],["BUILD_PASTURE"],["WEST"]],"market":[["SELL","FERTILIZER",2],["BUY_PRODUCT","WHEAT",4]]},{"farmer":["SOUTH"],"hands":[["EAST"],["PICKUP","WHEAT",4],["EAST"],["NORTH"],["SOUTH"],["WATER"],["WEST"],["SOUTH"],["FEED"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["PLACE","FERTILIZER",1000],"hands":[["COLLECT_FERTILIZER"],["NORTH"],["EAST"],["NORTH"],["PLACE","FERTILIZER",1000],["WEST"],["WEST"],["COLLECT_FERTILIZER"],["CARE"]],"market":[["BUY_PRODUCT","WHEAT",3]]},{"farmer":["WEST"],"hands":[["SOUTH"],["NORTH"],["COLLECT_FERTILIZER"],["WATER"],["PICKUP","WHEAT",3],["WATER"],["PLACE","FERTILIZER",1000],["NORTH"],["WEST"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["WEST"],"hands":[["WEST"],["FEED"],["WEST"],["NORTH"],["EAST"],["NORTH"],["PASS"],["NORTH"],["COLLECT_FERTILIZER"]],"market":[["SELL","FERTILIZER",2],["BUY_PRODUCT","WHEAT",3]]},{"farmer":["CARE"],"hands":[["PLACE","FERTILIZER",1000],["CARE"],["WEST"],["WATER"],["FEED"],["WATER"],["PICKUP","WHEAT",3],["NORTH"],["EAST"]],"market":[]},{"farmer":["NORTH"],"hands":[["PASS"],["EAST"],["WEST"],["WEST"],["CARE"],["NORTH"],["FEED"],["PLANT","STRAWBERRY"],["EAST"]],"market":[["SELL","FERTILIZER",1],["BUY_PRODUCT","WHEAT",3],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WATER"],"hands":[["PICKUP","WHEAT",3],["FEED"],["PLACE","FERTILIZER",1000],["WATER"],["EAST"],["WATER"],["NORTH"],["PLANT","STRAWBERRY"],["PLACE","FERTILIZER",1000]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["EAST"],"hands":[["NORTH"],["CARE"],["PASS"],["SOUTH"],["FEED"],["EAST"],["FEED"],["WATER"],["PASS"]],"market":[["SELL","FERTILIZER",2],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WATER"],"hands":[["CARE"],["EAST"],["PASS"],["WATER"],["CARE"],["WATER"],["CARE"],["EAST"],["PASS"]],"market":[["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WEST"],"hands":[["EAST"],["EAST"],["PASS"],["SOUTH"],["EAST"],["SOUTH"],["SOUTH"],["EAST"],["PASS"]],"market":[]},{"farmer":["NORTH"],"hands":[["FEED"],["EAST"],["PASS"],["WATER"],["FEED"],["WATER"],["WEST"],["EAST"],["PASS"]],"market":[]},{"farmer":["WATER"],"hands":[["CARE"],["EAST"],["EAST"],["WEST"],["CARE"],["PASS"],["WEST"],["PLANT","STRAWBERRY"],["PASS"]],"market":[]},{"farmer":["NORTH"],"hands":[["WEST"],["PLANT","STRAWBERRY"],["EAST"],["NORTH"],["EAST"],["PASS"],["WEST"],["WATER"],["PASS"]],"market":[]},{"farmer":["WATER"],"hands":[["WEST"],["WATER"],["EAST"],["NORTH"],["PLANT","WHEAT"],["PASS"],["FEED"],["SOUTH"],["PASS"]],"market":[]},{"farmer":["WEST"],"hands":[["FEED"],["WEST"],["NORTH"],["WATER"],["PLANT","WHEAT"],["PASS"],["PASS"],["WEST"],["PASS"]],"market":[]},{"farmer":["WEST"],"hands":[["PASS"],["PASS"],["PLANT","WHEAT"],["WEST"],["PLANT","WHEAT"],["SOUTH"],["PASS"],["NORTH"],["PASS"]],"market":[]},{"farmer":["WATER"],"hands":[["SOUTH"],["SOUTH"],["SOUTH"],["WATER"],["SOUTH"],["SOUTH"],["SOUTH"],["WATER"],["PASS"]],"market":[]},{"farmer":["HARVEST"],"hands":[],"market":[["SELL","WHEAT",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["PLACE","MILK",1000],"hands":[["CARE"],["NORTH"],["PICKUP","WHEAT",1],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"],["NORTH"]],"market":[["SELL","MILK",6],["HIRE"],["BUY_PRODUCT","WHEAT",13]]},{"farmer":["PICKUP","WHEAT",4],"hands":[["NORTH"],["PICKUP","WHEAT",4],["NORTH"],["NORTH"],["PLACE","FERTILIZER",1000],["WEST"],["NORTH"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["EAST"],["HARVEST"],["PICKUP","WHEAT",3],["WEST"],["NORTH"],["WEST"],["NORTH"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["FEED"],"hands":[["EAST"],["FEED"],["COLLECT_FERTILIZER"],["SOUTH"],["EAST"],["WEST"],["EAST"],["WATER"],["WEST"]],"market":[]},{"farmer":["CARE"],"hands":[["COLLECT_FERTILIZER"],["CARE"],["WEST"],["SOUTH"],["EAST"],["WATER"],["EAST"],["NORTH"],["WATER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["SOUTH"],["WEST"],["PLACE","FERTILIZER",1000],["DROP"],["FEED"],["NORTH"],["WATER"],["WATER"],["WEST"]],"market":[["SELL","MILK",6],["BUY_ANIMAL","COW",1]]},{"farmer":["NORTH"],"hands":[["WEST"],["FEED"],["EAST"],["PICKUP","COW",1],["CARE"],["WATER"],["HARVEST"],["NORTH"],["WATER"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["FEED"],"hands":[["DROP"],["CARE"],["EAST"],["EAST"],["COLLECT_FERTILIZER"],["NORTH"],["PLANT","STRAWBERRY"],["WATER"],["NORTH"]],"market":[["SELL","FERTILIZER",2]]},{"farmer":["CARE"],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["EAST"],["EAST"],["WEST"],["WATER"],["WATER"],["EAST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["EAST"],["FEED"],["NORTH"],["WEST"],["NORTH"],["EAST"],["WATER"],["NORTH"]],"market":[]},{"farmer":["SOUTH"],"hands":[["COLLECT_FERTILIZER"],["EAST"],["CARE"],["NORTH"],["PLACE","FERTILIZER",1000],["WATER"],["WATER"],["SOUTH"],["WATER"]],"market":[]},{"farmer":["SOUTH"],"hands":[["SOUTH"],["PLACE","FERTILIZER",1000],["COLLECT_FERTILIZER"],["PLACE","COW",1],["EAST"],["NORTH"],["NORTH"],["WATER"],["NORTH"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","WHEAT",1]]},{"farmer":["PLACE","FERTILIZER",1000],"hands":[["SOUTH"],["FEED"],["EAST"],["NORTH"],["EAST"],["WATER"],["WATER"],["EAST"],["WATER"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["CARE"],"hands":[["PLACE","FERTILIZER",1000],["CARE"],["PLANT","WHEAT"],["WATER"],["NORTH"],["WEST"],["EAST"],["WATER"],["EAST"]],"market":[["SELL","FERTILIZER",2],["BUY_SEED","WHEAT",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WEST"],"hands":[["WEST"],["COLLECT_FERTILIZER"],["WATER"],["EAST"],["WATER"],["WATER"],["WATER"],["NORTH"],["EAST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["PASS"],["PLACE","FERTILIZER",1000],["NORTH"],["WATER"],["EAST"],["SOUTH"],["HARVEST"],["WATER"],["EAST"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["EAST"],"hands":[["PASS"],["PASS"],["WATER"],["NORTH"],["PLANT","WHEAT"],["WATER"],["PLANT","WHEAT"],["EAST"],["EAST"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["PLACE","FERTILIZER",1000],"hands":[["PASS"],["PASS"],["NORTH"],["WATER"],["WATER"],["SOUTH"],["WATER"],["WATER"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["WATER"],["EAST"],["WEST"],["WATER"],["NORTH"],["SOUTH"],["SOUTH"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["NORTH"],["WATER"],["WEST"],["SOUTH"],["WATER"],["SOUTH"],["SOUTH"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["SOUTH"],["SOUTH"],["SOUTH"],["WATER"],["SOUTH"],["SOUTH"],["SOUTH"]],"market":[]},{"farmer":["PASS"],"hands":[["PASS"],["PASS"],["SOUTH"],["SOUTH"],["PASS"],["SOUTH"],["SOUTH"],["SOUTH"],["SOUTH"]],"market":[]},{"farmer":["SOUTH"],"hands":[["PASS"],["SOUTH"],["SOUTH"],["SOUTH"],["SOUTH"],["WATER"],["SOUTH"],["SOUTH"],["SOUTH"]],"market":[]},{"farmer":["NORTH"],"hands":[],"market":[["SELL","FERTILIZER",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["BUY_ANIMAL","COW",1]]},{"farmer":["HARVEST"],"hands":[["WEST"],["PICKUP","COW",1],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["NORTH"],["WEST"],["NORTH"],["PICKUP","WHEAT",3]],"market":[["BUY_PRODUCT","WHEAT",5],["HIRE"],["HIRE"]]},{"farmer":["SOUTH"],"hands":[["HARVEST"],["PASS"],["NORTH"],["NORTH"],["NORTH"],["WEST"],["WEST"],["NORTH"],["PICKUP","WHEAT",3],["NORTH"]],"market":[]},{"farmer":["PLACE","WOOL",1000],"hands":[["EAST"],["PASS"],["WEST"],["EAST"],["WEST"],["WEST"],["WEST"],["EAST"],["CARE"],["NORTH"]],"market":[["SELL","WOOL",4],["BUY_LAND"]]},{"farmer":["PICKUP","WHEAT",3],"hands":[["DROP"],["SOUTH"],["FEED"],["FEED"],["WATER"],["HARVEST"],["WEST"],["EAST"],["COLLECT_FERTILIZER"],["WEST"]],"market":[["SELL","WOOL",4]]},{"farmer":["NORTH"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["CARE"],["CARE"],["NORTH"],["EAST"],["WATER"],["FEED"],["PLACE","FERTILIZER",1000],["WATER"]],"market":[]},{"farmer":["FEED"],"hands":[["PLACE","FERTILIZER",1000],["WEST"],["WEST"],["COLLECT_FERTILIZER"],["WATER"],["EAST"],["WEST"],["CARE"],["FEED"],["WEST"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["CARE"],"hands":[["PICKUP","WHEAT",2],["BUILD_PASTURE"],["FEED"],["NORTH"],["NORTH"],["DROP"],["WATER"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"]],"market":[["SELL","WOOL",4],["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FEED"],["PLACE","COW",1],["CARE"],["FEED"],["WATER"],["WEST"],["SOUTH"],["EAST"],["CARE"],["WEST"]],"market":[["BUY_ANIMAL","COW",1]]},{"farmer":["NORTH"],"hands":[["CARE"],["SOUTH"],["COLLECT_FERTILIZER"],["CARE"],["EAST"],["COLLECT_FERTILIZER"],["PLANT","WHEAT"],["FEED"],["COLLECT_FERTILIZER"],["WATER"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["PICKUP","COW",1],["PLANT","WHEAT"],["SOUTH"],["COLLECT_FERTILIZER"],["WATER"],["EAST"],["WATER"],["CARE"],["FEED"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["SOUTH"],["WATER"],["WEST"],["NORTH"],["SOUTH"],["PLACE","FERTILIZER",1000],["SOUTH"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"]],"market":[["BUY_ANIMAL","GOOSE",1],["BUY_ANIMAL","COW",1],["BUY_SEED","WHEAT",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["BUILD_PASTURE"],["SOUTH"],["PLANT","WHEAT"],["FEED"],["WATER"],["PICKUP","GOOSE",1],["PLANT","WHEAT"],["NORTH"],["FEED"],["NORTH"]],"market":[["SELL","FERTILIZER",1],["BUY_SEED","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["PLACE","COW",1],["PLANT","WHEAT"],["WATER"],["CARE"],["WEST"],["SOUTH"],["WATER"],["NORTH"],["CARE"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["SOUTH"],"hands":[["PICKUP","GOOSE",1],["WATER"],["SOUTH"],["COLLECT_FERTILIZER"],["WEST"],["SOUTH"],["SOUTH"],["WATER"],["COLLECT_FERTILIZER"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PLACE","FERTILIZER",1000],"hands":[["WEST"],["SOUTH"],["PLANT","WHEAT"],["NORTH"],["WATER"],["BUILD_COOP"],["PLANT","WHEAT"],["EAST"],["SOUTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["SOUTH"],"hands":[["SOUTH"],["PLANT","STRAWBERRY"],["WATER"],["WATER"],["SOUTH"],["PLACE","GOOSE",1],["WATER"],["WATER"],["SOUTH"],["WEST"]],"market":[["SELL","FERTILIZER",2],["BUY_SEED","WHEAT",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WEST"],"hands":[["WEST"],["WATER"],["SOUTH"],["NORTH"],["WATER"],["SOUTH"],["SOUTH"],["NORTH"],["PLACE","FERTILIZER",1000],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WEST"],"hands":[["PLANT","WHEAT"],["SOUTH"],["PLANT","WHEAT"],["WATER"],["WEST"],["SOUTH"],["PLANT","STRAWBERRY"],["NORTH"],["NORTH"],["SOUTH"]],"market":[["SELL","FERTILIZER",2],["BUY_SEED","WHEAT",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PLANT","WHEAT"],"hands":[["WATER"],["PLANT","STRAWBERRY"],["WATER"],["EAST"],["WEST"],["PLANT","STRAWBERRY"],["WATER"],["WATER"],["NORTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["SOUTH"],["WATER"],["SOUTH"],["WATER"],["WATER"],["WATER"],["SOUTH"],["WEST"],["NORTH"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["PLANT","WHEAT"],["WEST"],["PLANT","STRAWBERRY"],["SOUTH"],["SOUTH"],["SOUTH"],["PLANT","WHEAT"],["WATER"],["WATER"],["EAST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["WATER"],["PLANT","STRAWBERRY"],["WATER"],["WATER"],["WATER"],["PLANT","WHEAT"],["WATER"],["SOUTH"],["NORTH"],["EAST"]],"market":[]},{"farmer":["SOUTH"],"hands":[["SOUTH"],["PASS"],["NORTH"],["SOUTH"],["SOUTH"],["WATER"],["NORTH"],["WATER"],["WATER"],["WATER"]],"market":[]},{"farmer":["HARVEST"],"hands":[],"market":[["SELL","FERTILIZER",6],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["BUY_PRODUCT","WHEAT",4]]},{"farmer":["PLACE","MILK",1000],"hands":[["PICKUP","WHEAT",3],["PICKUP","WHEAT",2],["PICKUP","WHEAT",2],["WEST"],["PICKUP","WHEAT",2],["NORTH"],["NORTH"],["NORTH"]],"market":[["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["BUY_PRODUCT","WHEAT",13]]},{"farmer":["PICKUP","WHEAT",1],"hands":[["FEED"],["FEED"],["NORTH"],["WEST"],["NORTH"],["WEST"],["NORTH"],["NORTH"],["NORTH"],["NORTH"],["NORTH"],["NORTH"]],"market":[["BUY_PRODUCT","WHEAT",16]]},{"farmer":["PICKUP","WHEAT",1],"hands":[["CARE"],["CARE"],["EAST"],["WEST"],["FEED"],["WEST"],["NORTH"],["WEST"],["NORTH"],["EAST"],["WEST"],["NORTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FEED"],["WATER"],["CARE"],["WEST"],["WEST"],["WATER"],["WEST"],["EAST"],["WATER"],["NORTH"]],"market":[]},{"farmer":["PLACE","FERTILIZER",1000],"hands":[["NORTH"],["SOUTH"],["CARE"],["NORTH"],["COLLECT_FERTILIZER"],["HARVEST"],["NORTH"],["HARVEST"],["WEST"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["CARE"],"hands":[["EAST"],["FEED"],["COLLECT_FERTILIZER"],["WATER"],["NORTH"],["EAST"],["WATER"],["SOUTH"],["WATER"],["HARVEST"],["NORTH"],["WEST"]],"market":[["BUY_PRODUCT","WHEAT",4],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PICKUP","WHEAT",2],"hands":[["FEED"],["CARE"],["EAST"],["HARVEST"],["COLLECT_FERTILIZER"],["EAST"],["HARVEST"],["SOUTH"],["WEST"],["EAST"],["WATER"],["WATER"]],"market":[["BUY_PRODUCT","WHEAT",3]]},{"farmer":["NORTH"],"hands":[["CARE"],["COLLECT_FERTILIZER"],["FEED"],["SOUTH"],["EAST"],["EAST"],["SOUTH"],["EAST"],["NORTH"],["COLLECT_FERTILIZER"],["HARVEST"],["HARVEST"]],"market":[["BUY_PRODUCT","WHEAT",3],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["SOUTH"],["CARE"],["EAST"],["COLLECT_FERTILIZER"],["DROP"],["SOUTH"],["DROP"],["WATER"],["HARVEST"],["SOUTH"],["NORTH"]],"market":[["SELL","MELON",12],["BUY_PRODUCT","WHEAT",32],["BUY_ANIMAL","GOOSE",1]]},{"farmer":["CARE"],"hands":[["EAST"],["SOUTH"],["NORTH"],["EAST"],["EAST"],["PICKUP","WHEAT",4],["SOUTH"],["PICKUP","COW",1],["HARVEST"],["EAST"],["SOUTH"],["WATER"]],"market":[["BUY_ANIMAL","GOOSE",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["WEST"],["WATER"],["EAST"],["WATER"],["WEST"],["DROP"],["PICKUP","GOOSE",1],["SOUTH"],["FERTILIZE"],["SOUTH"],["EAST"]],"market":[["SELL","MELON",6],["BUY_SEED","WHEAT",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["NORTH"],"hands":[["EAST"],["WEST"],["EAST"],["DROP"],["EAST"],["FEED"],["PICKUP","GOOSE",1],["WEST"],["SOUTH"],["WATER"],["EAST"],["WATER"]],"market":[["SELL","MELON",6],["BUY_SEED","WHEAT",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["HARVEST"],"hands":[["FERTILIZE"],["PLANT","STRAWBERRY"],["FERTILIZE"],["PICKUP","WHEAT",4],["EAST"],["CARE"],["SOUTH"],["WEST"],["EAST"],["NORTH"],["DROP"],["SOUTH"]],"market":[["SELL","MELON",6],["BUY_LAND"],["BUY_SEED","WHEAT",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["SOUTH"],["WATER"],["WATER"],["FEED"],["WATER"],["COLLECT_FERTILIZER"],["SOUTH"],["NORTH"],["EAST"],["WATER"],["PICKUP","COW",1],["PLANT","STRAWBERRY"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WEST"],"hands":[["FEED"],["SOUTH"],["SOUTH"],["SOUTH"],["NORTH"],["WEST"],["SOUTH"],["WEST"],["EAST"],["SOUTH"],["SOUTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PLANT","WHEAT"],"hands":[["CARE"],["PLANT","STRAWBERRY"],["CARE"],["WEST"],["FERTILIZE"],["FEED"],["BUILD_COOP"],["BUILD_COOP"],["PLACE","MELON",1000],["SOUTH"],["EAST"],["WEST"]],"market":[["SELL","MELON",6],["BUY_SEED","WHEAT",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WATER"],"hands":[["SOUTH"],["WATER"],["SOUTH"],["FEED"],["WATER"],["CARE"],["PLACE","GOOSE",1],["PLACE","GOOSE",1],["SOUTH"],["PLANT","WHEAT"],["PLANT","WHEAT"],["PLANT","STRAWBERRY"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WEST"],"hands":[["PLANT","WHEAT"],["WEST"],["PLANT","WHEAT"],["CARE"],["NORTH"],["COLLECT_FERTILIZER"],["EAST"],["NORTH"],["EAST"],["WATER"],["WATER"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WATER"],"hands":[["WATER"],["PLANT","STRAWBERRY"],["WATER"],["COLLECT_FERTILIZER"],["WATER"],["WEST"],["PLANT","STRAWBERRY"],["PLANT","WHEAT"],["SOUTH"],["SOUTH"],["SOUTH"],["WEST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["NORTH"],"hands":[["WEST"],["WATER"],["WEST"],["SOUTH"],["WEST"],["PLANT","WHEAT"],["WATER"],["WATER"],["EAST"],["PLANT","WHEAT"],["EAST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["NORTH"],"hands":[["PLANT","WHEAT"],["NORTH"],["PLANT","WHEAT"],["SOUTH"],["WATER"],["WATER"],["SOUTH"],["WEST"],["SOUTH"],["WATER"],["SOUTH"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WATER"],["WEST"],["WATER"],["SOUTH"],["SOUTH"],["WEST"],["PLANT","STRAWBERRY"],["WATER"],["PLANT","WHEAT"],["SOUTH"],["SOUTH"],["WEST"]],"market":[]},{"farmer":["WEST"],"hands":[["SOUTH"],["WATER"],["SOUTH"],["WATER"],["WATER"],["WATER"],["WATER"],["SOUTH"],["WATER"],["SOUTH"],["SOUTH"],["WATER"]],"market":[]},{"farmer":["PICKUP","WHEAT",4],"hands":[],"market":[["SELL","FERTILIZER",11],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["PICKUP","WHEAT",4],["PICKUP","WHEAT",3],["PICKUP","WHEAT",4],["NORTH"],["PICKUP","WHEAT",4],["WEST"],["EAST"],["NORTH"]],"market":[["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["CARE"],"hands":[["FEED"],["CARE"],["NORTH"],["WEST"],["NORTH"],["WEST"],["PLANT","WHEAT"],["NORTH"],["PICKUP","WHEAT",3],["NORTH"],["PICKUP","WHEAT",2]],"market":[["SELL","EGG",6],["SELL","FERTILIZER",1]]},{"farmer":["FEED"],"hands":[["CARE"],["COLLECT_FERTILIZER"],["EAST"],["WATER"],["FEED"],["WATER"],["WATER"],["NORTH"],["WEST"],["WEST"],["SOUTH"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["FEED"],["HARVEST"],["CARE"],["WEST"],["SOUTH"],["NORTH"],["FEED"],["WEST"],["FEED"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["CARE"],["SOUTH"],["COLLECT_FERTILIZER"],["WATER"],["PLANT","WHEAT"],["WATER"],["CARE"],["WATER"],["CARE"]],"market":[]},{"farmer":["FEED"],"hands":[["EAST"],["SOUTH"],["COLLECT_FERTILIZER"],["EAST"],["NORTH"],["WEST"],["WATER"],["HARVEST"],["COLLECT_FERTILIZER"],["HARVEST"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["CARE"],"hands":[["FEED"],["FERTILIZE"],["EAST"],["DROP"],["FEED"],["WATER"],["EAST"],["SOUTH"],["WEST"],["SOUTH"],["SOUTH"]],"market":[["SELL","MELON",6],["SELL","WHEAT",2],["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["CARE"],["WATER"],["FEED"],["PICKUP","WHEAT",2],["CARE"],["SOUTH"],["PLANT","WHEAT"],["SOUTH"],["FEED"],["EAST"],["FEED"]],"market":[["BUY_PRODUCT","WHEAT",5],["BUY_ANIMAL","GOOSE",1]]},{"farmer":["NORTH"],"hands":[["COLLECT_FERTILIZER"],["SOUTH"],["CARE"],["PICKUP","GOOSE",1],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["SOUTH"],["CARE"],["EAST"],["CARE"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["NORTH"],["FERTILIZE"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"],["HARVEST"],["SOUTH"],["SOUTH"],["COLLECT_FERTILIZER"],["DROP"],["COLLECT_FERTILIZER"]],"market":[["SELL","MELON",6]]},{"farmer":["WEST"],"hands":[["FEED"],["WATER"],["EAST"],["WEST"],["WATER"],["PLANT","TOMATO"],["PLANT","WHEAT"],["DROP"],["WEST"],["COLLECT_FERTILIZER"],["SOUTH"]],"market":[["SELL","MELON",6],["BUY_SEED","WHEAT",1],["BUY_SEED","TOMATO",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WATER"],"hands":[["CARE"],["WEST"],["FEED"],["WEST"],["NORTH"],["PLANT","TOMATO"],["WATER"],["PICKUP","WHEAT",2],["WEST"],["WEST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["COLLECT_FERTILIZER"],["WATER"],["CARE"],["BUILD_COOP"],["WATER"],["WATER"],["EAST"],["FEED"],["FERTILIZE"],["WEST"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","TOMATO",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["PLANT","STRAWBERRY"],"hands":[["NORTH"],["WEST"],["COLLECT_FERTILIZER"],["PLACE","GOOSE",1],["WEST"],["SOUTH"],["PLANT","STRAWBERRY"],["CARE"],["WATER"],["SOUTH"],["FERTILIZE"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WATER"],"hands":[["WATER"],["WATER"],["HARVEST"],["WEST"],["PLANT","STRAWBERRY"],["WATER"],["WATER"],["WEST"],["NORTH"],["SOUTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WEST"],"hands":[["EAST"],["SOUTH"],["NORTH"],["FEED"],["WATER"],["HARVEST"],["NORTH"],["NORTH"],["WATER"],["FERTILIZE"],["EAST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["WATER"],["WATER"],["WATER"],["CARE"],["EAST"],["PLANT","TOMATO"],["PLANT","WHEAT"],["PLANT","WHEAT"],["NORTH"],["WATER"],["PLANT","STRAWBERRY"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["NORTH"],["WEST"],["HARVEST"],["COLLECT_FERTILIZER"],["EAST"],["WATER"],["WATER"],["WATER"],["NORTH"],["WEST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FERTILIZE"],"hands":[["WATER"],["SOUTH"],["PLANT","WHEAT"],["NORTH"],["WATER"],["NORTH"],["EAST"],["WEST"],["FERTILIZE"],["WATER"],["EAST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["EAST"],["WATER"],["WATER"],["NORTH"],["EAST"],["SOUTH"],["NORTH"],["FEED"],["WATER"],["HARVEST"],["PLANT","STRAWBERRY"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["EAST"],"hands":[["EAST"],["HARVEST"],["NORTH"],["FERTILIZE"],["EAST"],["SOUTH"],["NORTH"],["CARE"],["SOUTH"],["PLANT","WHEAT"],["WATER"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["SOUTH"],["PLANT","TOMATO"],["WATER"],["WATER"],["WATER"],["WATER"],["WATER"],["NORTH"],["WATER"],["WATER"],["NORTH"]],"market":[]},{"farmer":["WATER"],"hands":[["WATER"],["EAST"],["SOUTH"],["SOUTH"],["EAST"],["SOUTH"],["NORTH"],["WATER"],["SOUTH"],["SOUTH"],["SOUTH"]],"market":[]},{"farmer":["NORTH"],"hands":[],"market":[["SELL","MELON",6],["SELL","FERTILIZER",9],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["HARVEST"],"hands":[["HARVEST"],["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["WATER"],["HARVEST"],["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["EAST"]],"market":[["SELL","MILK",6],["SELL","WHEAT",10],["SELL","FERTILIZER",1],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["SOUTH"],"hands":[["DROP"],["CARE"],["CARE"],["SOUTH"],["NORTH"],["NORTH"],["SOUTH"],["EAST"],["SOUTH"],["WEST"],["PICKUP","WHEAT",2]],"market":[["SELL","FERTILIZER",1],["BUY_PRODUCT","WHEAT",5]]},{"farmer":["DROP"],"hands":[["COLLECT_FERTILIZER"],["FEED"],["FEED"],["SOUTH"],["COLLECT_FERTILIZER"],["FEED"],["FEED"],["WATER"],["SOUTH"],["COLLECT_FERTILIZER"],["EAST"]],"market":[["SELL","WOOL",4],["BUY_PRODUCT","WHEAT",5]]},{"farmer":["PICKUP","WHEAT",3],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WATER"],["NORTH"],["CARE"],["CARE"],["EAST"],["SOUTH"],["WEST"],["FEED"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["FEED"],"hands":[["WEST"],["EAST"],["WEST"],["EAST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["COLLECT_FERTILIZER"],["CARE"]],"market":[]},{"farmer":["CARE"],"hands":[["WEST"],["COLLECT_FERTILIZER"],["FEED"],["WATER"],["HARVEST"],["NORTH"],["SOUTH"],["EAST"],["WEST"],["WEST"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["NORTH"],"hands":[["COLLECT_FERTILIZER"],["EAST"],["CARE"],["SOUTH"],["NORTH"],["FEED"],["FEED"],["WATER"],["SOUTH"],["FERTILIZE"],["EAST"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["FEED"],["COLLECT_FERTILIZER"],["PLANT","STRAWBERRY"],["WATER"],["CARE"],["CARE"],["NORTH"],["WATER"],["WATER"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["FEED"],"hands":[["FERTILIZE"],["HARVEST"],["WEST"],["WATER"],["WEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WATER"],["HARVEST"],["NORTH"],["NORTH"]],"market":[]},{"farmer":["CARE"],"hands":[["WATER"],["CARE"],["FERTILIZE"],["EAST"],["WATER"],["EAST"],["WEST"],["HARVEST"],["PLANT","WHEAT"],["COLLECT_FERTILIZER"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["WEST"],["EAST"],["WATER"],["PLANT","WHEAT"],["WEST"],["FEED"],["WATER"],["PLANT","WHEAT"],["WATER"],["WEST"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","STRAWBERRY",1]]},{"farmer":["WATER"],"hands":[["WATER"],["FEED"],["SOUTH"],["WATER"],["FERTILIZE"],["CARE"],["HARVEST"],["WATER"],["WEST"],["FERTILIZE"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["WEST"],["CARE"],["WATER"],["EAST"],["WATER"],["COLLECT_FERTILIZER"],["PLANT","WHEAT"],["NORTH"],["DIG"],["WATER"],["EAST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PLANT","WHEAT"],"hands":[["FERTILIZE"],["COLLECT_FERTILIZER"],["HARVEST"],["PLANT","WHEAT"],["NORTH"],["SOUTH"],["WATER"],["WATER"],["PLANT","WHEAT"],["SOUTH"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","TOMATO",1]]},{"farmer":["WATER"],"hands":[["WATER"],["HARVEST"],["PLANT","WHEAT"],["WATER"],["FERTILIZE"],["FEED"],["SOUTH"],["NORTH"],["WATER"],["HARVEST"],["WATER"]],"market":[["SELL","WHEAT",4],["BUY_SEED","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["NORTH"],["EAST"],["WATER"],["EAST"],["WATER"],["CARE"],["WATER"],["WATER"],["WEST"],["WATER"],["EAST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","TOMATO",1]]},{"farmer":["WEST"],"hands":[["HARVEST"],["SOUTH"],["SOUTH"],["PLANT","WHEAT"],["WEST"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["WATER"],["SOUTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["WATER"],["SOUTH"],["FERTILIZE"],["WATER"],["WATER"],["SOUTH"],["WATER"],["HARVEST"],["WEST"],["FERTILIZE"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["NORTH"],["FERTILIZE"],["WATER"],["NORTH"],["WEST"],["WEST"],["WEST"],["PLANT","WHEAT"],["WATER"],["WATER"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["HARVEST"],["WATER"],["EAST"],["PLANT","WHEAT"],["HARVEST"],["DROP"],["NORTH"],["WATER"],["WEST"],["EAST"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["WATER"],["WEST"],["NORTH"],["WATER"],["WATER"],["SOUTH"],["FERTILIZE"],["SOUTH"],["PLANT","TOMATO"],["WATER"],["WATER"]],"market":[["SELL","MILK",3],["SELL","FERTILIZER",4]]},{"farmer":["CARE"],"hands":[["SOUTH"],["SOUTH"],["WATER"],["WEST"],["SOUTH"],["SOUTH"],["WATER"],["WEST"],["WATER"],["SOUTH"],["WEST"]],"market":[["SELL","EGG",2],["SELL","WHEAT",3]]},{"farmer":["SOUTH"],"hands":[["EAST"],["WATER"],["SOUTH"],["WATER"],["EAST"],["SOUTH"],["SOUTH"],["WATER"],["NORTH"],["WEST"],["WATER"]],"market":[]},{"farmer":["PICKUP","WHEAT",4],"hands":[],"market":[["SELL","FERTILIZER",4],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",4],["PICKUP","WHEAT",3],["WATER"],["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["WEST"],["EAST"],["WEST"]],"market":[["SELL","MILK",2],["SELL","FERTILIZER",1],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["FEED"],["CARE"],["HARVEST"],["FEED"],["NORTH"],["WEST"],["EAST"],["WEST"],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",3],["SOUTH"]],"market":[["SELL","EGG",6],["SELL","FERTILIZER",1]]},{"farmer":["CARE"],"hands":[["CARE"],["FEED"],["PLANT","WHEAT"],["CARE"],["FEED"],["WATER"],["WATER"],["COLLECT_FERTILIZER"],["NORTH"],["SOUTH"],["PLANT","WHEAT"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WATER"],["NORTH"],["CARE"],["HARVEST"],["HARVEST"],["WEST"],["COLLECT_FERTILIZER"],["FEED"],["WATER"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["WEST"],"hands":[["EAST"],["WEST"],["EAST"],["FEED"],["COLLECT_FERTILIZER"],["PLANT","WHEAT"],["PLANT","WHEAT"],["WATER"],["WEST"],["CARE"],["EAST"]],"market":[["SELL","WHEAT",5],["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["FEED"],["FEED"],["WATER"],["CARE"],["NORTH"],["WATER"],["WATER"],["HARVEST"],["FERTILIZE"],["COLLECT_FERTILIZER"],["WATER"]],"market":[]},{"farmer":["CARE"],"hands":[["CARE"],["CARE"],["NORTH"],["NORTH"],["FEED"],["WEST"],["NORTH"],["PLANT","WHEAT"],["WATER"],["HARVEST"],["SOUTH"]],"market":[["SELL","WHEAT",2],["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FEED"],["CARE"],["WATER"],["FEED"],["WATER"],["WEST"],["SOUTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["FEED"],["SOUTH"],["EAST"],["CARE"],["COLLECT_FERTILIZER"],["HARVEST"],["CARE"],["WEST"],["NORTH"],["FEED"],["HARVEST"]],"market":[]},{"farmer":["CARE"],"hands":[["CARE"],["WATER"],["EAST"],["COLLECT_FERTILIZER"],["NORTH"],["PLANT","WHEAT"],["COLLECT_FERTILIZER"],["WATER"],["HARVEST"],["CARE"],["PLANT","WHEAT"]],"market":[["SELL","WHEAT",4],["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["HARVEST"],["FEED"],["NORTH"],["WATER"],["WATER"],["HARVEST"],["SOUTH"],["WATER"],["COLLECT_FERTILIZER"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","TOMATO",1]]},{"farmer":["WEST"],"hands":[["NORTH"],["PLANT","WHEAT"],["CARE"],["NORTH"],["NORTH"],["SOUTH"],["SOUTH"],["WATER"],["WEST"],["SOUTH"],["EAST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["FEED"],["WATER"],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["WATER"],["SOUTH"],["HARVEST"],["FERTILIZE"],["WATER"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","TOMATO",1]]},{"farmer":["CARE"],"hands":[["CARE"],["WEST"],["HARVEST"],["WEST"],["EAST"],["SOUTH"],["FERTILIZE"],["PLANT","WHEAT"],["WATER"],["SOUTH"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["SOUTH"],["NORTH"],["WATER"],["WATER"],["WATER"],["WATER"],["WATER"],["NORTH"],["EAST"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","TOMATO",1]]},{"farmer":["WEST"],"hands":[["NORTH"],["WATER"],["FERTILIZE"],["WEST"],["EAST"],["HARVEST"],["EAST"],["SOUTH"],["WATER"],["WATER"],["WATER"]],"market":[]},{"farmer":["HARVEST"],"hands":[["WATER"],["HARVEST"],["WATER"],["HARVEST"],["WATER"],["PLANT","TOMATO"],["WATER"],["WATER"],["HARVEST"],["NORTH"],["SOUTH"]],"market":[["SELL","STRAWBERRY",2],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["EAST"],["PLANT","WHEAT"],["SOUTH"],["WATER"],["EAST"],["WATER"],["NORTH"],["SOUTH"],["WEST"],["WATER"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["WATER"],["WATER"],["EAST"],["WEST"],["WATER"],["SOUTH"],["WATER"],["WATER"],["WATER"],["NORTH"],["EAST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["EAST"],["SOUTH"],["SOUTH"],["HARVEST"],["EAST"],["WATER"],["HARVEST"],["SOUTH"],["NORTH"],["WATER"],["PLANT","STRAWBERRY"]],"market":[]},{"farmer":["WATER"],"hands":[["WATER"],["WATER"],["FERTILIZE"],["WATER"],["WATER"],["SOUTH"],["PLANT","WHEAT"],["WATER"],["WATER"],["SOUTH"],["WATER"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["SOUTH"],"hands":[["SOUTH"],["SOUTH"],["WATER"],["SOUTH"],["SOUTH"],["WATER"],["WATER"],["SOUTH"],["SOUTH"],["WEST"],["NORTH"]],"market":[["SELL","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["WATER"],["WATER"],["SOUTH"],["EAST"],["WATER"],["WEST"],["SOUTH"],["WATER"],["SOUTH"],["WEST"],["WATER"]],"market":[]},{"farmer":["HARVEST"],"hands":[],"market":[["SELL","FERTILIZER",14],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["PLACE","MILK",1000],"hands":[["HARVEST"],["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["NORTH"],["NORTH"],["SOUTH"],["EAST"],["NORTH"]],"market":[["SELL","MILK",3],["SELL","WHEAT",13],["SELL","STRAWBERRY",6],["SELL","FERTILIZER",1],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["PICKUP","WHEAT",4],"hands":[["PLACE","MILK",1000],["FEED"],["NORTH"],["NORTH"],["HARVEST"],["COLLECT_FERTILIZER"],["NORTH"],["WEST"],["PICKUP","WHEAT",4],["EAST"],["PICKUP","WHEAT",4]],"market":[["SELL","MILK",6],["SELL","FERTILIZER",1]]},{"farmer":["FEED"],"hands":[["PICKUP","WHEAT",3],["CARE"],["EAST"],["HARVEST"],["SOUTH"],["HARVEST"],["HARVEST"],["WATER"],["WEST"],["NORTH"],["SOUTH"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["CARE"],"hands":[["FEED"],["COLLECT_FERTILIZER"],["FEED"],["SOUTH"],["PLACE","MILK",1000],["WEST"],["WEST"],["HARVEST"],["FEED"],["HARVEST"],["FEED"]],"market":[["SELL","MILK",6]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["CARE"],["WEST"],["CARE"],["SOUTH"],["PICKUP","WHEAT",3],["SOUTH"],["PLACE","MILK",1000],["PLANT","WHEAT"],["CARE"],["SOUTH"],["CARE"]],"market":[["SELL","MILK",6]]},{"farmer":["NORTH"],"hands":[["COLLECT_FERTILIZER"],["FEED"],["COLLECT_FERTILIZER"],["PLACE","MILK",1000],["NORTH"],["FERTILIZE"],["PICKUP","WHEAT",3],["WATER"],["COLLECT_FERTILIZER"],["WEST"],["SOUTH"]],"market":[["SELL","MILK",3],["SELL","FERTILIZER",1]]},{"farmer":["FEED"],"hands":[["NORTH"],["CARE"],["EAST"],["PICKUP","WHEAT",3],["FEED"],["WATER"],["EAST"],["WEST"],["HARVEST"],["DROP"],["FEED"]],"market":[["SELL","MILK",6]]},{"farmer":["CARE"],"hands":[["CARE"],["COLLECT_FERTILIZER"],["FEED"],["NORTH"],["NORTH"],["SOUTH"],["NORTH"],["FEED"],["WEST"],["EAST"],["COLLECT_FERTILIZER"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["NORTH"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["CARE"],["COLLECT_FERTILIZER"],["FEED"],["WATER"],["FEED"],["CARE"],["FEED"],["EAST"],["HARVEST"]],"market":[["SELL","STRAWBERRY",3]]},{"farmer":["FEED"],"hands":[["EAST"],["SOUTH"],["EAST"],["NORTH"],["CARE"],["SOUTH"],["CARE"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["EAST"],["CARE"]],"market":[]},{"farmer":["CARE"],"hands":[["EAST"],["FERTILIZE"],["FEED"],["NORTH"],["HARVEST"],["WATER"],["COLLECT_FERTILIZER"],["WEST"],["CARE"],["COLLECT_FERTILIZER"],["EAST"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["WATER"],["CARE"],["WATER"],["COLLECT_FERTILIZER"],["HARVEST"],["NORTH"],["FEED"],["HARVEST"],["EAST"],["WATER"]],"market":[]},{"farmer":["WEST"],"hands":[["EAST"],["WEST"],["HARVEST"],["WEST"],["SOUTH"],["PLANT","WHEAT"],["FEED"],["HARVEST"],["EAST"],["FERTILIZE"],["EAST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FERTILIZE"],"hands":[["WATER"],["FERTILIZE"],["SOUTH"],["WATER"],["SOUTH"],["WATER"],["CARE"],["CARE"],["EAST"],["WATER"],["EAST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["HARVEST"],["WATER"],["SOUTH"],["WEST"],["DROP"],["EAST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["DROP"],["NORTH"],["FERTILIZE"]],"market":[]},{"farmer":["WEST"],"hands":[["PLANT","WHEAT"],["SOUTH"],["FERTILIZE"],["WATER"],["EAST"],["WATER"],["EAST"],["WEST"],["WEST"],["WATER"],["WATER"]],"market":[["SELL","STRAWBERRY",5],["SELL","EGG",7],["SELL","FERTILIZER",3],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WATER"],["WATER"],["WATER"],["HARVEST"],["EAST"],["HARVEST"],["WATER"],["WATER"],["WEST"],["SOUTH"],["EAST"]],"market":[]},{"farmer":["WEST"],"hands":[["EAST"],["WEST"],["EAST"],["NORTH"],["COLLECT_FERTILIZER"],["PLANT","WHEAT"],["EAST"],["NORTH"],["WEST"],["SOUTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["NORTH"],["WATER"],["WATER"],["WATER"],["HARVEST"],["WATER"],["FERTILIZE"],["WATER"],["WEST"],["WATER"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["WATER"],["SOUTH"],["HARVEST"],["WEST"],["SOUTH"],["WEST"],["WATER"],["NORTH"],["HARVEST"],["HARVEST"],["WATER"]],"market":[]},{"farmer":["PLANT","WHEAT"],"hands":[["NORTH"],["WATER"],["SOUTH"],["FERTILIZE"],["SOUTH"],["WEST"],["NORTH"],["HARVEST"],["WATER"],["PLANT","WHEAT"],["EAST"]],"market":[["SELL","MILK",2]]},{"farmer":["WATER"],"hands":[["FERTILIZE"],["SOUTH"],["WATER"],["WATER"],["WATER"],["WATER"],["FERTILIZE"],["FERTILIZE"],["SOUTH"],["WATER"],["WATER"]],"market":[["SELL","WHEAT",12]]},{"farmer":["NORTH"],"hands":[["WATER"],["WATER"],["SOUTH"],["WEST"],["WEST"],["WEST"],["WATER"],["WATER"],["SOUTH"],["WEST"],["SOUTH"]],"market":[]},{"farmer":["PICKUP","WHEAT",4],"hands":[],"market":[["SELL","FERTILIZER",4],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["WATER"],["PICKUP","WHEAT",4],["EAST"],["SOUTH"],["EAST"],["WEST"]],"market":[["SELL","MILK",3],["SELL","STRAWBERRY",6],["SELL","FERTILIZER",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["BUY_ANIMAL","SHEEP",2]]},{"farmer":["FEED"],"hands":[["FEED"],["PICKUP","SHEEP",1],["PICKUP","SHEEP",1],["FEED"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WATER"],["WEST"],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["PICKUP","SHEEP",1]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["CARE"],"hands":[["CARE"],["EAST"],["HARVEST"],["CARE"],["EAST"],["HARVEST"],["HARVEST"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"],["FEED"],["SOUTH"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["BUILD_PASTURE"],["BUILD_PASTURE"],["NORTH"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["WEST"],["COLLECT_FERTILIZER"],["FEED"],["CARE"],["WATER"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["PLACE","SHEEP",1],["EAST"],["FEED"],["EAST"],["FERTILIZE"],["FEED"],["FERTILIZE"],["NORTH"],["CARE"],["COLLECT_FERTILIZER"],["SOUTH"]],"market":[]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["FEED"],["BUILD_PASTURE"],["CARE"],["COLLECT_FERTILIZER"],["WATER"],["CARE"],["WATER"],["COLLECT_FERTILIZER"],["NORTH"],["SOUTH"],["SOUTH"]],"market":[]},{"farmer":["CARE"],"hands":[["EAST"],["CARE"],["PLACE","SHEEP",1],["NORTH"],["EAST"],["SOUTH"],["EAST"],["NORTH"],["NORTH"],["FEED"],["FEED"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["FEED"],["WEST"],["FEED"],["FEED"],["WATER"],["WATER"],["FEED"],["COLLECT_FERTILIZER"],["NORTH"],["CARE"],["CARE"],["SOUTH"]],"market":[]},{"farmer":["FEED"],"hands":[["CARE"],["WEST"],["CARE"],["CARE"],["NORTH"],["HARVEST"],["CARE"],["HARVEST"],["WATER"],["COLLECT_FERTILIZER"],["SOUTH"],["WATER"]],"market":[]},{"farmer":["HARVEST"],"hands":[["COLLECT_FERTILIZER"],["FEED"],["SOUTH"],["WEST"],["FERTILIZE"],["PLANT","WHEAT"],["SOUTH"],["WEST"],["EAST"],["NORTH"],["FEED"],["EAST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["NORTH"],["CARE"],["WATER"],["WATER"],["WATER"],["WATER"],["WATER"],["HARVEST"],["FERTILIZE"],["FERTILIZE"],["COLLECT_FERTILIZER"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FEED"],["COLLECT_FERTILIZER"],["HARVEST"],["HARVEST"],["NORTH"],["WEST"],["EAST"],["FERTILIZE"],["WATER"],["WATER"],["CARE"],["EAST"]],"market":[]},{"farmer":["WEST"],"hands":[["CARE"],["WEST"],["PLANT","WHEAT"],["PLANT","WHEAT"],["NORTH"],["WATER"],["WATER"],["WATER"],["EAST"],["EAST"],["HARVEST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["COLLECT_FERTILIZER"],["FERTILIZE"],["WATER"],["WATER"],["WATER"],["SOUTH"],["SOUTH"],["SOUTH"],["WATER"],["WATER"],["SOUTH"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["NORTH"],["WATER"],["EAST"],["WEST"],["HARVEST"],["WATER"],["WATER"],["WATER"],["EAST"],["EAST"],["WATER"],["WATER"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["FERTILIZE"],["WEST"],["WATER"],["HARVEST"],["PLANT","WHEAT"],["WEST"],["HARVEST"],["SOUTH"],["FERTILIZE"],["WATER"],["EAST"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["EAST"],["WATER"],["HARVEST"],["NORTH"],["WATER"],["WATER"],["PLANT","WHEAT"],["WATER"],["WATER"],["EAST"],["EAST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["FERTILIZE"],["SOUTH"],["PLANT","WHEAT"],["HARVEST"],["NORTH"],["SOUTH"],["WATER"],["SOUTH"],["EAST"],["WATER"],["NORTH"],["EAST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["SOUTH"],["WATER"],["WATER"],["EAST"],["WATER"],["WATER"],["NORTH"],["WATER"],["FERTILIZE"],["SOUTH"],["FERTILIZE"],["EAST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["SOUTH"],["HARVEST"],["SOUTH"],["NORTH"],["FERTILIZE"],["WEST"],["NORTH"],["NORTH"],["WATER"],["WATER"],["WATER"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["FERTILIZE"],["PLANT","WHEAT"],["WATER"],["WATER"],["SOUTH"],["WATER"],["FEED"],["NORTH"],["SOUTH"],["EAST"],["EAST"],["HARVEST"]],"market":[["SELL","WOOL",2]]},{"farmer":["FERTILIZE"],"hands":[["WATER"],["WATER"],["HARVEST"],["WEST"],["SOUTH"],["NORTH"],["CARE"],["NORTH"],["SOUTH"],["WATER"],["EAST"],["EAST"]],"market":[["SELL","WHEAT",19],["SELL","EGG",12]]},{"farmer":["WATER"],"hands":[["NORTH"],["SOUTH"],["EAST"],["HARVEST"],["FERTILIZE"],["WATER"],["HARVEST"],["NORTH"],["SOUTH"],["SOUTH"],["WATER"],["WATER"]],"market":[]},{"farmer":["HARVEST"],"hands":[],"market":[["SELL","STRAWBERRY",11],["SELL","FERTILIZER",2],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["PLACE","MILK",1000],"hands":[["HARVEST"],["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["NORTH"],["NORTH"],["SOUTH"],["EAST"],["WEST"]],"market":[["SELL","MILK",3],["SELL","WHEAT",16],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["PICKUP","WHEAT",4],"hands":[["PLACE","MILK",1000],["FEED"],["FEED"],["NORTH"],["HARVEST"],["COLLECT_FERTILIZER"],["EAST"],["WEST"],["PICKUP","WHEAT",4],["EAST"],["PICKUP","WHEAT",3],["PICKUP","SHEEP",1]],"market":[["SELL","MILK",3],["SELL","FERTILIZER",1]]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["CARE"],["CARE"],["HARVEST"],["NORTH"],["HARVEST"],["WATER"],["COLLECT_FERTILIZER"],["WEST"],["HARVEST"],["SOUTH"],["SOUTH"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["CARE"],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["SOUTH"],["HARVEST"],["WEST"],["EAST"],["WEST"],["FEED"],["WEST"],["FEED"],["WATER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["EAST"],["SOUTH"],["NORTH"],["WATER"],["WATER"],["WATER"],["CARE"],["PLACE","MILK",1000],["CARE"],["HARVEST"]],"market":[["SELL","MILK",3]]},{"farmer":["NORTH"],"hands":[["EAST"],["FEED"],["FEED"],["PLACE","MILK",1000],["HARVEST"],["WEST"],["HARVEST"],["HARVEST"],["COLLECT_FERTILIZER"],["EAST"],["SOUTH"],["PLANT","WHEAT"]],"market":[["SELL","MILK",3]]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["CARE"],["CARE"],["NORTH"],["NORTH"],["WATER"],["PLANT","WHEAT"],["PLANT","WHEAT"],["WEST"],["COLLECT_FERTILIZER"],["FEED"],["WATER"]],"market":[["SELL","WHEAT",8],["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["HARVEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["NORTH"],["HARVEST"],["HARVEST"],["WATER"],["WATER"],["FEED"],["EAST"],["COLLECT_FERTILIZER"],["SOUTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["WEST"],["EAST"],["COLLECT_FERTILIZER"],["SOUTH"],["PLANT","WHEAT"],["NORTH"],["NORTH"],["CARE"],["COLLECT_FERTILIZER"],["CARE"],["WATER"]],"market":[["SELL","WHEAT",4],["SELL","WOOL",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["WATER"],["EAST"],["NORTH"],["SOUTH"],["WATER"],["FEED"],["FEED"],["NORTH"],["HARVEST"],["HARVEST"],["EAST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FERTILIZE"],"hands":[["HARVEST"],["WEST"],["EAST"],["WATER"],["SOUTH"],["SOUTH"],["CARE"],["CARE"],["FEED"],["NORTH"],["SOUTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["NORTH"],["FERTILIZE"],["FERTILIZE"],["WEST"],["SOUTH"],["WATER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["HARVEST"],["SOUTH"],["EAST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["HARVEST"],["WATER"],["WATER"],["WATER"],["DROP"],["HARVEST"],["NORTH"],["WEST"],["HARVEST"],["NORTH"],["FERTILIZE"],["PLANT","WHEAT"]],"market":[["SELL","MILK",6],["SELL","STRAWBERRY",4],["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["NORTH"],["WEST"],["NORTH"],["WEST"],["NORTH"],["PLANT","WHEAT"],["FERTILIZE"],["WATER"],["NORTH"],["WATER"],["WATER"],["WATER"]],"market":[["SELL","EGG",12],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["FERTILIZE"],["FERTILIZE"],["WATER"],["FERTILIZE"],["NORTH"],["WATER"],["WATER"],["NORTH"],["FERTILIZE"],["NORTH"],["WEST"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","TOMATO",1]]},{"farmer":["NORTH"],"hands":[["WATER"],["WATER"],["HARVEST"],["WATER"],["COLLECT_FERTILIZER"],["WEST"],["EAST"],["FERTILIZE"],["WATER"],["HARVEST"],["WATER"],["WATER"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["EAST"],["NORTH"],["PLANT","WHEAT"],["NORTH"],["EAST"],["WATER"],["HARVEST"],["WATER"],["NORTH"],["EAST"],["NORTH"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["HARVEST"],["HARVEST"],["WATER"],["WATER"],["EAST"],["WEST"],["WATER"],["HARVEST"],["NORTH"],["HARVEST"],["WATER"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["EAST"],["WATER"],["SOUTH"],["WEST"],["FERTILIZE"],["WATER"],["NORTH"],["NORTH"],["FERTILIZE"],["NORTH"],["WEST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["HARVEST"],["SOUTH"],["SOUTH"],["WATER"],["EAST"],["SOUTH"],["WATER"],["HARVEST"],["EAST"],["HARVEST"],["SOUTH"],["EAST"]],"market":[]},{"farmer":["WATER"],"hands":[["WATER"],["SOUTH"],["SOUTH"],["HARVEST"],["HARVEST"],["WATER"],["NORTH"],["WATER"],["WATER"],["EAST"],["WATER"],["EAST"]],"market":[["SELL","WOOL",2]]},{"farmer":["SOUTH"],"hands":[["EAST"],["WATER"],["WATER"],["WEST"],["WATER"],["SOUTH"],["WATER"],["NORTH"],["EAST"],["WATER"],["WEST"],["WATER"]],"market":[["SELL","WHEAT",5]]},{"farmer":["SOUTH"],"hands":[["SOUTH"],["SOUTH"],["HARVEST"],["HARVEST"],["NORTH"],["WATER"],["WEST"],["HARVEST"],["WATER"],["SOUTH"],["WATER"],["HARVEST"]],"market":[]},{"farmer":["PICKUP","WHEAT",4],"hands":[],"market":[["SELL","STRAWBERRY",11],["SELL","FERTILIZER",8],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",4],["HARVEST"],["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["EAST"],["WEST"],["EAST"],["NORTH"]],"market":[["SELL","MILK",9],["SELL","STRAWBERRY",6],["SELL","FERTILIZER",1],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["FEED"],["PLACE","MILK",1000],["FEED"],["FEED"],["COLLECT_FERTILIZER"],["HARVEST"],["EAST"],["WEST"],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3]],"market":[["SELL","STRAWBERRY",6],["SELL","FERTILIZER",1],["HIRE"]]},{"farmer":["CARE"],"hands":[["CARE"],["COLLECT_FERTILIZER"],["CARE"],["CARE"],["NORTH"],["EAST"],["WATER"],["WATER"],["NORTH"],["NORTH"],["SOUTH"],["COLLECT_FERTILIZER"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["EAST"],["NORTH"],["COLLECT_FERTILIZER"],["PLACE","MILK",1000],["HARVEST"],["HARVEST"],["COLLECT_FERTILIZER"],["FEED"],["FEED"],["SOUTH"]],"market":[]},{"farmer":["WEST"],"hands":[["EAST"],["COLLECT_FERTILIZER"],["FEED"],["FEED"],["NORTH"],["WEST"],["PLANT","WHEAT"],["PLANT","WHEAT"],["NORTH"],["CARE"],["CARE"],["SOUTH"]],"market":[["SELL","STRAWBERRY",2],["SELL","WOOL",1]]},{"farmer":["FEED"],"hands":[["FEED"],["SOUTH"],["CARE"],["CARE"],["COLLECT_FERTILIZER"],["WEST"],["WATER"],["WATER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["SOUTH"]],"market":[]},{"farmer":["CARE"],"hands":[["CARE"],["WATER"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"],["WATER"],["NORTH"],["WEST"],["WEST"],["NORTH"],["HARVEST"],["WATER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["HARVEST"],["SOUTH"],["FEED"],["WATER"],["HARVEST"],["FEED"],["FEED"],["FERTILIZE"],["FEED"],["SOUTH"],["SOUTH"]],"market":[]},{"farmer":["HARVEST"],"hands":[["FEED"],["PLANT","TOMATO"],["FERTILIZE"],["CARE"],["EAST"],["PLANT","WHEAT"],["CARE"],["COLLECT_FERTILIZER"],["WATER"],["CARE"],["FEED"],["WATER"]],"market":[["SELL","MILK",9],["SELL","STRAWBERRY",2],["SELL","WOOL",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["CARE"],["WATER"],["WATER"],["NORTH"],["WATER"],["WATER"],["COLLECT_FERTILIZER"],["HARVEST"],["WEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["EAST"]],"market":[["SELL","STRAWBERRY",2],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["EAST"],["SOUTH"],["SOUTH"],["WATER"],["EAST"],["WEST"],["EAST"],["CARE"],["HARVEST"],["NORTH"],["CARE"],["WATER"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["WATER"],["FERTILIZE"],["WATER"],["WEST"],["FERTILIZE"],["WATER"],["FEED"],["WEST"],["WATER"],["WATER"],["HARVEST"],["EAST"]],"market":[]},{"farmer":["WATER"],"hands":[["NORTH"],["WATER"],["HARVEST"],["WATER"],["WATER"],["HARVEST"],["HARVEST"],["FEED"],["WEST"],["NORTH"],["SOUTH"],["WATER"]],"market":[]},{"farmer":["SOUTH"],"hands":[["WATER"],["WEST"],["PLANT","WHEAT"],["WEST"],["EAST"],["PLANT","WHEAT"],["CARE"],["CARE"],["WATER"],["WATER"],["WATER"],["NORTH"]],"market":[["SELL","WHEAT",10],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["EAST"],["SOUTH"],["WATER"],["HARVEST"],["FERTILIZE"],["WATER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["NORTH"],["EAST"],["SOUTH"],["EAST"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","TOMATO",1]]},{"farmer":["HARVEST"],"hands":[["FERTILIZE"],["WATER"],["SOUTH"],["WATER"],["WATER"],["SOUTH"],["NORTH"],["WEST"],["WATER"],["HARVEST"],["WATER"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PLANT","WHEAT"],"hands":[["WATER"],["WEST"],["WATER"],["NORTH"],["NORTH"],["WATER"],["WATER"],["HARVEST"],["WEST"],["WATER"],["HARVEST"],["WATER"]],"market":[["SELL","WHEAT",4],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["EAST"],["WATER"],["EAST"],["HARVEST"],["HARVEST"],["HARVEST"],["EAST"],["WATER"],["FERTILIZE"],["EAST"],["PLANT","WHEAT"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["HARVEST"],["FERTILIZE"],["NORTH"],["WATER"],["WATER"],["PLANT","TOMATO"],["WATER"],["NORTH"],["WATER"],["WATER"],["WATER"],["FERTILIZE"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WATER"],["WEST"],["NORTH"],["WEST"],["WEST"],["WATER"],["SOUTH"],["HARVEST"],["NORTH"],["WEST"],["WEST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FERTILIZE"],"hands":[["WEST"],["WATER"],["WATER"],["HARVEST"],["WATER"],["SOUTH"],["FERTILIZE"],["WATER"],["WATER"],["SOUTH"],["FERTILIZE"],["EAST"]],"market":[["SELL","MILK",2]]},{"farmer":["SOUTH"],"hands":[["WEST"],["SOUTH"],["SOUTH"],["WATER"],["SOUTH"],["WATER"],["SOUTH"],["SOUTH"],["EAST"],["SOUTH"],["WATER"],["PLANT","WHEAT"]],"market":[["SELL","EGG",10],["SELL","WHEAT",5]]},{"farmer":["WATER"],"hands":[["SOUTH"],["WATER"],["WATER"],["SOUTH"],["SOUTH"],["WEST"],["WATER"],["SOUTH"],["FERTILIZE"],["FEED"],["WEST"],["WATER"]],"market":[]},{"farmer":["PICKUP","WHEAT",4],"hands":[],"market":[["SELL","STRAWBERRY",11],["SELL","FERTILIZER",7],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["HARVEST"],["NORTH"],["SOUTH"],["EAST"],["WEST"]],"market":[["SELL","STRAWBERRY",6],["SELL","WHEAT",16],["SELL","WOOL",4],["SELL","FERTILIZER",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["EAST"],["FEED"],["FEED"],["PLACE","MILK",1000],["NORTH"],["COLLECT_FERTILIZER"],["EAST"],["WEST"],["COLLECT_FERTILIZER"],["EAST"],["PICKUP","WHEAT",3],["PICKUP","SHEEP",1]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["CARE"],"hands":[["EAST"],["CARE"],["CARE"],["PICKUP","WHEAT",3],["NORTH"],["HARVEST"],["EAST"],["WEST"],["NORTH"],["NORTH"],["SOUTH"],["SOUTH"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["NORTH"],["HARVEST"],["WEST"],["WATER"],["WEST"],["COLLECT_FERTILIZER"],["EAST"],["FEED"],["WATER"]],"market":[]},{"farmer":["WEST"],"hands":[["HARVEST"],["WEST"],["EAST"],["FEED"],["NORTH"],["SOUTH"],["EAST"],["HARVEST"],["NORTH"],["HARVEST"],["CARE"],["SOUTH"]],"market":[["SELL","STRAWBERRY",1]]},{"farmer":["FEED"],"hands":[["EAST"],["FEED"],["FEED"],["CARE"],["HARVEST"],["WATER"],["WATER"],["NORTH"],["COLLECT_FERTILIZER"],["NORTH"],["SOUTH"],["WATER"]],"market":[]},{"farmer":["CARE"],"hands":[["COLLECT_FERTILIZER"],["CARE"],["CARE"],["WEST"],["EAST"],["HARVEST"],["HARVEST"],["WATER"],["NORTH"],["HARVEST"],["FEED"],["SOUTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WEST"],["SOUTH"],["PLANT","TOMATO"],["PLANT","WHEAT"],["NORTH"],["NORTH"],["NORTH"],["COLLECT_FERTILIZER"],["WATER"]],"market":[["SELL","WHEAT",8],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["WATER"],["WEST"],["SOUTH"],["FEED"],["HARVEST"],["WATER"],["WATER"],["WATER"],["WATER"],["HARVEST"],["CARE"],["SOUTH"]],"market":[["SELL","MILK",1]]},{"farmer":["FERTILIZE"],"hands":[["HARVEST"],["SOUTH"],["WATER"],["COLLECT_FERTILIZER"],["SOUTH"],["SOUTH"],["NORTH"],["NORTH"],["WEST"],["EAST"],["HARVEST"],["WATER"]],"market":[]},{"farmer":["WATER"],"hands":[["PLANT","WHEAT"],["FERTILIZE"],["EAST"],["HARVEST"],["SOUTH"],["FERTILIZE"],["WATER"],["HARVEST"],["WATER"],["HARVEST"],["SOUTH"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["WATER"],["WATER"],["FERTILIZE"],["CARE"],["SOUTH"],["WATER"],["NORTH"],["DIG"],["WEST"],["SOUTH"],["FERTILIZE"],["WEST"]],"market":[]},{"farmer":["FEED"],"hands":[["EAST"],["SOUTH"],["WATER"],["NORTH"],["WEST"],["WEST"],["HARVEST"],["PLANT","TOMATO"],["WATER"],["HARVEST"],["WATER"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["NORTH"],["FERTILIZE"],["SOUTH"],["WATER"],["DROP"],["WEST"],["NORTH"],["WATER"],["WEST"],["SOUTH"],["EAST"],["HARVEST"]],"market":[["SELL","STRAWBERRY",6]]},{"farmer":["CARE"],"hands":[["FERTILIZE"],["WATER"],["FERTILIZE"],["NORTH"],["EAST"],["WATER"],["NORTH"],["EAST"],["WATER"],["SOUTH"],["EAST"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["WEST"],["WATER"],["WATER"],["COLLECT_FERTILIZER"],["SOUTH"],["WATER"],["HARVEST"],["WEST"],["WEST"],["WATER"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["NORTH"],["WATER"],["EAST"],["EAST"],["NORTH"],["WATER"],["HARVEST"],["DIG"],["HARVEST"],["WEST"],["EAST"],["WEST"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["NORTH"],["WEST"],["NORTH"],["SOUTH"],["COLLECT_FERTILIZER"],["WEST"],["PLANT","WHEAT"],["PLANT","TOMATO"],["DIG"],["WEST"],["WATER"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["FERTILIZE"],["WATER"],["WATER"],["WATER"],["HARVEST"],["WATER"],["WATER"],["WATER"],["PLANT","TOMATO"],["DROP"],["HARVEST"],["NORTH"]],"market":[["SELL","STRAWBERRY",6],["BUY_SEED","WHEAT",1]]},{"farmer":["DIG"],"hands":[["WATER"],["NORTH"],["HARVEST"],["EAST"],["NORTH"],["NORTH"],["WEST"],["SOUTH"],["PLANT","TOMATO"],["NORTH"],["PLANT","WHEAT"],["WATER"]],"market":[["SELL","STRAWBERRY",4],["BUY_SEED","WHEAT",1]]},{"farmer":["PLANT","WHEAT"],"hands":[["WEST"],["WATER"],["PLANT","WHEAT"],["HARVEST"],["COLLECT_FERTILIZER"],["WATER"],["NORTH"],["WATER"],["PLANT","TOMATO"],["COLLECT_FERTILIZER"],["WATER"],["WEST"]],"market":[["SELL","MILK",2]]},{"farmer":["WATER"],"hands":[["HARVEST"],["EAST"],["WATER"],["EAST"],["HARVEST"],["PASS"],["HARVEST"],["HARVEST"],["PLANT","TOMATO"],["HARVEST"],["SOUTH"],["NORTH"]],"market":[["SELL","EGG",10],["SELL","WHEAT",7]]},{"farmer":["SOUTH"],"hands":[["FERTILIZE"],["WATER"],["SOUTH"],["COLLECT_FERTILIZER"],["EAST"],["SOUTH"],["WATER"],["SOUTH"],["SOUTH"],["NORTH"],["WATER"],["NORTH"]],"market":[]},{"farmer":["PICKUP","WHEAT",4],"hands":[],"market":[["SELL","STRAWBERRY",11],["SELL","FERTILIZER",10],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",4],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",4],["PICKUP","WHEAT",4],["EAST"],["SOUTH"],["EAST"],["WEST"]],"market":[["SELL","MILK",6],["SELL","WHEAT",13],["SELL","STRAWBERRY",1],["SELL","FERTILIZER",1],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["FEED"],["WEST"],["FEED"],["FEED"],["COLLECT_FERTILIZER"],["SOUTH"],["EAST"],["WEST"],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["CARE"],"hands":[["CARE"],["COLLECT_FERTILIZER"],["CARE"],["CARE"],["EAST"],["SOUTH"],["EAST"],["WEST"],["NORTH"],["NORTH"],["SOUTH"],["SOUTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["EAST"],["NORTH"],["COLLECT_FERTILIZER"],["HARVEST"],["WATER"],["WATER"],["COLLECT_FERTILIZER"],["FEED"],["FEED"],["WATER"]],"market":[]},{"farmer":["WEST"],"hands":[["EAST"],["FERTILIZE"],["FEED"],["FEED"],["NORTH"],["WEST"],["HARVEST"],["HARVEST"],["WEST"],["CARE"],["CARE"],["SOUTH"]],"market":[["SELL","WOOL",1]]},{"farmer":["FEED"],"hands":[["FEED"],["WATER"],["CARE"],["CARE"],["FERTILIZE"],["HARVEST"],["PLANT","WHEAT"],["PLANT","WHEAT"],["FERTILIZE"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FERTILIZE"]],"market":[["SELL","WHEAT",5],["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["CARE"],["WEST"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"],["EAST"],["WATER"],["WATER"],["WATER"],["NORTH"],["HARVEST"],["WATER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["FERTILIZE"],["SOUTH"],["FEED"],["NORTH"],["NORTH"],["NORTH"],["NORTH"],["NORTH"],["FEED"],["SOUTH"],["EAST"]],"market":[]},{"farmer":["HARVEST"],"hands":[["FEED"],["WATER"],["WATER"],["CARE"],["FERTILIZE"],["NORTH"],["FEED"],["FEED"],["WATER"],["CARE"],["FEED"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["CARE"],["WEST"],["HARVEST"],["COLLECT_FERTILIZER"],["WATER"],["NORTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["HARVEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["EAST"]],"market":[]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["WATER"],["PLANT","WHEAT"],["NORTH"],["EAST"],["DROP"],["HARVEST"],["HARVEST"],["PLANT","WHEAT"],["NORTH"],["CARE"],["WATER"]],"market":[["SELL","STRAWBERRY",4],["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["SOUTH"],["WATER"],["FERTILIZE"],["WATER"],["WEST"],["CARE"],["CARE"],["WATER"],["FERTILIZE"],["SOUTH"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["COLLECT_FERTILIZER"],["WATER"],["EAST"],["WATER"],["NORTH"],["HARVEST"],["EAST"],["WEST"],["NORTH"],["WATER"],["WATER"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["NORTH"],["HARVEST"],["WATER"],["WEST"],["WATER"],["SOUTH"],["WATER"],["HARVEST"],["FERTILIZE"],["NORTH"],["EAST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["FERTILIZE"],["SOUTH"],["HARVEST"],["WATER"],["NORTH"],["WATER"],["NORTH"],["DIG"],["WATER"],["FERTILIZE"],["FERTILIZE"],["EAST"]],"market":[]},{"farmer":["HARVEST"],"hands":[["WATER"],["HARVEST"],["PLANT","WHEAT"],["WEST"],["WATER"],["WEST"],["FERTILIZE"],["PLANT","WHEAT"],["WEST"],["WATER"],["WATER"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["DIG"],"hands":[["EAST"],["WATER"],["WATER"],["HARVEST"],["EAST"],["WATER"],["WATER"],["WATER"],["HARVEST"],["EAST"],["WEST"],["EAST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PLANT","WHEAT"],"hands":[["FERTILIZE"],["SOUTH"],["NORTH"],["NORTH"],["HARVEST"],["SOUTH"],["WEST"],["NORTH"],["NORTH"],["WATER"],["SOUTH"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WATER"],["HARVEST"],["FERTILIZE"],["HARVEST"],["WATER"],["WATER"],["WEST"],["HARVEST"],["HARVEST"],["HARVEST"],["FERTILIZE"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["NORTH"],["WATER"],["WATER"],["DIG"],["SOUTH"],["HARVEST"],["SOUTH"],["DIG"],["WEST"],["EAST"],["WATER"],["HARVEST"]],"market":[]},{"farmer":["PLANT","WHEAT"],"hands":[["FERTILIZE"],["EAST"],["NORTH"],["PLANT","WHEAT"],["SOUTH"],["PLANT","WHEAT"],["FEED"],["PLANT","WHEAT"],["HARVEST"],["WATER"],["EAST"],["PLANT","WHEAT"]],"market":[["SELL","MILK",3]]},{"farmer":["WATER"],"hands":[["HARVEST"],["HARVEST"],["CARE"],["WATER"],["HARVEST"],["WATER"],["CARE"],["WATER"],["DIG"],["HARVEST"],["EAST"],["WATER"]],"market":[["SELL","EGG",12],["SELL","WHEAT",8]]},{"farmer":["SOUTH"],"hands":[["SOUTH"],["WATER"],["HARVEST"],["SOUTH"],["WATER"],["SOUTH"],["HARVEST"],["SOUTH"],["SOUTH"],["SOUTH"],["WATER"],["NORTH"]],"market":[]},{"farmer":["PICKUP","WHEAT",4],"hands":[],"market":[["SELL","STRAWBERRY",11],["SELL","FERTILIZER",4],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["PICKUP","WHEAT",4],["NORTH"],["WEST"],["EAST"],["NORTH"]],"market":[["SELL","STRAWBERRY",6],["SELL","WOOL",4],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["EAST"],["FEED"],["FEED"],["NORTH"],["NORTH"],["WEST"],["EAST"],["NORTH"],["COLLECT_FERTILIZER"],["EAST"],["PICKUP","WHEAT",3],["SOUTH"]],"market":[["SELL","WHEAT",10],["SELL","STRAWBERRY",5],["SELL","FERTILIZER",1]]},{"farmer":["CARE"],"hands":[["EAST"],["CARE"],["CARE"],["FEED"],["NORTH"],["WATER"],["WATER"],["NORTH"],["WEST"],["NORTH"],["SOUTH"],["WATER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["CARE"],["HARVEST"],["WEST"],["HARVEST"],["HARVEST"],["WEST"],["EAST"],["FEED"],["HARVEST"]],"market":[]},{"farmer":["HARVEST"],"hands":[["EAST"],["WEST"],["EAST"],["COLLECT_FERTILIZER"],["NORTH"],["WATER"],["PLANT","WHEAT"],["WEST"],["COLLECT_FERTILIZER"],["HARVEST"],["CARE"],["PLANT","TOMATO"]],"market":[["SELL","WOOL",1]]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["FEED"],["FEED"],["HARVEST"],["HARVEST"],["HARVEST"],["WATER"],["HARVEST"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["PLANT","WHEAT"]],"market":[]},{"farmer":["FEED"],"hands":[["EAST"],["CARE"],["CARE"],["NORTH"],["EAST"],["PLANT","WHEAT"],["NORTH"],["EAST"],["WEST"],["HARVEST"],["SOUTH"],["WATER"]],"market":[["SELL","WHEAT",10],["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["WATER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["SOUTH"],["WATER"],["FEED"],["SOUTH"],["FERTILIZE"],["NORTH"],["FEED"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["HARVEST"],["SOUTH"],["SOUTH"],["NORTH"],["HARVEST"],["SOUTH"],["CARE"],["SOUTH"],["WATER"],["HARVEST"],["COLLECT_FERTILIZER"],["HARVEST"]],"market":[["SELL","MILK",1],["SELL","WOOL",1]]},{"farmer":["FEED"],"hands":[["PLANT","WHEAT"],["SOUTH"],["SOUTH"],["NORTH"],["SOUTH"],["WATER"],["EAST"],["SOUTH"],["SOUTH"],["EAST"],["HARVEST"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["WATER"],["WATER"],["WATER"],["FERTILIZE"],["SOUTH"],["EAST"],["FEED"],["DROP"],["FERTILIZE"],["HARVEST"],["CARE"],["HARVEST"]],"market":[["SELL","STRAWBERRY",6],["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["SOUTH"],["SOUTH"],["SOUTH"],["WATER"],["SOUTH"],["WATER"],["CARE"],["WEST"],["WATER"],["SOUTH"],["SOUTH"],["WATER"]],"market":[]},{"farmer":["CARE"],"hands":[["FERTILIZE"],["WATER"],["WATER"],["WEST"],["WEST"],["HARVEST"],["NORTH"],["NORTH"],["SOUTH"],["HARVEST"],["WATER"],["NORTH"]],"market":[]},{"farmer":["WEST"],"hands":[["WATER"],["WEST"],["SOUTH"],["FERTILIZE"],["DROP"],["PLANT","WHEAT"],["WATER"],["WATER"],["HARVEST"],["SOUTH"],["SOUTH"],["NORTH"]],"market":[["SELL","STRAWBERRY",6],["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["WEST"],["WATER"],["FERTILIZE"],["WATER"],["NORTH"],["WATER"],["EAST"],["HARVEST"],["WATER"],["SOUTH"],["WATER"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["SOUTH"],["HARVEST"],["WATER"],["WEST"],["COLLECT_FERTILIZER"],["WEST"],["HARVEST"],["PLANT","WHEAT"],["SOUTH"],["WEST"],["EAST"],["DROP"]],"market":[["SELL","STRAWBERRY",4],["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["FERTILIZE"],["SOUTH"],["EAST"],["WEST"],["NORTH"],["SOUTH"],["WATER"],["WATER"],["HARVEST"],["WEST"],["FERTILIZE"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["WATER"],["WATER"],["WATER"],["PLANT","WHEAT"],["COLLECT_FERTILIZER"],["WATER"],["NORTH"],["NORTH"],["WATER"],["WEST"],["WATER"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["SOUTH"],["HARVEST"],["NORTH"],["WATER"],["HARVEST"],["SOUTH"],["WATER"],["NORTH"],["SOUTH"],["DROP"],["WEST"],["WATER"]],"market":[["SELL","STRAWBERRY",6],["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["FERTILIZE"],["FERTILIZE"],["FERTILIZE"],["WEST"],["EAST"],["WATER"],["NORTH"],["WATER"],["SOUTH"],["EAST"],["HARVEST"],["EAST"]],"market":[["SELL","STRAWBERRY",4]]},{"farmer":["WATER"],"hands":[["WATER"],["WEST"],["WATER"],["PLANT","WHEAT"],["DIG"],["SOUTH"],["WATER"],["WEST"],["WATER"],["COLLECT_FERTILIZER"],["PLANT","WHEAT"],["HARVEST"]],"market":[["SELL","MILK",1]]},{"farmer":["WEST"],"hands":[["NORTH"],["WATER"],["NORTH"],["WATER"],["PLANT","WHEAT"],["WATER"],["NORTH"],["DIG"],["HARVEST"],["HARVEST"],["WATER"],["PLANT","WHEAT"]],"market":[["SELL","WHEAT",9],["SELL","TOMATO",3],["SELL","EGG",10]]},{"farmer":["WATER"],"hands":[["EAST"],["HARVEST"],["WATER"],["SOUTH"],["WATER"],["HARVEST"],["WATER"],["SOUTH"],["NORTH"],["NORTH"],["WEST"],["WATER"]],"market":[]},{"farmer":["PICKUP","WHEAT",3],"hands":[],"market":[["SELL","WOOL",8],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",4],["COLLECT_FERTILIZER"],["HARVEST"],["PICKUP","WHEAT",4],["EAST"],["WEST"],["EAST"],["WEST"]],"market":[["SELL","WOOL",4],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["FEED"],["WEST"],["PLACE","WOOL",1000],["FEED"],["COLLECT_FERTILIZER"],["WEST"],["HARVEST"],["WEST"],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["PICKUP","FERTILIZER",3]],"market":[["SELL","WOOL",6]]},{"farmer":["CARE"],"hands":[["CARE"],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",2],["CARE"],["EAST"],["WATER"],["WEST"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"],["SOUTH"],["SOUTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["SOUTH"],["FEED"],["NORTH"],["COLLECT_FERTILIZER"],["HARVEST"],["DROP"],["WEST"],["COLLECT_FERTILIZER"],["FEED"],["FEED"],["SOUTH"]],"market":[["SELL","WOOL",2]]},{"farmer":["WEST"],"hands":[["EAST"],["WATER"],["CARE"],["FEED"],["HARVEST"],["PLANT","WHEAT"],["EAST"],["FERTILIZE"],["NORTH"],["CARE"],["HARVEST"],["WATER"]],"market":[["SELL","WOOL",2],["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["FEED"],["WEST"],["COLLECT_FERTILIZER"],["CARE"],["NORTH"],["WATER"],["COLLECT_FERTILIZER"],["WATER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["CARE"],["SOUTH"]],"market":[]},{"farmer":["CARE"],"hands":[["CARE"],["SOUTH"],["EAST"],["NORTH"],["WATER"],["WEST"],["SOUTH"],["WEST"],["NORTH"],["NORTH"],["COLLECT_FERTILIZER"],["WATER"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["WATER"],["FEED"],["FEED"],["NORTH"],["WEST"],["FERTILIZE"],["WATER"],["WATER"],["FEED"],["SOUTH"],["EAST"]],"market":[]},{"farmer":["FEED"],"hands":[["FEED"],["WEST"],["CARE"],["CARE"],["WATER"],["WATER"],["WATER"],["HARVEST"],["NORTH"],["CARE"],["FEED"],["FERTILIZE"]],"market":[["SELL","WOOL",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["CARE"],["FERTILIZE"],["EAST"],["WEST"],["EAST"],["HARVEST"],["EAST"],["PLANT","WHEAT"],["HARVEST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WATER"]],"market":[["SELL","WHEAT",10],["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["COLLECT_FERTILIZER"],["WATER"],["EAST"],["WATER"],["FERTILIZE"],["PLANT","WHEAT"],["WATER"],["WATER"],["WATER"],["NORTH"],["CARE"],["SOUTH"]],"market":[["SELL","WHEAT",5],["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["EAST"],["HARVEST"],["FERTILIZE"],["NORTH"],["WATER"],["WATER"],["EAST"],["NORTH"],["EAST"],["WATER"],["HARVEST"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["EAST"],["SOUTH"],["WATER"],["WATER"],["NORTH"],["SOUTH"],["WATER"],["WATER"],["WATER"],["EAST"],["SOUTH"],["WATER"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["FERTILIZE"],["HARVEST"],["EAST"],["WEST"],["FERTILIZE"],["HARVEST"],["HARVEST"],["EAST"],["EAST"],["WATER"],["HARVEST"],["EAST"]],"market":[["SELL","WOOL",1]]},{"farmer":["WATER"],"hands":[["WATER"],["FERTILIZE"],["WATER"],["PLANT","WHEAT"],["WATER"],["WATER"],["PLANT","WHEAT"],["FEED"],["FERTILIZE"],["EAST"],["FERTILIZE"],["FERTILIZE"]],"market":[["SELL","STRAWBERRY",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["EAST"],["WATER"],["HARVEST"],["WATER"],["EAST"],["SOUTH"],["WATER"],["CARE"],["WATER"],["WATER"],["WATER"],["WATER"]],"market":[["SELL","STRAWBERRY",1],["SELL","MILK",2],["BUY_SEED","WHEAT",1]]},{"farmer":["FERTILIZE"],"hands":[["WATER"],["WEST"],["PLANT","WHEAT"],["NORTH"],["WATER"],["HARVEST"],["SOUTH"],["COLLECT_FERTILIZER"],["HARVEST"],["EAST"],["WEST"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WEST"],["WATER"],["WATER"],["WATER"],["HARVEST"],["WATER"],["HARVEST"],["HARVEST"],["EAST"],["NORTH"],["HARVEST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["SOUTH"],["HARVEST"],["SOUTH"],["HARVEST"],["PLANT","WHEAT"],["SOUTH"],["WATER"],["WEST"],["WATER"],["FERTILIZE"],["FERTILIZE"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["FEED"],["SOUTH"],["WATER"],["PLANT","WHEAT"],["WATER"],["SOUTH"],["SOUTH"],["HARVEST"],["HARVEST"],["WATER"],["WATER"],["PLANT","WHEAT"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["CARE"],["HARVEST"],["HARVEST"],["WATER"],["SOUTH"],["HARVEST"],["PLANT","WHEAT"],["PLANT","WHEAT"],["EAST"],["HARVEST"],["WEST"],["WATER"]],"market":[["SELL","MILK",6],["SELL","STRAWBERRY",3]]},{"farmer":["PLANT","WHEAT"],"hands":[["COLLECT_FERTILIZER"],["WATER"],["PLANT","WHEAT"],["EAST"],["HARVEST"],["WATER"],["WATER"],["WATER"],["EAST"],["EAST"],["SOUTH"],["NORTH"]],"market":[["SELL","TOMATO",4],["SELL","WHEAT",5],["SELL","EGG",8],["SELL","FERTILIZER",5]]},{"farmer":["WATER"],"hands":[["HARVEST"],["EAST"],["WATER"],["HARVEST"],["WATER"],["EAST"],["SOUTH"],["SOUTH"],["HARVEST"],["HARVEST"],["WATER"],["WATER"]],"market":[]},{"farmer":["PICKUP","WHEAT",3],"hands":[],"market":[["SELL","STRAWBERRY",6],["SELL","TOMATO",4],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["HARVEST"],["HARVEST"],["PICKUP","WHEAT",3],["HARVEST"],["NORTH"],["SOUTH"],["EAST"],["WEST"]],"market":[["SELL","STRAWBERRY",6],["SELL","WHEAT",13],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["PLACE","MILK",1000],["PLACE","MILK",1000],["FEED"],["PLACE","MILK",1000],["HARVEST"],["COLLECT_FERTILIZER"],["EAST"],["WEST"],["COLLECT_FERTILIZER"],["EAST"],["PICKUP","WHEAT",3],["PICKUP","FERTILIZER",3]],"market":[["SELL","WHEAT",10],["SELL","FERTILIZER",4]]},{"farmer":["CARE"],"hands":[["COLLECT_FERTILIZER"],["PICKUP","WHEAT",2],["CARE"],["PICKUP","WHEAT",3],["NORTH"],["HARVEST"],["EAST"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["SOUTH"],["SOUTH"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["FEED"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"],["WEST"],["WATER"],["WATER"],["COLLECT_FERTILIZER"],["EAST"],["FEED"],["FERTILIZE"]],"market":[]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["CARE"],["EAST"],["FEED"],["HARVEST"],["SOUTH"],["HARVEST"],["HARVEST"],["WEST"],["COLLECT_FERTILIZER"],["CARE"],["WATER"]],"market":[["SELL","STRAWBERRY",2],["SELL","MILK",2]]},{"farmer":["FEED"],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["FEED"],["CARE"],["NORTH"],["WATER"],["PLANT","WHEAT"],["PLANT","WHEAT"],["FERTILIZE"],["EAST"],["SOUTH"],["SOUTH"]],"market":[["SELL","WHEAT",4],["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["CARE"],["NORTH"],["HARVEST"],["WEST"],["WATER"],["WATER"],["WATER"],["COLLECT_FERTILIZER"],["FEED"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["EAST"],["FEED"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["EAST"],["WATER"],["NORTH"],["NORTH"],["NORTH"],["EAST"],["COLLECT_FERTILIZER"],["SOUTH"]],"market":[]},{"farmer":["HARVEST"],"hands":[["FERTILIZE"],["CARE"],["EAST"],["FEED"],["SOUTH"],["HARVEST"],["FEED"],["FEED"],["FERTILIZE"],["FERTILIZE"],["CARE"],["HARVEST"]],"market":[["SELL","MILK",6],["SELL","STRAWBERRY",2]]},{"farmer":["WEST"],"hands":[["WATER"],["COLLECT_FERTILIZER"],["FERTILIZE"],["CARE"],["HARVEST"],["PLANT","WHEAT"],["CARE"],["CARE"],["WATER"],["WATER"],["HARVEST"],["FERTILIZE"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["NORTH"],["WEST"],["WATER"],["HARVEST"],["SOUTH"],["WATER"],["NORTH"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["SOUTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","CARROT",6]]},{"farmer":["FERTILIZE"],"hands":[["NORTH"],["SOUTH"],["NORTH"],["NORTH"],["SOUTH"],["WEST"],["WATER"],["HARVEST"],["WATER"],["HARVEST"],["WATER"],["SOUTH"]],"market":[]},{"farmer":["WATER"],"hands":[["WATER"],["FERTILIZE"],["FEED"],["NORTH"],["SOUTH"],["WATER"],["HARVEST"],["EAST"],["HARVEST"],["NORTH"],["WEST"],["WATER"]],"market":[]},{"farmer":["SOUTH"],"hands":[["EAST"],["WATER"],["CARE"],["WATER"],["WEST"],["HARVEST"],["PLANT","WHEAT"],["FEED"],["PLANT","CARROT"],["FERTILIZE"],["WATER"],["HARVEST"]],"market":[["SELL","STRAWBERRY",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["HARVEST"],["SOUTH"],["NORTH"],["WEST"],["DROP"],["SOUTH"],["WATER"],["CARE"],["WATER"],["WATER"],["WEST"],["EAST"]],"market":[["SELL","STRAWBERRY",2],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["DIG"],["WEST"],["HARVEST"],["WATER"],["EAST"],["WATER"],["WEST"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["FERTILIZE"],["WATER"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["HARVEST"],"hands":[["PLANT","WHEAT"],["SOUTH"],["NORTH"],["WEST"],["SOUTH"],["SOUTH"],["DIG"],["HARVEST"],["WATER"],["NORTH"],["WATER"],["NORTH"]],"market":[["SELL","MILK",2]]},{"farmer":["DIG"],"hands":[["WATER"],["WEST"],["HARVEST"],["WEST"],["SOUTH"],["FERTILIZE"],["PLANT","WHEAT"],["EAST"],["HARVEST"],["FERTILIZE"],["HARVEST"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["PLANT","CARROT"],"hands":[["SOUTH"],["FERTILIZE"],["EAST"],["FERTILIZE"],["WATER"],["WATER"],["WATER"],["EAST"],["PLANT","CARROT"],["WATER"],["SOUTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["HARVEST"],["WATER"],["HARVEST"],["WATER"],["EAST"],["HARVEST"],["WEST"],["HARVEST"],["WATER"],["WEST"],["HARVEST"],["NORTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["DIG"],["NORTH"],["DIG"],["WEST"],["WATER"],["WEST"],["COLLECT_FERTILIZER"],["SOUTH"],["NORTH"],["HARVEST"],["WATER"],["FERTILIZE"]],"market":[["SELL","MILK",2],["SELL","STRAWBERRY",2]]},{"farmer":["HARVEST"],"hands":[["PLANT","WHEAT"],["HARVEST"],["PLANT","WHEAT"],["WATER"],["SOUTH"],["WATER"],["HARVEST"],["DROP"],["WATER"],["SOUTH"],["EAST"],["WATER"]],"market":[["SELL","WHEAT",7],["SELL","EGG",10],["SELL","FERTILIZER",2]]},{"farmer":["DIG"],"hands":[["WATER"],["DIG"],["WATER"],["SOUTH"],["WATER"],["HARVEST"],["SOUTH"],["PASS"],["WEST"],["HARVEST"],["DIG"],["SOUTH"]],"market":[["SELL","EGG",10]]},{"farmer":["PICKUP","WHEAT",2],"hands":[],"market":[["SELL","TOMATO",5],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",3],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",2],["PICKUP","WHEAT",3],["EAST"],["WEST"],["SOUTH"],["NORTH"]],"market":[["SELL","WOOL",8],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["FEED"],["WEST"],["FEED"],["FEED"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WATER"],["WEST"],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",2],["PICKUP","WHEAT",2]],"market":[["SELL","FERTILIZER",5],["HIRE"]]},{"farmer":["CARE"],"hands":[["CARE"],["WEST"],["CARE"],["CARE"],["EAST"],["WEST"],["HARVEST"],["WATER"],["NORTH"],["NORTH"],["SOUTH"],["SOUTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["FERTILIZE"],["COLLECT_FERTILIZER"],["NORTH"],["COLLECT_FERTILIZER"],["WEST"],["PLANT","CARROT"],["HARVEST"],["COLLECT_FERTILIZER"],["FEED"],["FEED"],["SOUTH"]],"market":[]},{"farmer":["HARVEST"],"hands":[["EAST"],["WATER"],["EAST"],["FEED"],["EAST"],["WATER"],["WATER"],["PLANT","WHEAT"],["NORTH"],["CARE"],["CARE"],["COLLECT_FERTILIZER"]],"market":[["SELL","STRAWBERRY",2],["SELL","MILK",2],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["FEED"],["SOUTH"],["FEED"],["CARE"],["COLLECT_FERTILIZER"],["HARVEST"],["EAST"],["WATER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["EAST"]],"market":[]},{"farmer":["FEED"],"hands":[["CARE"],["WATER"],["CARE"],["NORTH"],["HARVEST"],["PLANT","WHEAT"],["WATER"],["WEST"],["NORTH"],["NORTH"],["SOUTH"],["FERTILIZE"]],"market":[["SELL","WHEAT",5],["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["NORTH"],["HARVEST"],["COLLECT_FERTILIZER"],["FEED"],["EAST"],["WATER"],["HARVEST"],["FEED"],["FERTILIZE"],["FEED"],["FEED"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FEED"],["PLANT","CARROT"],["EAST"],["CARE"],["WATER"],["WEST"],["PLANT","WHEAT"],["HARVEST"],["WATER"],["CARE"],["CARE"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["CARE"],["WATER"],["WATER"],["WEST"],["HARVEST"],["FERTILIZE"],["WATER"],["CARE"],["WEST"],["COLLECT_FERTILIZER"],["HARVEST"],["WATER"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","CARROT",6]]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["EAST"],["SOUTH"],["WATER"],["PLANT","CARROT"],["WATER"],["NORTH"],["COLLECT_FERTILIZER"],["FERTILIZE"],["NORTH"],["SOUTH"],["EAST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FERTILIZE"],"hands":[["NORTH"],["WATER"],["WATER"],["HARVEST"],["WATER"],["SOUTH"],["WEST"],["WEST"],["WATER"],["DIG"],["HARVEST"],["WATER"]],"market":[]},{"farmer":["WATER"],"hands":[["WATER"],["SOUTH"],["HARVEST"],["PLANT","CARROT"],["SOUTH"],["SOUTH"],["DROP"],["FEED"],["HARVEST"],["PLANT","CARROT"],["WATER"],["EAST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["EAST"],["WATER"],["PLANT","CARROT"],["WATER"],["FERTILIZE"],["PLANT","CARROT"],["SOUTH"],["CARE"],["WEST"],["WATER"],["SOUTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["FERTILIZE"],"hands":[["FERTILIZE"],["WEST"],["WATER"],["SOUTH"],["WATER"],["WATER"],["EAST"],["COLLECT_FERTILIZER"],["FERTILIZE"],["NORTH"],["DIG"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1],["BUY_SEED","CARROT",6]]},{"farmer":["WATER"],"hands":[["WATER"],["SOUTH"],["EAST"],["SOUTH"],["SOUTH"],["SOUTH"],["SOUTH"],["HARVEST"],["WATER"],["DIG"],["PLANT","CARROT"],["WATER"]],"market":[["SELL","MILK",2]]},{"farmer":["NORTH"],"hands":[["EAST"],["WATER"],["FERTILIZE"],["EAST"],["FERTILIZE"],["HARVEST"],["WATER"],["SOUTH"],["NORTH"],["PLANT","WHEAT"],["WATER"],["HARVEST"]],"market":[["SELL","MILK",2]]},{"farmer":["WATER"],"hands":[["EAST"],["WEST"],["WATER"],["DROP"],["WATER"],["WATER"],["EAST"],["SOUTH"],["WATER"],["WATER"],["WEST"],["EAST"]],"market":[]},{"farmer":["NORTH"],"hands":[["HARVEST"],["HARVEST"],["SOUTH"],["NORTH"],["WEST"],["SOUTH"],["WATER"],["SOUTH"],["WEST"],["EAST"],["PLANT","CARROT"],["PLANT","CARROT"]],"market":[["SELL","WHEAT",24]]},{"farmer":["DIG"],"hands":[["NORTH"],["WATER"],["FERTILIZE"],["NORTH"],["NORTH"],["HARVEST"],["HARVEST"],["SOUTH"],["WATER"],["HARVEST"],["WATER"],["WATER"]],"market":[]},{"farmer":["PLANT","WHEAT"],"hands":[["FERTILIZE"],["SOUTH"],["WATER"],["NORTH"],["NORTH"],["DIG"],["PLANT","CARROT"],["WATER"],["HARVEST"],["DIG"],["WEST"],["NORTH"]],"market":[["SELL","MILK",8],["SELL","STRAWBERRY",2]]},{"farmer":["WATER"],"hands":[["WATER"],["WATER"],["HARVEST"],["HARVEST"],["FEED"],["PLANT","CARROT"],["WATER"],["HARVEST"],["PLANT","WHEAT"],["PLANT","WHEAT"],["FERTILIZE"],["WATER"]],"market":[["SELL","WHEAT",1],["SELL","EGG",4]]},{"farmer":["NORTH"],"hands":[["NORTH"],["WEST"],["NORTH"],["NORTH"],["CARE"],["WATER"],["SOUTH"],["NORTH"],["WATER"],["WATER"],["WATER"],["SOUTH"]],"market":[["SELL","STRAWBERRY",3]]},{"farmer":["NORTH"],"hands":[],"market":[["SELL","TOMATO",3],["SELL","WOOL",4],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["HARVEST"],"hands":[["PICKUP","WHEAT",3],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",2],["HARVEST"],["WEST"],["EAST"],["SOUTH"],["EAST"]],"market":[["SELL","STRAWBERRY",3],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["SOUTH"],"hands":[["WEST"],["NORTH"],["FEED"],["PLACE","WOOL",1000],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["HARVEST"],["HARVEST"],["COLLECT_FERTILIZER"],["NORTH"],["PICKUP","WHEAT",2]],"market":[["SELL","WOOL",4]]},{"farmer":["DROP"],"hands":[["FEED"],["COLLECT_FERTILIZER"],["CARE"],["PICKUP","WHEAT",2],["WEST"],["EAST"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["EAST"],["SOUTH"]],"market":[["SELL","WOOL",4]]},{"farmer":["PICKUP","WHEAT",2],"hands":[["CARE"],["NORTH"],["COLLECT_FERTILIZER"],["FEED"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WEST"],["PLACE","WOOL",1000],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["FEED"]],"market":[["SELL","WOOL",4]]},{"farmer":["NORTH"],"hands":[["WEST"],["COLLECT_FERTILIZER"],["WEST"],["CARE"],["WEST"],["HARVEST"],["FERTILIZE"],["EAST"],["NORTH"],["NORTH"],["CARE"]],"market":[["SELL","STRAWBERRY",3]]},{"farmer":["FEED"],"hands":[["FEED"],["HARVEST"],["FEED"],["COLLECT_FERTILIZER"],["FERTILIZE"],["SOUTH"],["WATER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WATER"],["SOUTH"]],"market":[]},{"farmer":["CARE"],"hands":[["CARE"],["EAST"],["CARE"],["EAST"],["WATER"],["WATER"],["WEST"],["SOUTH"],["NORTH"],["HARVEST"],["FEED"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["EAST"],["COLLECT_FERTILIZER"],["FEED"],["WEST"],["HARVEST"],["SOUTH"],["SOUTH"],["NORTH"],["PLANT","WHEAT"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["WEST"],"hands":[["FEED"],["HARVEST"],["WEST"],["CARE"],["WATER"],["PLANT","WHEAT"],["WATER"],["WATER"],["FERTILIZE"],["WATER"],["CARE"]],"market":[["SELL","STRAWBERRY",2],["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["NORTH"],["WATER"],["EAST"],["HARVEST"],["WATER"],["WEST"],["HARVEST"],["WATER"],["SOUTH"],["HARVEST"]],"market":[]},{"farmer":["HARVEST"],"hands":[["WATER"],["FERTILIZE"],["WEST"],["EAST"],["PLANT","CARROT"],["NORTH"],["HARVEST"],["PLANT","CARROT"],["WEST"],["HARVEST"],["SOUTH"]],"market":[["SELL","WHEAT",8],["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["NORTH"],["WATER"],["SOUTH"],["FERTILIZE"],["WATER"],["FEED"],["DIG"],["WATER"],["FERTILIZE"],["EAST"],["FERTILIZE"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["WATER"],["NORTH"],["FERTILIZE"],["WATER"],["SOUTH"],["CARE"],["PLANT","WHEAT"],["EAST"],["WATER"],["FERTILIZE"],["WATER"]],"market":[["SELL","STRAWBERRY",2],["SELL","WOOL",1],["BUY_SEED","WHEAT",1]]},{"farmer":["FEED"],"hands":[["HARVEST"],["FERTILIZE"],["WATER"],["EAST"],["WATER"],["EAST"],["WATER"],["SOUTH"],["HARVEST"],["WATER"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["PLANT","WHEAT"],["WATER"],["SOUTH"],["WATER"],["HARVEST"],["FEED"],["SOUTH"],["FERTILIZE"],["WEST"],["SOUTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["WATER"],["EAST"],["SOUTH"],["HARVEST"],["PLANT","WHEAT"],["CARE"],["WATER"],["WATER"],["FERTILIZE"],["WEST"],["HARVEST"]],"market":[["SELL","WHEAT",5],["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["WEST"],["DIG"],["FERTILIZE"],["PLANT","WHEAT"],["WATER"],["COLLECT_FERTILIZER"],["WEST"],["EAST"],["WATER"],["HARVEST"],["EAST"]],"market":[["SELL","STRAWBERRY",2],["BUY_SEED","WHEAT",1],["BUY_SEED","CARROT",6]]},{"farmer":["NORTH"],"hands":[["WATER"],["PLANT","WHEAT"],["SOUTH"],["WATER"],["SOUTH"],["NORTH"],["WATER"],["WATER"],["WEST"],["WEST"],["EAST"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["SOUTH"],["WATER"],["HARVEST"],["SOUTH"],["FERTILIZE"],["FERTILIZE"],["SOUTH"],["HARVEST"],["WEST"],["DROP"],["SOUTH"]],"market":[]},{"farmer":["WEST"],"hands":[["WATER"],["SOUTH"],["WATER"],["WATER"],["WATER"],["WATER"],["WATER"],["PLANT","CARROT"],["WATER"],["EAST"],["WATER"]],"market":[["SELL","WHEAT",12],["SELL","FERTILIZER",5]]},{"farmer":["FERTILIZE"],"hands":[["HARVEST"],["SOUTH"],["EAST"],["WEST"],["HARVEST"],["NORTH"],["NORTH"],["WATER"],["HARVEST"],["EAST"],["EAST"]],"market":[["SELL","MILK",6],["SELL","STRAWBERRY",2]]},{"farmer":["WATER"],"hands":[["PLANT","WHEAT"],["FERTILIZE"],["HARVEST"],["WATER"],["PLANT","CARROT"],["FERTILIZE"],["NORTH"],["NORTH"],["PLANT","WHEAT"],["WEST"],["WATER"]],"market":[["SELL","WHEAT",1],["SELL","EGG",10]]},{"farmer":["NORTH"],"hands":[["WATER"],["WATER"],["WATER"],["HARVEST"],["WATER"],["WATER"],["WATER"],["WATER"],["WATER"],["EAST"],["HARVEST"]],"market":[["SELL","STRAWBERRY",3]]},{"farmer":["PICKUP","WHEAT",2],"hands":[],"market":[["SELL","TOMATO",2],["SELL","WHEAT",16],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["PICKUP","WHEAT",3],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",2],["PICKUP","WHEAT",3],["EAST"],["WEST"],["EAST"],["WEST"]],"market":[["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["FEED"],["WEST"],["FEED"],["FEED"],["COLLECT_FERTILIZER"],["HARVEST"],["EAST"],["WEST"],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",2],["PICKUP","WHEAT",2]],"market":[["HIRE"]]},{"farmer":["CARE"],"hands":[["CARE"],["COLLECT_FERTILIZER"],["CARE"],["CARE"],["EAST"],["WEST"],["EAST"],["WEST"],["NORTH"],["NORTH"],["SOUTH"],["SOUTH"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["COLLECT_FERTILIZER"],["NORTH"],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["WATER"],["COLLECT_FERTILIZER"],["FEED"],["FEED"],["SOUTH"]],"market":[]},{"farmer":["WEST"],"hands":[["EAST"],["WEST"],["EAST"],["FEED"],["NORTH"],["HARVEST"],["HARVEST"],["HARVEST"],["WEST"],["CARE"],["CARE"],["COLLECT_FERTILIZER"]],"market":[["SELL","STRAWBERRY",3],["SELL","MILK",1],["SELL","WOOL",1]]},{"farmer":["FEED"],"hands":[["FEED"],["FERTILIZE"],["FEED"],["CARE"],["WATER"],["PLANT","WHEAT"],["PLANT","WHEAT"],["PLANT","WHEAT"],["FERTILIZE"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["SOUTH"]],"market":[["SELL","WHEAT",8],["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["CARE"],["WATER"],["CARE"],["NORTH"],["HARVEST"],["WATER"],["WATER"],["WATER"],["WATER"],["NORTH"],["SOUTH"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["CARE"],"hands":[["NORTH"],["SOUTH"],["COLLECT_FERTILIZER"],["FEED"],["PLANT","WHEAT"],["EAST"],["NORTH"],["NORTH"],["NORTH"],["FEED"],["FEED"],["DIG"]],"market":[["SELL","CARROT",6],["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["FEED"],["WATER"],["SOUTH"],["CARE"],["WATER"],["EAST"],["FEED"],["FEED"],["WATER"],["CARE"],["CARE"],["PLANT","CARROT"]],"market":[["SELL","STRAWBERRY",2],["SELL","MILK",1],["BUY_SEED","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["CARE"],["HARVEST"],["FERTILIZE"],["COLLECT_FERTILIZER"],["NORTH"],["DROP"],["HARVEST"],["CARE"],["WEST"],["COLLECT_FERTILIZER"],["HARVEST"],["WATER"]],"market":[]},{"farmer":["SOUTH"],"hands":[["COLLECT_FERTILIZER"],["SOUTH"],["WATER"],["NORTH"],["DIG"],["WEST"],["CARE"],["COLLECT_FERTILIZER"],["WATER"],["NORTH"],["WEST"],["SOUTH"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["EAST"],["SOUTH"],["EAST"],["WATER"],["PLANT","WHEAT"],["SOUTH"],["COLLECT_FERTILIZER"],["HARVEST"],["HARVEST"],["FERTILIZE"],["FERTILIZE"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["EAST"],["HARVEST"],["FERTILIZE"],["WEST"],["WATER"],["WATER"],["EAST"],["WEST"],["PLANT","CARROT"],["WATER"],["WATER"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["WATER"],["SOUTH"],["WATER"],["WATER"],["NORTH"],["HARVEST"],["FERTILIZE"],["WATER"],["WATER"],["NORTH"],["SOUTH"],["FERTILIZE"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["NORTH"],["FERTILIZE"],["SOUTH"],["HARVEST"],["WATER"],["EAST"],["WATER"],["HARVEST"],["WEST"],["FERTILIZE"],["HARVEST"],["WATER"]],"market":[]},{"farmer":["WATER"],"hands":[["WATER"],["WATER"],["WATER"],["WEST"],["HARVEST"],["EAST"],["WEST"],["PLANT","WHEAT"],["NORTH"],["WATER"],["DIG"],["WEST"]],"market":[["SELL","MILK",2],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["EAST"],["WEST"],["SOUTH"],["NORTH"],["PLANT","WHEAT"],["WATER"],["WEST"],["WATER"],["FERTILIZE"],["EAST"],["PLANT","CARROT"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["NORTH"],["WATER"],["WATER"],["WATER"],["WATER"],["SOUTH"],["FEED"],["NORTH"],["WATER"],["WATER"],["WATER"],["NORTH"]],"market":[]},{"farmer":["WATER"],"hands":[["WATER"],["HARVEST"],["HARVEST"],["HARVEST"],["EAST"],["WATER"],["CARE"],["WATER"],["WEST"],["EAST"],["EAST"],["WATER"]],"market":[]},{"farmer":["SOUTH"],"hands":[["HARVEST"],["PLANT","CARROT"],["SOUTH"],["PLANT","WHEAT"],["DIG"],["SOUTH"],["WEST"],["HARVEST"],["WATER"],["WATER"],["EAST"],["HARVEST"]],"market":[]},{"farmer":["HARVEST"],"hands":[["PLANT","WHEAT"],["WATER"],["WATER"],["WATER"],["PLANT","WHEAT"],["WATER"],["WEST"],["PLANT","WHEAT"],["EAST"],["HARVEST"],["EAST"],["WEST"]],"market":[["SELL","MILK",6],["SELL","STRAWBERRY",2]]},{"farmer":["DIG"],"hands":[["WATER"],["NORTH"],["EAST"],["WEST"],["WATER"],["EAST"],["DROP"],["WATER"],["NORTH"],["PLANT","WHEAT"],["WATER"],["DIG"]],"market":[["SELL","WHEAT",12],["SELL","EGG",16],["SELL","FERTILIZER",1]]},{"farmer":["SOUTH"],"hands":[["FERTILIZE"],["SOUTH"],["WATER"],["WATER"],["FERTILIZE"],["SOUTH"],["PASS"],["SOUTH"],["WATER"],["WATER"],["SOUTH"],["PASS"]],"market":[]},{"farmer":["PICKUP","WHEAT",2],"hands":[],"market":[["SELL","WHEAT",16],["SELL","TOMATO",4],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["HARVEST"],["PICKUP","WHEAT",2],["PICKUP","WHEAT",2],["HARVEST"],["NORTH"],["SOUTH"],["SOUTH"],["NORTH"]],"market":[["SELL","WOOL",4],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["FEED"],"hands":[["PLACE","MILK",1000],["FEED"],["FEED"],["PLACE","MILK",1000],["HARVEST"],["HARVEST"],["WATER"],["WEST"],["COLLECT_FERTILIZER"],["EAST"],["PICKUP","WHEAT",2]],"market":[["SELL","WHEAT",10]]},{"farmer":["CARE"],"hands":[["COLLECT_FERTILIZER"],["CARE"],["CARE"],["PICKUP","WHEAT",3],["NORTH"],["WEST"],["HARVEST"],["WATER"],["NORTH"],["COLLECT_FERTILIZER"],["SOUTH"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["NORTH"],["COLLECT_FERTILIZER"],["HARVEST"],["PLANT","CARROT"],["HARVEST"],["COLLECT_FERTILIZER"],["EAST"],["FEED"]],"market":[]},{"farmer":["HARVEST"],"hands":[["COLLECT_FERTILIZER"],["WEST"],["EAST"],["FEED"],["NORTH"],["WATER"],["WATER"],["PLANT","WHEAT"],["NORTH"],["COLLECT_FERTILIZER"],["CARE"]],"market":[["SELL","MILK",2],["SELL","STRAWBERRY",2],["SELL","WOOL",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["EAST"],["FEED"],["FEED"],["CARE"],["WATER"],["WEST"],["SOUTH"],["WATER"],["COLLECT_FERTILIZER"],["EAST"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["FEED"],"hands":[["COLLECT_FERTILIZER"],["CARE"],["CARE"],["WEST"],["HARVEST"],["WATER"],["HARVEST"],["WEST"],["NORTH"],["COLLECT_FERTILIZER"],["SOUTH"]],"market":[]},{"farmer":["CARE"],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["NORTH"],["PLANT","WHEAT"],["HARVEST"],["SOUTH"],["FEED"],["HARVEST"],["EAST"],["FEED"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FERTILIZE"],["SOUTH"],["EAST"],["WATER"],["WATER"],["PLANT","WHEAT"],["HARVEST"],["HARVEST"],["NORTH"],["WATER"],["COLLECT_FERTILIZER"]],"market":[["SELL","MILK",6],["SELL","STRAWBERRY",2],["SELL","WOOL",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["WATER"],["SOUTH"],["FERTILIZE"],["HARVEST"],["NORTH"],["WATER"],["DIG"],["CARE"],["WATER"],["HARVEST"],["CARE"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["EAST"],["WATER"],["WATER"],["PLANT","WHEAT"],["WATER"],["WEST"],["PLANT","WHEAT"],["COLLECT_FERTILIZER"],["WEST"],["PLANT","WHEAT"],["SOUTH"]],"market":[["SELL","WHEAT",4],["BUY_SEED","WHEAT",1]]},{"farmer":["FERTILIZE"],"hands":[["EAST"],["WEST"],["SOUTH"],["WATER"],["EAST"],["WATER"],["WATER"],["WEST"],["WATER"],["WATER"],["SOUTH"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WATER"],["WATER"],["WATER"],["NORTH"],["FERTILIZE"],["HARVEST"],["NORTH"],["FEED"],["WEST"],["SOUTH"],["WATER"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["HARVEST"],["HARVEST"],["HARVEST"],["HARVEST"],["WATER"],["NORTH"],["NORTH"],["CARE"],["WEST"],["FERTILIZE"],["HARVEST"]],"market":[]},{"farmer":["FERTILIZE"],"hands":[["SOUTH"],["PLANT","WHEAT"],["SOUTH"],["DIG"],["SOUTH"],["WATER"],["NORTH"],["COLLECT_FERTILIZER"],["FERTILIZE"],["WATER"],["WEST"]],"market":[["SELL","WHEAT",6],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WATER"],["WATER"],["WATER"],["PLANT","WHEAT"],["DIG"],["EAST"],["DROP"],["NORTH"],["WATER"],["WEST"],["WATER"]],"market":[["SELL","STRAWBERRY",2],["BUY_SEED","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["HARVEST"],["WEST"],["HARVEST"],["WATER"],["PLANT","WHEAT"],["EAST"],["EAST"],["FERTILIZE"],["WEST"],["SOUTH"],["HARVEST"]],"market":[["SELL","STRAWBERRY",2],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["PLANT","WHEAT"],["FERTILIZE"],["WEST"],["WEST"],["WATER"],["EAST"],["SOUTH"],["WATER"],["FERTILIZE"],["SOUTH"],["WEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["SOUTH"],"hands":[["WATER"],["WATER"],["FERTILIZE"],["WATER"],["EAST"],["DROP"],["WATER"],["NORTH"],["WATER"],["FERTILIZE"],["HARVEST"]],"market":[["SELL","CARROT",12]]},{"farmer":["WATER"],"hands":[["SOUTH"],["SOUTH"],["WATER"],["SOUTH"],["EAST"],["HARVEST"],["EAST"],["WATER"],["SOUTH"],["WATER"],["WEST"]],"market":[]},{"farmer":["HARVEST"],"hands":[["FEED"],["EAST"],["SOUTH"],["SOUTH"],["NORTH"],["DROP"],["PLANT","WHEAT"],["HARVEST"],["FERTILIZE"],["SOUTH"],["HARVEST"]],"market":[["SELL","STRAWBERRY",2],["SELL","MILK",4]]},{"farmer":["PLANT","WHEAT"],"hands":[["CARE"],["HARVEST"],["SOUTH"],["NORTH"],["WATER"],["PASS"],["WATER"],["EAST"],["WATER"],["FERTILIZE"],["WEST"]],"market":[["SELL","TOMATO",4],["SELL","WHEAT",1],["SELL","EGG",7],["SELL","FERTILIZER",3]]},{"farmer":["WATER"],"hands":[["SOUTH"],["DIG"],["WATER"],["WATER"],["SOUTH"],["PASS"],["EAST"],["FERTILIZE"],["SOUTH"],["WATER"],["FERTILIZE"]],"market":[["SELL","STRAWBERRY",3]]},{"farmer":["NORTH"],"hands":[],"market":[["SELL","TOMATO",2],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["HARVEST"],"hands":[["PICKUP","WHEAT",3],["PICKUP","WHEAT",3],["COLLECT_FERTILIZER"],["HARVEST"],["NORTH"],["EAST"],["SOUTH"],["EAST"]],"market":[["SELL","WOOL",4],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["SOUTH"],"hands":[["FEED"],["FEED"],["WEST"],["PLACE","WOOL",1000],["NORTH"],["COLLECT_FERTILIZER"],["SOUTH"],["HARVEST"],["COLLECT_FERTILIZER"],["PICKUP","WHEAT",2],["PICKUP","FERTILIZER",3]],"market":[["SELL","WOOL",4]]},{"farmer":["DROP"],"hands":[["CARE"],["CARE"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["HARVEST"],["EAST"],["COLLECT_FERTILIZER"],["WEST"],["WEST"],["NORTH"],["SOUTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["WEST"],["EAST"],["SOUTH"],["COLLECT_FERTILIZER"],["HARVEST"],["DROP"],["COLLECT_FERTILIZER"],["FEED"],["COLLECT_FERTILIZER"]],"market":[]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["EAST"],["FERTILIZE"],["COLLECT_FERTILIZER"],["SOUTH"],["HARVEST"],["WEST"],["SOUTH"],["WEST"],["CARE"],["SOUTH"]],"market":[["SELL","WOOL",1]]},{"farmer":["NORTH"],"hands":[["FEED"],["FEED"],["WATER"],["EAST"],["PLACE","MILK",1000],["NORTH"],["WATER"],["EAST"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["SOUTH"]],"market":[]},{"farmer":["NORTH"],"hands":[["CARE"],["CARE"],["WEST"],["WATER"],["NORTH"],["FERTILIZE"],["HARVEST"],["WATER"],["WEST"],["NORTH"],["FERTILIZE"]],"market":[]},{"farmer":["DIG"],"hands":[["COLLECT_FERTILIZER"],["NORTH"],["WATER"],["EAST"],["WEST"],["WATER"],["NORTH"],["HARVEST"],["FERTILIZE"],["FEED"],["WATER"]],"market":[]},{"farmer":["PLANT","WHEAT"],"hands":[["WEST"],["FEED"],["HARVEST"],["FERTILIZE"],["WEST"],["NORTH"],["FERTILIZE"],["SOUTH"],["WATER"],["CARE"],["WEST"]],"market":[["SELL","CARROT",27],["SELL","WOOL",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["WEST"],["CARE"],["PLANT","WHEAT"],["WATER"],["COLLECT_FERTILIZER"],["FERTILIZE"],["WATER"],["WATER"],["WEST"],["COLLECT_FERTILIZER"],["FERTILIZE"]],"market":[["SELL","WHEAT",4],["BUY_SEED","WHEAT",1]]},{"farmer":["NORTH"],"hands":[["FERTILIZE"],["COLLECT_FERTILIZER"],["WATER"],["EAST"],["WEST"],["WATER"],["HARVEST"],["HARVEST"],["WATER"],["NORTH"],["WATER"]],"market":[["SELL","WOOL",1],["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["WATER"],["NORTH"],["SOUTH"],["WATER"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"],["SOUTH"],["HARVEST"],["NORTH"],["EAST"]],"market":[["SELL","WOOL",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["NORTH"],["WATER"],["FERTILIZE"],["HARVEST"],["HARVEST"],["WATER"],["EAST"],["WATER"],["PLANT","WHEAT"],["WATER"],["SOUTH"]],"market":[["SELL","STRAWBERRY",2],["SELL","WOOL",1],["BUY_SEED","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["WATER"],["NORTH"],["WATER"],["PLANT","WHEAT"],["WEST"],["EAST"],["DROP"],["HARVEST"],["WATER"],["HARVEST"],["EAST"]],"market":[["SELL","WOOL",1],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["WEST"],["NORTH"],["HARVEST"],["WATER"],["FERTILIZE"],["WATER"],["SOUTH"],["NORTH"],["SOUTH"],["PLANT","WHEAT"],["EAST"]],"market":[["SELL","WOOL",1],["BUY_SEED","WHEAT",1]]},{"farmer":["FERTILIZE"],"hands":[["WATER"],["WATER"],["NORTH"],["WEST"],["WATER"],["EAST"],["HARVEST"],["NORTH"],["WATER"],["WATER"],["HARVEST"]],"market":[["BUY_SEED","WHEAT",1]]},{"farmer":["WATER"],"hands":[["HARVEST"],["HARVEST"],["EAST"],["NORTH"],["NORTH"],["WATER"],["SOUTH"],["NORTH"],["SOUTH"],["SOUTH"],["EAST"]],"market":[["SELL","WHEAT",10],["BUY_SEED","WHEAT",1]]},{"farmer":["WEST"],"hands":[["SOUTH"],["PLANT","WHEAT"],["EAST"],["HARVEST"],["FERTILIZE"],["NORTH"],["EAST"],["WEST"],["WATER"],["SOUTH"],["FERTILIZE"]],"market":[]},{"farmer":["WATER"],"hands":[["WATER"],["WATER"],["EAST"],["FEED"],["WATER"],["DIG"],["SOUTH"],["DROP"],["HARVEST"],["SOUTH"],["WATER"]],"market":[]},{"farmer":["HARVEST"],"hands":[["SOUTH"],["EAST"],["DROP"],["CARE"],["NORTH"],["WEST"],["EAST"],["SOUTH"],["SOUTH"],["SOUTH"],["HARVEST"]],"market":[]},{"farmer":["WEST"],"hands":[["FEED"],["FERTILIZE"],["SOUTH"],["COLLECT_FERTILIZER"],["WATER"],["WATER"],["EAST"],["SOUTH"],["SOUTH"],["DROP"],["NORTH"]],"market":[["SELL","MILK",6],["SELL","STRAWBERRY",2]]},{"farmer":["WATER"],"hands":[["CARE"],["WATER"],["SOUTH"],["WEST"],["HARVEST"],["HARVEST"],["EAST"],["SOUTH"],["SOUTH"],["EAST"],["EAST"]],"market":[["SELL","WHEAT",18],["SELL","TOMATO",8],["SELL","EGG",7],["SELL","FERTILIZER",3]]},{"farmer":["HARVEST"],"hands":[["PASS"],["SOUTH"],["CARE"],["FEED"],["SOUTH"],["SOUTH"],["HARVEST"],["WATER"],["WATER"],["EAST"],["HARVEST"]],"market":[["SELL","STRAWBERRY",3],["SELL","WHEAT",1],["SELL","CARROT",4],["SELL","MILK",1]]},{"farmer":["HARVEST"],"hands":[],"market":[["SELL","WHEAT",16],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["PLACE","MILK",1000],"hands":[["COLLECT_FERTILIZER"],["PICKUP","WHEAT",2],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["NORTH"],["SOUTH"],["EAST"],["WEST"]],"market":[["SELL","WOOL",1],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["WEST"],"hands":[["EAST"],["FEED"],["EAST"],["NORTH"],["HARVEST"],["SOUTH"],["EAST"],["WEST"],["EAST"],["PICKUP","FERTILIZER",3],["PICKUP","FERTILIZER",3]],"market":[["SELL","WHEAT",8],["SELL","FERTILIZER",1]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["NORTH"],["CARE"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["NORTH"],["COLLECT_FERTILIZER"],["WATER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["SOUTH"],["SOUTH"]],"market":[]},{"farmer":["HARVEST"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["EAST"],["NORTH"],["HARVEST"],["HARVEST"],["HARVEST"],["HARVEST"],["EAST"],["COLLECT_FERTILIZER"],["FERTILIZE"]],"market":[]},{"farmer":["NORTH"],"hands":[["NORTH"],["WEST"],["SOUTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["SOUTH"],["EAST"],["WEST"],["COLLECT_FERTILIZER"],["WEST"],["WATER"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["FERTILIZE"],"hands":[["WATER"],["FEED"],["FERTILIZE"],["WEST"],["NORTH"],["WATER"],["WATER"],["WATER"],["HARVEST"],["HARVEST"],["SOUTH"]],"market":[]},{"farmer":["WATER"],"hands":[["HARVEST"],["CARE"],["WATER"],["FERTILIZE"],["FERTILIZE"],["HARVEST"],["HARVEST"],["HARVEST"],["NORTH"],["WEST"],["SOUTH"]],"market":[]},{"farmer":["WEST"],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["SOUTH"],["WATER"],["WATER"],["WEST"],["NORTH"],["WEST"],["WATER"],["FERTILIZE"],["FERTILIZE"]],"market":[["SELL","WHEAT",3],["SELL","CARROT",9]]},{"farmer":["COLLECT_FERTILIZER"],"hands":[["FERTILIZE"],["WEST"],["SOUTH"],["NORTH"],["WEST"],["WATER"],["HARVEST"],["SOUTH"],["EAST"],["WATER"],["WATER"]],"market":[["SELL","STRAWBERRY",2],["SELL","MILK",1],["SELL","WOOL",1]]},{"farmer":["HARVEST"],"hands":[["WATER"],["WATER"],["SOUTH"],["FERTILIZE"],["SOUTH"],["HARVEST"],["COLLECT_FERTILIZER"],["WATER"],["FERTILIZE"],["SOUTH"],["EAST"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["NORTH"],"hands":[["EAST"],["WEST"],["WATER"],["WATER"],["HARVEST"],["NORTH"],["WEST"],["HARVEST"],["WATER"],["FERTILIZE"],["HARVEST"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["WATER"],"hands":[["FERTILIZE"],["SOUTH"],["EAST"],["WEST"],["SOUTH"],["FERTILIZE"],["WEST"],["EAST"],["NORTH"],["WATER"],["WATER"]],"market":[["SELL","STRAWBERRY",2],["SELL","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["WATER"],["HARVEST"],["WEST"],["WATER"],["SOUTH"],["WATER"],["HARVEST"],["EAST"],["NORTH"],["WEST"],["NORTH"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["WEST"],"hands":[["SOUTH"],["WEST"],["EAST"],["HARVEST"],["DROP"],["HARVEST"],["WEST"],["EAST"],["WATER"],["WATER"],["NORTH"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["WATER"],"hands":[["WATER"],["SOUTH"],["NORTH"],["NORTH"],["NORTH"],["NORTH"],["DROP"],["EAST"],["HARVEST"],["HARVEST"],["EAST"]],"market":[["SELL","WHEAT",1],["SELL","STRAWBERRY",2]]},{"farmer":["HARVEST"],"hands":[["HARVEST"],["FERTILIZE"],["EAST"],["WATER"],["WEST"],["NORTH"],["NORTH"],["DROP"],["EAST"],["NORTH"],["EAST"]],"market":[["SELL","WHEAT",21],["SELL","FERTILIZER",2]]},{"farmer":["NORTH"],"hands":[["SOUTH"],["WATER"],["NORTH"],["HARVEST"],["WEST"],["EAST"],["COLLECT_FERTILIZER"],["SOUTH"],["WATER"],["NORTH"],["EAST"]],"market":[["SELL","WHEAT",1],["SELL","STRAWBERRY",2]]},{"farmer":["FERTILIZE"],"hands":[["HARVEST"],["SOUTH"],["NORTH"],["SOUTH"],["WEST"],["DROP"],["NORTH"],["HARVEST"],["HARVEST"],["FERTILIZE"],["NORTH"]],"market":[["SELL","WHEAT",1]]},{"farmer":["WATER"],"hands":[["SOUTH"],["SOUTH"],["NORTH"],["SOUTH"],["COLLECT_FERTILIZER"],["HARVEST"],["NORTH"],["NORTH"],["WEST"],["EAST"],["NORTH"]],"market":[["SELL","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["WEST"],["WATER"],["FERTILIZE"],["SOUTH"],["HARVEST"],["DROP"],["NORTH"],["DROP"],["NORTH"],["EAST"],["WATER"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["WEST"],"hands":[["WEST"],["HARVEST"],["WATER"],["FEED"],["WEST"],["SOUTH"],["FERTILIZE"],["SOUTH"],["WEST"],["EAST"],["HARVEST"]],"market":[["SELL","MILK",6],["SELL","STRAWBERRY",2],["SELL","WOOL",4]]},{"farmer":["SOUTH"],"hands":[["DROP"],["NORTH"],["SOUTH"],["CARE"],["WATER"],["WEST"],["EAST"],["WEST"],["WATER"],["DROP"],["WEST"]],"market":[["SELL","TOMATO",6],["SELL","WHEAT",21],["SELL","CARROT",8],["SELL","EGG",18],["SELL","FERTILIZER",1]]},{"farmer":["WATER"],"hands":[["NORTH"],["SOUTH"],["SOUTH"],["WEST"],["HARVEST"],["WEST"],["WATER"],["WEST"],["HARVEST"],["PASS"],["FEED"]],"market":[]},{"farmer":["NORTH"],"hands":[],"market":[["SELL","WHEAT",16],["SELL","FERTILIZER",4],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["NORTH"],["NORTH"],["NORTH"],["WEST"],["SOUTH"]],"market":[["SELL","MILK",6],["SELL","FERTILIZER",1],["HIRE"],["HIRE"]]},{"farmer":["NORTH"],"hands":[["PLACE","FERTILIZER",1000],["PLACE","FERTILIZER",1000],["WEST"],["EAST"],["NORTH"],["NORTH"],["WEST"],["WATER"],["NORTH"],["NORTH"]],"market":[["SELL","WHEAT",13],["SELL","FERTILIZER",1]]},{"farmer":["WEST"],"hands":[["NORTH"],["NORTH"],["COLLECT_FERTILIZER"],["COLLECT_FERTILIZER"],["WEST"],["NORTH"],["WATER"],["HARVEST"],["EAST"],["WEST"]],"market":[["SELL","FERTILIZER",1]]},{"farmer":["WEST"],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["HARVEST"],["EAST"],["WATER"],["WATER"],["HARVEST"],["SOUTH"],["EAST"],["WATER"]],"market":[]},{"farmer":["WEST"],"hands":[["COLLECT_FERTILIZER"],["EAST"],["WEST"],["EAST"],["HARVEST"],["HARVEST"],["SOUTH"],["SOUTH"],["COLLECT_FERTILIZER"],["HARVEST"]],"market":[["SELL","STRAWBERRY",2],["SELL","MILK",1],["SELL","WOOL",1]]},{"farmer":["HARVEST"],"hands":[["NORTH"],["COLLECT_FERTILIZER"],["WEST"],["HARVEST"],["NORTH"],["EAST"],["WATER"],["WATER"],["HARVEST"],["WEST"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["WEST"],"hands":[["WATER"],["HARVEST"],["WATER"],["NORTH"],["WATER"],["WATER"],["HARVEST"],["HARVEST"],["SOUTH"],["HARVEST"]],"market":[]},{"farmer":["SOUTH"],"hands":[["HARVEST"],["WEST"],["HARVEST"],["WATER"],["HARVEST"],["HARVEST"],["SOUTH"],["SOUTH"],["SOUTH"],["COLLECT_FERTILIZER"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["WATER"],"hands":[["NORTH"],["SOUTH"],["EAST"],["HARVEST"],["NORTH"],["EAST"],["WATER"],["EAST"],["WATER"],["WEST"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["HARVEST"],"hands":[["EAST"],["DROP"],["EAST"],["SOUTH"],["SOUTH"],["WATER"],["HARVEST"],["EAST"],["HARVEST"],["HARVEST"]],"market":[["SELL","STRAWBERRY",2]]},{"farmer":["SOUTH"],"hands":[["WATER"],["NORTH"],["EAST"],["COLLECT_FERTILIZER"],["SOUTH"],["HARVEST"],["EAST"],["HARVEST"],["NORTH"],["COLLECT_FERTILIZER"]],"market":[["SELL","STRAWBERRY",7],["SELL","WHEAT",6],["SELL","FERTILIZER",2]]},{"farmer":["SOUTH"],"hands":[["HARVEST"],["NORTH"],["DROP"],["WEST"],["SOUTH"],["SOUTH"],["HARVEST"],["NORTH"],["WEST"],["SOUTH"]],"market":[["SELL","WHEAT",1]]},{"farmer":["WATER"],"hands":[["SOUTH"],["COLLECT_FERTILIZER"],["HARVEST"],["WEST"],["SOUTH"],["SOUTH"],["NORTH"],["NORTH"],["WEST"],["EAST"]],"market":[["SELL","WHEAT",1]]},{"farmer":["HARVEST"],"hands":[["SOUTH"],["SOUTH"],["DROP"],["WEST"],["EAST"],["SOUTH"],["NORTH"],["NORTH"],["DROP"],["EAST"]],"market":[["SELL","MILK",9],["SELL","WHEAT",1]]},{"farmer":["EAST"],"hands":[["SOUTH"],["SOUTH"],["NORTH"],["DROP"],["DROP"],["WEST"],["EAST"],["NORTH"],["SOUTH"],["EAST"]],"market":[["SELL","WHEAT",4],["SELL","FERTILIZER",3]]},{"farmer":["EAST"],"hands":[["SOUTH"],["DROP"],["SOUTH"],["HARVEST"],["SOUTH"],["WEST"],["DROP"],["WEST"],["SOUTH"],["DROP"]],"market":[["SELL","WHEAT",13],["SELL","TOMATO",6],["SELL","FERTILIZER",5]]},{"farmer":["EAST"],"hands":[["DROP"],["SOUTH"],["SOUTH"],["DROP"],["SOUTH"],["DROP"],["SOUTH"],["WEST"],["WEST"],["SOUTH"]],"market":[["SELL","WHEAT",13],["SELL","FERTILIZER",1]]},{"farmer":["EAST"],"hands":[["SOUTH"],["SOUTH"],["SOUTH"],["SOUTH"],["SOUTH"],["SOUTH"],["SOUTH"],["DROP"],["WEST"],["SOUTH"]],"market":[["SELL","WHEAT",13],["SELL","STRAWBERRY",2]]},{"farmer":["DROP"],"hands":[["SOUTH"],["WEST"],["WEST"],["SOUTH"],["WEST"],["SOUTH"],["WEST"],["SOUTH"],["WEST"],["SOUTH"]],"market":[["SELL","WHEAT",13]]},{"farmer":["SOUTH"],"hands":[["WEST"],["SOUTH"],["WEST"],["WEST"],["WEST"],["WEST"],["WEST"],["WEST"],["WEST"],["WEST"]],"market":[["SELL","WHEAT",19],["SELL","WOOL",3]]},{"farmer":["SOUTH"],"hands":[["SOUTH"],["WEST"],["WEST"],["SOUTH"],["WEST"],["SOUTH"],["WEST"],["SOUTH"],["WEST"],["WEST"]],"market":[["SELL","MILK",7],["SELL","WHEAT",1],["SELL","CARROT",12]]},{"farmer":["SOUTH"],"hands":[["WEST"],["WEST"],["WEST"],["WEST"],["WEST"],["WEST"],["WEST"],["WEST"],["HARVEST"],["WEST"]],"market":[["SELL","EGG",10],["SELL","WHEAT",1],["SELL","TOMATO",2]]}]')
_PROXY=make_agent({0:_DEMO})
def archived_proxy_agent(observation,configuration=None):
    return _PROXY(observation,configuration)
archived_proxy_agent.telemetry=_PROXY.chassis.diagnostics
agent=archived_proxy_agent
