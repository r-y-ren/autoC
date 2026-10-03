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


# Archived development demonstration; responsive guards, fixed production.
_DEMO=[{'farmer': ['PASS'], 'hands': [], 'market': [['BUY_ANIMAL', 'COW', 1], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['PICKUP', 'COW', 1], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['BUILD_PASTURE'], 'hands': [['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'COW', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'COW', 1]], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'COW', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['BUILD_PASTURE'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['BUILD_PASTURE'], ['PLACE', 'SHEEP', 1], ['NORTH'], ['PLACE', 'SHEEP', 1], ['NORTH']], 'market': [['BUY_SEED', 'MELON', 2], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLACE', 'SHEEP', 1], ['CARE'], ['WEST'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WEST'], ['BUILD_PASTURE'], ['BUILD_PASTURE'], ['PLANT', 'MELON']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WEST'], ['NORTH'], ['PLACE', 'COW', 1], ['PLACE', 'SHEEP', 1], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'MELON'], ['PLANT', 'MELON'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['PLANT', 'MELON'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'MELON'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['PLANT', 'MELON'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['PASS'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['PASS'], 'hands': [['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['SOUTH'], ['PASS'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PLANT', 'WHEAT'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['SOUTH'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['DROP'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['SOUTH'], ['CARE'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 1], ['PICKUP', 'WHEAT', 2], ['CARE']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 1], ['NORTH'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['NORTH'], ['DROP']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['CARE'], ['PICKUP', 'WHEAT', 1]], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PASS'], ['PASS'], ['FEED']], 'market': []}, {'farmer': ['PLANT', 'MELON'], 'hands': [['WEST'], ['PASS'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['PASS'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['PASS'], ['NORTH']], 'market': []}, {'farmer': ['PLANT', 'MELON'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['DROP'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['DROP'], ['DROP'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WATER'], 'hands': [['PICKUP', 'COW', 1], ['CARE'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['PASS'], ['SOUTH'], ['WATER'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['BUILD_PASTURE'], ['PASS'], ['SOUTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLACE', 'COW', 1], ['PASS'], ['CARE'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['PASS'], ['FEED'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['SOUTH'], ['PASS'], ['EAST'], ['HARVEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['NORTH'], ['FEED'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FEED'], ['NORTH'], ['PASS'], ['PASS'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PLANT', 'WHEAT'], ['PASS'], ['PLANT', 'WHEAT'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 7], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['WEST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['DROP'], ['DROP'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['NORTH'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'COW', 1], ['CARE'], ['SOUTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['EAST'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['SOUTH'], ['HARVEST'], ['CARE']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['DROP'], ['SOUTH'], ['SOUTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WATER'], ['PASS'], ['FEED'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['BUILD_PASTURE'], ['WEST'], ['PASS'], ['CARE'], ['SOUTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['PLACE', 'COW', 1], ['WATER'], ['PASS'], ['SOUTH'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['NORTH'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLANT', 'STRAWBERRY'], ['WATER'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['HARVEST'], ['PASS'], ['CARE'], ['PASS']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WEST'], ['PLANT', 'STRAWBERRY'], ['PASS'], ['FEED'], ['PASS']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['PASS'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['FEED'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WEST'], ['PASS'], ['PASS'], ['CARE'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 9], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WEST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['DROP'], ['WEST'], ['WEST'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'COW', 1], ['CARE'], ['SOUTH'], ['WEST'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['EAST'], ['HARVEST'], ['DROP'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['PICKUP', 'WHEAT', 2], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['CARE'], ['DROP'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['BUILD_PASTURE'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['FEED'], ['FEED'], ['HARVEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['PLACE', 'COW', 1], ['PASS'], ['FEED'], ['CARE'], ['NORTH'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['PASS'], ['NORTH'], ['EAST'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['HARVEST'], ['PASS'], ['NORTH'], ['FEED'], ['NORTH'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLANT', 'STRAWBERRY'], ['PASS'], ['FEED'], ['CARE'], ['FEED'], ['PASS']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['CARE'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['EAST'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['FEED'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['NORTH']], 'market': []}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['SOUTH'], ['EAST'], ['FEED'], ['CARE'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['SOUTH'], ['EAST'], ['CARE'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['SOUTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['PASS'], ['FEED'], ['FEED'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['CARE'], 'hands': [['PASS'], ['PASS'], ['CARE'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['PASS'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PASS'], ['WEST'], ['NORTH'], ['WEST'], ['DROP']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PASS'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['WEST'], ['CARE'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PASS'], ['WATER'], ['EAST'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PASS'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PASS'], ['WATER'], ['FEED'], ['DROP'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['NORTH'], ['CARE'], ['PASS'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['PASS'], ['WATER'], ['WEST'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['NORTH'], ['WATER'], ['PASS'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PASS'], ['WEST'], ['PASS'], ['PASS'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WOOL', 6], ['BUY_LAND']]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['NORTH'], ['FEED'], ['EAST'], ['EAST'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 6], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'STRAWBERRY', 8]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'GOOSE', 1], ['NORTH'], ['CARE'], ['EAST'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLANT', 'STRAWBERRY'], ['DROP'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 6], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['BUILD_COOP'], ['SOUTH'], ['WEST'], ['WATER'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': [['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['PICKUP', 'GOOSE', 1], 'hands': [['PLACE', 'GOOSE', 1], ['SOUTH'], ['FEED'], ['NORTH'], ['FEED'], ['EAST'], ['EAST'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'MELON', 2]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['DROP'], ['CARE'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['EAST'], ['EAST']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'MELON'], ['PICKUP', 'GOOSE', 1], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['BUILD_COOP'], 'hands': [['WATER'], ['EAST'], ['EAST'], ['EAST'], ['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER']], 'market': [['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['PLACE', 'GOOSE', 1], 'hands': [['EAST'], ['NORTH'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['PLANT', 'STRAWBERRY'], ['SOUTH'], ['SOUTH'], ['EAST']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'STRAWBERRY', 2]]}, {'farmer': ['EAST'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['DROP'], ['WATER'], ['NORTH'], ['WATER'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 2]]}, {'farmer': ['PLANT', 'MELON'], 'hands': [['WATER'], ['BUILD_COOP'], ['PICKUP', 'GOOSE', 1], ['EAST'], ['FEED'], ['EAST'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['PLACE', 'GOOSE', 1], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['PLANT', 'STRAWBERRY'], ['SOUTH'], ['SOUTH'], ['PICKUP', 'GOOSE', 1]], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['PLANT', 'STRAWBERRY'], ['NORTH'], ['EAST'], ['WATER'], ['NORTH'], ['WATER'], ['DROP'], ['PLANT', 'STRAWBERRY'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WATER'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['NORTH'], ['WEST'], ['EAST'], ['PASS'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['CARE'], ['PLANT', 'STRAWBERRY'], ['PASS'], ['NORTH'], ['EAST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PASS'], 'hands': [['PLANT', 'STRAWBERRY'], ['WEST'], ['BUILD_COOP'], ['WATER'], ['WEST'], ['WATER'], ['PASS'], ['PASS'], ['NORTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['WEST'], ['PLACE', 'GOOSE', 1], ['PASS'], ['WATER'], ['PASS'], ['PASS'], ['PASS'], ['BUILD_COOP']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WEST'], ['PASS'], ['PASS'], ['PASS'], ['PLACE', 'GOOSE', 1]], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['SOUTH'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 10]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['CARE'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['PLACE', 'FERTILIZER', 1], ['EAST'], ['FEED'], ['SOUTH'], ['NORTH'], ['WATER'], ['SOUTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['PICKUP', 'WHEAT', 2], ['EAST'], ['CARE'], ['SOUTH'], ['FEED'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['DROP'], ['CARE'], ['WATER'], ['DROP']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['NORTH'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['NORTH'], ['FEED'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['FEED'], ['WATER'], ['FEED'], ['CARE'], ['NORTH'], ['PASS']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['WEST'], ['CARE'], ['NORTH'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['WEST'], ['FEED'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['NORTH'], ['CARE'], ['NORTH'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['NORTH'], ['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['FEED'], ['SOUTH'], ['CARE'], ['WEST'], ['EAST'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['SOUTH'], ['PASS'], ['WATER'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['DROP'], ['PASS'], ['WEST'], ['SOUTH'], ['PASS']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['WATER'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['EAST'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['EAST'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['EAST']], 'market': [['SELL', 'MILK', 6], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['NORTH'], ['EAST'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['PLACE', 'FERTILIZER', 1], ['WEST'], ['FEED'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['PICKUP', 'WHEAT', 3], ['FEED'], ['NORTH'], ['SOUTH'], ['WATER'], ['EAST'], ['NORTH'], ['WATER'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_LAND']]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['FEED'], ['SOUTH'], ['EAST'], ['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WEST']], 'market': [['BUY_LAND']]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WEST'], ['NORTH'], ['DROP'], ['WATER'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER']], 'market': [['SELL', 'MILK', 6], ['BUY_LAND']]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['FEED'], ['FEED'], ['CARE'], ['NORTH'], ['WEST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['CARE'], ['CARE'], ['PICKUP', 'GOOSE', 1], ['WATER'], ['SOUTH'], ['DROP'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['EAST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['EAST'], ['WATER'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['EAST'], ['NORTH'], ['BUILD_COOP'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['DROP'], ['WATER'], ['PLACE', 'GOOSE', 1], ['WATER'], ['SOUTH'], ['SOUTH'], ['DROP'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['PICKUP', 'WHEAT', 2], ['EAST'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['FEED'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['PASS'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['NORTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['WATER'], ['PASS'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['PASS'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['WEST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['PASS'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['NORTH'], ['SOUTH'], ['WATER'], ['PASS'], ['WEST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['PASS'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['FEED'], ['WEST'], ['SOUTH'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['PASS'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 4]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['CARE'], ['SOUTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH'], ['WATER'], ['PASS'], ['SOUTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['NORTH'], ['DROP'], ['WATER'], ['CARE'], ['PLANT', 'WHEAT'], ['WEST'], ['PASS'], ['PASS'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PASS'], ['PASS'], ['CARE'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['WEST'], ['PASS'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 13]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['PICKUP', 'WHEAT', 4], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 4], ['FEED'], ['NORTH'], ['HARVEST'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'WOOL', 4], ['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['DROP'], ['FEED'], ['CARE'], ['NORTH'], ['EAST'], ['FEED'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['WEST']], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'COW', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['CARE'], ['EAST'], ['NORTH'], ['PICKUP', 'COW', 1], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 1], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['DROP'], ['FEED'], ['BUILD_PASTURE'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'COW', 1], ['FEED'], ['FEED'], ['CARE'], ['PICKUP', 'COW', 1], ['WEST'], ['PLACE', 'COW', 1], ['SOUTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['CARE'], ['CARE'], ['EAST'], ['PICKUP', 'GOOSE', 1], ['FEED'], ['PICKUP', 'GOOSE', 1], ['DROP'], ['WEST']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WEST'], ['EAST'], ['FEED'], ['SOUTH'], ['CARE'], ['SOUTH'], ['PICKUP', 'WHEAT', 2], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['BUILD_PASTURE'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['CARE'], ['WEST'], ['WEST'], ['SOUTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PLACE', 'COW', 1], ['FEED'], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['CARE'], ['NORTH'], ['NORTH'], ['BUILD_COOP'], ['NORTH'], ['WEST'], ['NORTH'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'STRAWBERRY'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['PLACE', 'GOOSE', 1], ['FEED'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['EAST'], ['WEST'], ['CARE'], ['SOUTH'], ['CARE'], ['WATER'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WEST'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLANT', 'STRAWBERRY'], ['PLACE', 'FERTILIZER', 1], ['FEED'], ['EAST'], ['PASS'], ['WEST'], ['SOUTH'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['EAST'], ['CARE'], ['WATER'], ['PASS'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['PASS'], ['NORTH'], ['WATER'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['WEST'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['WEST'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['NORTH'], ['WEST'], ['EAST'], ['WATER'], ['WEST'], ['PASS'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['PASS'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['WATER'], ['PASS'], ['EAST'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['SOUTH'], ['WATER'], ['PASS'], ['SOUTH'], ['WATER'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 7], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 15]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['DROP'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 3], ['CARE'], ['WEST'], ['NORTH'], ['EAST'], ['WEST'], ['NORTH'], ['WEST'], ['DROP'], ['WEST']], 'market': [['SELL', 'MILK', 3], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['WATER'], ['WEST'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 9]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['CARE'], ['SOUTH'], ['CARE'], ['HARVEST'], ['EAST'], ['WEST'], ['CARE'], ['HARVEST'], ['DROP'], ['WATER']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['PICKUP', 'WHEAT', 4], ['HARVEST']], 'market': [['SELL', 'MELON', 6], ['SELL', 'WHEAT', 3], ['BUY_PRODUCT', 'WHEAT', 15]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['EAST'], ['NORTH'], ['CARE'], ['WEST'], ['SOUTH'], ['EAST'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1], ['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 13]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['WATER'], ['EAST'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['FEED'], ['SOUTH'], ['CARE'], ['DROP'], ['NORTH'], ['EAST'], ['WEST'], ['DROP'], ['FEED'], ['EAST']], 'market': [['SELL', 'MELON', 18]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 4], ['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['EAST'], ['HARVEST'], ['WEST'], ['CARE'], ['DROP']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WEST'], ['NORTH'], ['EAST'], ['FEED'], ['WEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['HARVEST'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['DROP'], ['CARE'], ['WEST'], ['FEED'], ['SOUTH']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['EAST'], ['WATER'], ['SOUTH'], ['CARE'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['EAST'], ['CARE'], ['WEST'], ['WEST'], ['WEST'], ['SOUTH'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['FEED'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['FEED'], ['NORTH'], ['CARE'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WEST'], ['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['WEST'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['SOUTH'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['DROP'], ['FERTILIZE'], ['EAST'], ['SOUTH'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['PASS'], ['WATER'], ['WATER'], ['SOUTH'], ['EAST'], ['WATER'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PASS'], ['WATER'], ['WATER'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['PICKUP', 'WHEAT', 4], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'MILK', 6], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['FEED'], ['WEST'], ['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['PICKUP', 'WHEAT', 4]], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['WEST'], ['FEED'], ['WATER'], ['SOUTH'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['CARE'], ['WEST'], ['WATER'], ['HARVEST'], ['CARE']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['FEED'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['CARE'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['EAST'], ['WEST'], ['SOUTH'], ['EAST'], ['NORTH'], ['WEST'], ['WATER'], ['SOUTH'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DROP'], 'hands': [['FEED'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['FERTILIZE'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['CARE'], ['WATER'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['WATER'], ['WATER'], ['DROP'], ['WEST']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['WEST'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['DROP'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['FEED']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['SOUTH'], ['EAST'], ['PICKUP', 'WHEAT', 2], ['FEED'], ['HARVEST'], ['WEST'], ['EAST'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['CARE'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['EAST'], ['HARVEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['EAST'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['HARVEST'], ['EAST'], ['FEED'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['CARE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['WEST'], ['WATER'], ['HARVEST'], ['WEST'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['SOUTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 3]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['PASS'], ['WATER'], ['WATER'], ['WATER'], ['PASS'], ['PASS'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 11], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['EAST'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 3]]}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['DROP'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4]], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['DROP'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 4], ['CARE'], ['WEST'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['WATER'], ['WEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['SOUTH'], ['CARE'], ['SOUTH'], ['EAST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['DROP'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['CARE']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['CARE'], ['FEED'], ['PICKUP', 'WHEAT', 3], ['EAST'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['FEED']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['CARE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['CARE'], ['WEST'], ['WATER'], ['FEED'], ['WATER'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['CARE'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['PLANT', 'STRAWBERRY'], ['SOUTH'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['FEED']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['NORTH'], ['SOUTH'], ['EAST'], ['NORTH'], ['WATER'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['WEST'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['EAST'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['WATER'], ['FEED'], ['NORTH'], ['EAST'], ['NORTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['DROP'], ['NORTH'], ['EAST'], ['CARE'], ['WATER'], ['DROP'], ['HARVEST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['NORTH'], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['SOUTH'], ['EAST'], ['PASS'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['EAST'], ['WATER'], ['FEED'], ['EAST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['EAST'], ['NORTH'], ['CARE'], ['WATER'], ['EAST'], ['SOUTH'], ['EAST'], ['PASS'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['PASS'], ['NORTH'], ['WATER'], ['WATER'], ['DROP'], ['PASS'], ['WATER']], 'market': [['SELL', 'EGG', 9], ['SELL', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'MILK', 3], ['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['WEST']], 'market': [['SELL', 'MILK', 2], ['SELL', 'FERTILIZER', 2], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['CARE'], ['NORTH'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['FEED'], ['EAST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['FEED'], ['FEED'], ['FEED'], ['NORTH'], ['SOUTH'], ['WEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['CARE'], ['NORTH'], ['CARE'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['FEED'], ['FEED'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['WATER'], ['CARE'], ['CARE'], ['NORTH'], ['WEST'], ['WATER'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['HARVEST'], ['WEST'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['PLANT', 'STRAWBERRY'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['FEED'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['WEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['CARE'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['FEED'], ['NORTH'], ['EAST'], ['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['WEST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['FEED'], ['WEST'], ['CARE'], ['FEED'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['FERTILIZE'], ['WEST'], ['CARE'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['FERTILIZE']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['EAST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['SOUTH'], ['WEST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['FERTILIZE'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['FERTILIZE'], ['WEST'], ['WEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['EAST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 4], ['SELL', 'EGG', 1]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['EAST'], ['SOUTH'], ['PASS'], ['SOUTH'], ['EAST'], ['NORTH'], ['PASS'], ['SOUTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 7], ['SELL', 'MILK', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['DROP'], ['CARE'], ['WEST'], ['PICKUP', 'WHEAT', 4], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['FEED'], ['WEST'], ['WEST'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['WATER'], ['SOUTH'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['CARE'], ['CARE'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['NORTH']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['FEED'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WEST'], ['FEED'], ['FEED'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['SOUTH'], ['CARE'], ['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WEST'], ['SOUTH'], ['NORTH'], ['WEST'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['CARE'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['EAST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'MILK', 1]]}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['FEED'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['EAST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['NORTH'], ['EAST'], ['NORTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['DROP'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'MILK', 3]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WATER'], ['EAST'], ['NORTH'], ['WATER'], ['EAST'], ['NORTH'], ['PASS'], ['WEST']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WATER'], 'hands': [['DROP'], ['PASS'], ['PASS'], ['HARVEST'], ['SOUTH'], ['WATER'], ['PASS'], ['PASS'], ['NORTH']], 'market': [['SELL', 'EGG', 5], ['SELL', 'WHEAT', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'MILK', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'FERTILIZER', 4], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'FERTILIZER', 4], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4]], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'MILK', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WEST'], ['EAST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'FERTILIZER', 3]], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['SOUTH'], ['EAST'], ['WEST'], ['WATER'], ['SOUTH'], ['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['FEED'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['WEST'], ['EAST'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DIG'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['BUILD_PASTURE'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['CARE'], ['WEST'], ['FERTILIZE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['PLACE', 'SHEEP', 1], ['WATER'], ['BUILD_PASTURE'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['FEED'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['CARE'], ['EAST'], ['PLACE', 'SHEEP', 1], ['FERTILIZE'], ['WEST'], ['EAST'], ['FERTILIZE'], ['WEST'], ['CARE'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['WEST'], ['FERTILIZE'], ['FEED'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FERTILIZE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WATER'], ['WATER'], ['CARE'], ['NORTH'], ['WEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WEST'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['FERTILIZE'], ['NORTH'], ['FEED'], ['FEED'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['CARE'], ['CARE'], ['NORTH'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WEST'], ['FEED'], ['CARE'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['EAST'], ['HARVEST'], ['EAST'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WATER'], ['WEST'], ['NORTH'], ['NORTH'], ['EAST'], ['EAST'], ['WEST'], ['WATER'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['EAST'], ['CARE'], ['WATER'], ['WATER'], ['EAST'], ['FERTILIZE'], ['NORTH'], ['SOUTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['PASS'], ['NORTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['SOUTH'], 'hands': [['FERTILIZE'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'EGG', 2]]}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['WATER'], ['PASS'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['PASS'], ['PASS']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'MILK', 4], ['SELL', 'FERTILIZER', 2], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['FEED'], ['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['CARE'], ['WEST'], ['FEED'], ['WATER'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['EAST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WEST'], ['WEST'], ['HARVEST'], ['EAST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FEED'], ['CARE'], ['WEST'], ['FEED'], ['DROP'], ['WEST'], ['DROP'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'MELON', 12]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WEST'], ['FEED'], ['CARE'], ['EAST'], ['WEST'], ['NORTH'], ['FEED'], ['NORTH'], ['EAST'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['CARE'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['CARE'], ['HARVEST'], ['WEST'], ['EAST'], ['SOUTH'], ['NORTH'], ['WEST'], ['HARVEST'], ['SOUTH'], ['FERTILIZE']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['PLANT', 'WHEAT'], ['WATER'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WEST'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WEST'], ['WATER'], ['CARE'], ['WATER'], ['WEST'], ['EAST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WEST'], ['FERTILIZE']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FEED'], ['FERTILIZE'], ['WATER'], ['WEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['DROP'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 7], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WATER'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['NORTH'], ['FERTILIZE'], ['FERTILIZE'], ['EAST'], ['WATER'], ['EAST'], ['HARVEST'], ['DROP'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 10]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['EAST'], ['HARVEST'], ['EAST'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['EAST'], ['HARVEST'], ['NORTH'], ['EAST'], ['NORTH'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['EAST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['WATER'], ['EAST'], ['SOUTH'], ['NORTH'], ['FEED'], ['HARVEST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['HARVEST'], ['EAST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['CARE'], ['PASS']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['EAST'], ['DROP'], ['HARVEST'], ['PASS'], ['PASS']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 12], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 6], ['SELL', 'MILK', 2], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['PLACE', 'MILK', 3], ['WEST'], ['FEED'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['FEED'], ['NORTH'], ['CARE'], ['SOUTH'], ['WEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['NORTH'], ['CARE'], ['FEED'], ['NORTH'], ['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['NORTH'], ['HARVEST'], ['CARE'], ['FEED'], ['WEST'], ['FERTILIZE'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['FEED'], ['SOUTH'], ['WEST'], ['EAST'], ['WEST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['CARE'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'WOOL', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['HARVEST'], ['WEST'], ['NORTH'], ['FEED'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['WEST'], ['NORTH'], ['EAST'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['EAST'], ['HARVEST'], ['WATER'], ['FEED'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['EAST'], ['WEST'], ['CARE'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['CARE'], ['EAST'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'WOOL', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['WEST'], ['HARVEST'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['FEED'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['CARE'], ['NORTH'], ['WEST'], ['WATER'], ['HARVEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'WOOL', 2]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['EAST'], ['WEST'], ['FERTILIZE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['HARVEST'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'EGG', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['SOUTH'], ['WATER'], ['PASS'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['SOUTH'], ['PASS'], ['PASS'], ['SOUTH'], ['FERTILIZE'], ['FERTILIZE'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['FERTILIZE'], ['EAST'], ['PASS'], ['WEST'], ['EAST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['EAST'], ['PASS']], 'market': [['SELL', 'EGG', 16]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['SOUTH'], ['PASS'], ['PASS'], ['FERTILIZE'], ['WATER'], ['EAST'], ['DROP'], ['WEST'], ['PASS'], ['PASS']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['WEST'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['CARE'], ['WEST'], ['FEED'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['EAST'], ['HARVEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['WEST'], ['CARE'], ['WEST'], ['FEED'], ['HARVEST'], ['NORTH'], ['WEST'], ['WEST'], ['EAST'], ['EAST'], ['FERTILIZE'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WATER'], ['FEED'], ['SOUTH'], ['EAST'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'MILK', 1]]}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['NORTH'], ['SOUTH'], ['CARE'], ['SOUTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['DROP'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['DROP'], ['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['DROP'], ['NORTH'], ['WEST'], ['WATER'], ['WEST'], ['WEST'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['CARE'], ['WEST'], ['HARVEST'], ['EAST'], ['NORTH'], ['SOUTH'], ['WEST'], ['DROP'], ['WEST'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['EAST'], 'hands': [['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['EAST'], ['EAST'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['DROP'], ['WEST'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['WEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['DROP'], ['DIG'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['SOUTH'], ['NORTH'], ['EAST'], ['EAST'], ['FEED'], ['WATER'], ['DIG'], ['FEED'], ['PICKUP', 'WHEAT', 2], ['PLANT', 'WHEAT'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['EAST'], ['NORTH'], ['CARE'], ['WEST'], ['PLANT', 'WHEAT'], ['CARE'], ['NORTH'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST'], ['DROP']], 'market': [['SELL', 'STRAWBERRY', 8]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WEST'], ['EAST'], ['FEED'], ['NORTH'], ['EAST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['CARE'], ['EAST'], ['EAST'], ['EAST'], ['EAST'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'EGG', 12]]}, {'farmer': ['PASS'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['EAST'], ['PASS'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['PASS'], ['FEED'], ['FEED'], ['SOUTH'], ['DROP']], 'market': [['SELL', 'EGG', 3], ['SELL', 'WHEAT', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 7], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'FERTILIZER', 4], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['PICKUP', 'FERTILIZER', 4]], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 1], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WEST'], ['SOUTH'], ['CARE'], ['WATER'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['WATER'], ['HARVEST'], ['EAST'], ['WATER'], ['HARVEST'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'WOOL', 1], ['SELL', 'MILK', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['SOUTH'], ['CARE'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['FEED'], ['SOUTH'], ['WEST'], ['WATER'], ['NORTH'], ['EAST'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['DROP'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['WATER'], ['FEED'], ['EAST'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'WOOL', 2]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['FERTILIZE'], ['EAST'], ['WATER'], ['FEED'], ['EAST'], ['WEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['NORTH'], ['CARE'], ['FERTILIZE'], ['FEED'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['WATER'], ['NORTH'], ['DROP'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['CARE'], ['HARVEST'], ['DIG']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['CARE'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['FEED'], ['WATER'], ['DROP'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['EAST'], 'hands': [['FERTILIZE'], ['WEST'], ['WATER'], ['CARE'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['DIG'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['DIG']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['DROP'], ['WATER'], ['EAST'], ['WATER'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['SOUTH'], ['WEST'], ['DIG'], ['WATER'], ['WEST'], ['NORTH'], ['HARVEST'], ['EAST'], ['WEST'], ['WEST'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['WATER'], ['SOUTH'], ['EAST'], ['WATER'], ['FERTILIZE'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['HARVEST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WEST'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['FERTILIZE']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'MILK', 3]]}, {'farmer': ['SOUTH'], 'hands': [['FERTILIZE'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'EGG', 4], ['SELL', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['FEED'], ['WEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['FEED'], ['EAST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['HARVEST'], ['WEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'WOOL', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['CARE'], ['WEST'], ['FEED'], ['WEST'], ['NORTH'], ['HARVEST'], ['WEST'], ['SOUTH'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['SOUTH'], ['WEST'], ['CARE'], ['HARVEST'], ['WEST'], ['NORTH'], ['WEST'], ['DIG'], ['SOUTH'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['NORTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['DROP'], ['DROP'], ['WEST'], ['WATER'], ['DROP'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 12]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WATER'], ['FEED'], ['FEED'], ['EAST'], ['PICKUP', 'WHEAT', 2], ['DROP'], ['NORTH'], ['EAST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['CARE'], 'hands': [['DROP'], ['SOUTH'], ['CARE'], ['CARE'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['EAST'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'WOOL', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['DIG'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 2], ['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['DROP'], ['WEST'], ['WEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['PICKUP', 'WHEAT', 3], ['SOUTH'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['WATER'], ['WEST'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['EAST'], ['FERTILIZE'], ['EAST'], ['NORTH'], ['FEED'], ['WATER'], ['WATER'], ['EAST'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['EAST'], ['WATER'], ['EAST'], ['FEED'], ['CARE'], ['NORTH'], ['WEST'], ['EAST'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['NORTH'], ['EAST'], ['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['DIG'], ['HARVEST'], ['DROP'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 10], ['SELL', 'WOOL', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WATER'], ['SOUTH'], ['NORTH'], ['FEED'], ['FERTILIZE'], ['HARVEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'EGG', 8]]}, {'farmer': ['PASS'], 'hands': [['CARE'], ['SOUTH'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['PASS'], ['EAST'], ['WATER'], ['NORTH'], ['PASS'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1]], 'market': [['SELL', 'MILK', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['WEST'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'FERTILIZER', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['PICKUP', 'FERTILIZER', 4]], 'market': [['SELL', 'FERTILIZER', 6]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['FEED'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['CARE'], ['SOUTH'], ['FEED'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['FERTILIZE'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['BUILD_PASTURE'], ['NORTH'], ['HARVEST'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['HARVEST'], ['WEST'], ['PLACE', 'SHEEP', 1], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['BUILD_PASTURE'], ['WATER'], ['FEED'], ['FEED'], ['HARVEST'], ['FEED'], ['WATER'], ['FEED'], ['WATER'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['PLACE', 'SHEEP', 1], ['FERTILIZE'], ['CARE'], ['CARE'], ['WEST'], ['CARE'], ['WEST'], ['CARE'], ['NORTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FEED'], ['NORTH'], ['NORTH'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH'], ['FERTILIZE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WATER'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['FEED'], ['WATER'], ['FEED'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['CARE'], ['HARVEST'], ['CARE'], ['EAST'], ['HARVEST'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['BUILD_PASTURE'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'WHEAT'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WEST'], ['PLACE', 'SHEEP', 1], ['HARVEST'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['NORTH'], ['FEED'], ['NORTH'], ['FEED'], ['NORTH'], ['HARVEST'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FERTILIZE'], ['CARE'], ['WATER'], ['CARE'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['WEST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['WATER'], ['NORTH'], ['EAST'], ['HARVEST'], ['WATER'], ['FEED'], ['FERTILIZE'], ['WEST'], ['SOUTH'], ['FERTILIZE']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['SOUTH'], ['WEST'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['EAST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'WOOL', 3]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['EAST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['SOUTH'], ['PASS'], ['WATER'], ['PASS'], ['HARVEST'], ['NORTH'], ['DROP'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'MILK', 4], ['SELL', 'FERTILIZER', 4], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['CARE'], ['WEST'], ['FEED'], ['EAST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['EAST'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['CARE'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['DIG'], ['HARVEST'], ['EAST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WEST'], ['CARE'], ['WEST'], ['FEED'], ['PLANT', 'WHEAT'], ['WEST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['EAST'], ['NORTH'], ['FERTILIZE'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['HARVEST'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WEST'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['EAST'], ['NORTH'], ['SOUTH'], ['CARE'], ['WEST'], ['EAST']], 'market': [['SELL', 'WOOL', 2]]}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['NORTH'], ['DIG'], ['FEED'], ['SOUTH'], ['NORTH'], ['FERTILIZE'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['DIG'], ['NORTH'], ['PLANT', 'WHEAT'], ['CARE'], ['SOUTH'], ['FEED'], ['WATER'], ['DIG']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['WEST'], ['FEED'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['CARE'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'STRAWBERRY', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'WHEAT', 2], ['FERTILIZE'], ['CARE'], ['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['DROP'], ['DIG'], ['WATER'], ['DROP'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 12]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['SOUTH'], ['WEST'], ['WATER'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['PLANT', 'WHEAT'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['HARVEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['WEST'], ['SOUTH'], ['DIG'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['DIG'], ['PLANT', 'WHEAT'], ['DIG']], 'market': [['BUY_SEED', 'WHEAT', 2], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WEST'], ['FERTILIZE'], ['FEED'], ['PLANT', 'WHEAT'], ['SOUTH'], ['NORTH'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['SOUTH'], ['WATER'], ['CARE'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['NORTH'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['DIG'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['FEED'], ['NORTH']], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FEED'], ['WEST'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['DIG'], ['EAST'], ['CARE'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WATER'], ['WATER'], ['HARVEST'], ['DIG'], ['HARVEST'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['DIG'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'MILK', 1]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 8]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['DIG']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'FERTILIZER', 12], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['PLACE', 'MILK', 3], ['WEST'], ['FEED'], ['WATER'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['FEED'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['FEED'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['FEED'], ['SOUTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WEST'], ['HARVEST'], ['EAST'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['SOUTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['SOUTH'], ['FEED'], ['FEED'], ['PLANT', 'WHEAT'], ['WEST'], ['SOUTH'], ['WATER'], ['DIG'], ['FERTILIZE'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['SOUTH'], ['CARE'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['CARE']], 'market': [['SELL', 'WHEAT', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WEST'], ['FEED'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['WEST'], ['DIG'], ['WEST'], ['WATER'], ['CARE'], ['EAST'], ['NORTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['NORTH'], ['FEED']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['FEED'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['NORTH'], ['CARE']], 'market': [['SELL', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['CARE'], ['WEST'], ['PLANT', 'CARROT'], ['WATER'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['FERTILIZE'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['NORTH'], ['SOUTH'], ['DIG'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'EGG', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DROP'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['FEED'], ['PLANT', 'WHEAT'], ['NORTH'], ['EAST']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['WATER'], ['EAST'], ['HARVEST'], ['NORTH'], ['DROP'], ['WATER'], ['NORTH'], ['CARE'], ['WATER'], ['WATER'], ['EAST']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['DIG']], 'market': [['SELL', 'WHEAT', 8], ['SELL', 'EGG', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['FERTILIZE'], ['DROP'], ['PLANT', 'CARROT'], ['CARE'], ['EAST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['HARVEST'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['DIG'], ['WATER'], ['SOUTH'], ['HARVEST'], ['EAST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'EGG', 7]]}, {'farmer': ['PASS'], 'hands': [['FERTILIZE'], ['PASS'], ['HARVEST'], ['FERTILIZE'], ['PASS'], ['EAST'], ['FERTILIZE'], ['FERTILIZE'], ['FERTILIZE'], ['EAST'], ['FERTILIZE']], 'market': [['SELL', 'WHEAT', 1], ['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'WHEAT', 16], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'FERTILIZER', 4], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2]], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['FEED'], ['EAST'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['EAST'], ['WATER'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['WEST'], ['CARE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['SOUTH'], ['FEED'], ['EAST'], ['DIG'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WEST'], ['FERTILIZE'], ['CARE'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['WATER'], ['WEST'], ['NORTH'], ['WEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['FEED'], ['SOUTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['HARVEST'], ['HARVEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['CARE'], ['WATER'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['DIG']], 'market': [['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['WATER'], ['DIG'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['HARVEST'], ['PLANT', 'WHEAT'], ['CARE'], ['NORTH'], ['PLANT', 'CARROT'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'EGG', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 2], ['BUY_SEED', 'CARROT', 3]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['FERTILIZE'], ['HARVEST'], ['WATER'], ['CARE'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['FEED'], ['EAST']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['EAST'], ['EAST'], ['DROP']], 'market': [['SELL', 'EGG', 3]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['NORTH'], ['EAST'], ['WEST'], ['FEED'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['WEST'], ['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['FERTILIZE'], ['CARE'], ['EAST'], ['DROP']], 'market': [['SELL', 'MILK', 6], ['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['SOUTH'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH'], ['EAST'], ['EAST'], ['WEST'], ['EAST'], ['WEST']], 'market': [['SELL', 'EGG', 5]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['FERTILIZE'], ['WATER'], ['EAST'], ['WATER'], ['HARVEST'], ['WATER'], ['EAST'], ['WEST'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'WHEAT', 16], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['DROP'], ['WEST'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['PICKUP', 'FERTILIZER', 4]], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['EAST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'WHEAT', 3], ['WEST'], ['FEED'], ['NORTH'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['EAST'], ['DIG'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WEST'], ['HARVEST'], ['CARE'], ['WATER'], ['PLANT', 'CARROT'], ['EAST'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['DIG']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['HARVEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WATER'], ['FEED'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['SOUTH'], ['CARE'], ['FEED'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WEST'], ['WATER'], ['WEST'], ['EAST'], ['WEST']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['FERTILIZE'], ['HARVEST'], ['CARE'], ['PLANT', 'WHEAT'], ['DIG'], ['NORTH'], ['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['CARE'], ['FEED'], ['WEST'], ['HARVEST'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FERTILIZE'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['NORTH'], ['EAST'], ['FEED'], ['SOUTH'], ['WATER'], ['WATER']], 'market': [['SELL', 'EGG', 1], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['FEED'], ['CARE'], ['FEED'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['SOUTH'], ['EAST'], ['WATER'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['PLANT', 'WHEAT'], ['SOUTH']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['FERTILIZE'], ['CARE'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WATER'], ['FERTILIZE']], 'market': [['SELL', 'MILK', 2], ['SELL', 'EGG', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['EAST'], ['DIG'], ['EAST'], ['SOUTH'], ['SOUTH'], ['FEED'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['HARVEST'], ['EAST'], ['WATER'], ['WATER'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['DROP'], ['WEST'], ['CARE'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 1], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['PLANT', 'CARROT'], ['NORTH'], ['EAST'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['PLANT', 'CARROT']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'MILK', 6], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['DROP'], ['FERTILIZE'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['EAST'], ['DROP'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['SELL', 'WHEAT', 8], ['SELL', 'EGG', 6]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['EAST'], ['PASS'], ['HARVEST'], ['PASS'], ['FERTILIZE'], ['WATER'], ['FERTILIZE']], 'market': [['SELL', 'EGG', 8], ['SELL', 'STRAWBERRY', 1], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'WHEAT', 18], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['EAST'], ['WEST'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['FEED'], ['HARVEST'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['FERTILIZE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['FEED'], ['FEED'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['FERTILIZE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['CARE'], ['HARVEST'], ['WEST'], ['SOUTH'], ['WATER'], ['EAST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['FERTILIZE'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['FEED'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['CARE'], ['HARVEST'], ['FEED'], ['FEED'], ['HARVEST'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['DIG'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['CARE'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['HARVEST'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 2], ['BUY_SEED', 'CARROT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['FEED'], ['WATER'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FERTILIZE'], ['CARE'], ['NORTH'], ['FEED'], ['NORTH'], ['WEST'], ['CARE'], ['EAST'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['NORTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['DROP']], 'market': [['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['FEED'], ['WATER'], ['HARVEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 11]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['HARVEST'], ['NORTH'], ['WATER'], ['SOUTH'], ['EAST'], ['WEST'], ['SOUTH'], ['PLANT', 'CARROT'], ['WATER'], ['DROP']], 'market': [['SELL', 'WHEAT', 6]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['EAST'], ['NORTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['EAST'], ['WEST']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['EAST'], ['EAST'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['FERTILIZE'], ['HARVEST'], ['EAST'], ['NORTH'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['EAST'], ['HARVEST'], ['EAST'], ['DROP'], ['SOUTH'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['WATER'], ['EAST'], ['DROP']], 'market': [['SELL', 'WHEAT', 9], ['SELL', 'CARROT', 6]]}, {'farmer': ['FERTILIZE'], 'hands': [['SOUTH'], ['FERTILIZE'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PASS'], ['SOUTH'], ['HARVEST'], ['PASS']], 'market': [['SELL', 'EGG', 2], ['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'WHEAT', 20], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'FERTILIZER', 4], ['WEST'], ['PICKUP', 'FERTILIZER', 4], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['WEST']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'WHEAT', 5], ['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 1], ['HIRE'], ['HIRE']]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['FEED'], ['PLACE', 'MILK', 4], ['WEST'], ['WEST'], ['EAST'], ['HARVEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['DROP'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['EAST'], ['EAST'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['EAST'], ['FERTILIZE'], ['FERTILIZE'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['WATER'], ['DROP'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['WEST'], ['EAST'], ['SOUTH'], ['HARVEST'], ['EAST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['SOUTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['HARVEST'], ['DROP'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 8], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FERTILIZE'], ['WATER'], ['WEST'], ['NORTH'], ['PLANT', 'CARROT'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['FERTILIZE'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['CARE'], ['WATER'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['FEED'], ['FERTILIZE'], ['SOUTH']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['EAST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['SOUTH'], ['CARE'], ['WATER'], ['FEED']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'WHEAT'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['EAST'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['NORTH'], ['HARVEST'], ['FEED'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['EAST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['EAST'], ['CARE'], ['WATER'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['EAST'], ['HARVEST'], ['DROP'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'CARROT', 7], ['BUY_SEED', 'CARROT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['FERTILIZE'], ['EAST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['EAST'], ['WEST'], ['EAST']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['EAST'], ['WATER'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['FEED']], 'market': [['SELL', 'WOOL', 2], ['SELL', 'MILK', 6], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WEST'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['PASS'], ['WEST'], ['EAST'], ['NORTH'], ['PASS'], ['CARE']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WEST'], ['FERTILIZE'], ['PASS'], ['WEST'], ['EAST'], ['PASS'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['PASS'], ['PASS']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'WHEAT', 23], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 2], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 3], ['SELL', 'WHEAT', 13], ['SELL', 'STRAWBERRY', 2], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['DROP'], ['WEST'], ['WEST'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 4]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['WATER'], ['FEED'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['EAST'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['EAST'], ['HARVEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['WEST'], ['EAST'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['HARVEST'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['WEST'], ['EAST'], ['HARVEST'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['FERTILIZE']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['FEED'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['EAST'], ['SOUTH'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'CARROT', 2], ['SELL', 'EGG', 2]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WEST'], ['EAST']], 'market': [['SELL', 'EGG', 2]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['EAST'], ['WATER'], ['DROP'], ['SOUTH'], ['WEST'], ['EAST']], 'market': [['SELL', 'EGG', 8], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['NORTH'], ['WATER'], ['HARVEST'], ['WEST'], ['EAST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['WEST'], ['EAST']], 'market': [['SELL', 'MILK', 6], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['EAST'], ['HARVEST'], ['EAST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WEST'], ['DROP'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['EAST'], ['DROP'], ['DROP'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['DROP'], ['DROP']], 'market': [['SELL', 'CARROT', 10], ['SELL', 'WHEAT', 2], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['EAST'], ['NORTH'], ['FERTILIZE'], ['NORTH'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 21], ['SELL', 'EGG', 3]]}, {'farmer': ['FERTILIZE'], 'hands': [['FERTILIZE'], ['NORTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WEST'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'STRAWBERRY', 6], ['SELL', 'MILK', 2]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['DROP'], ['WATER'], ['EAST'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 12], ['SELL', 'CARROT', 3], ['SELL', 'EGG', 3], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['PASS'], ['EAST'], ['EAST'], ['PASS'], ['WATER'], ['SOUTH'], ['EAST'], ['PASS'], ['PASS'], ['PASS']], 'market': [['SELL', 'EGG', 4], ['SELL', 'WHEAT', 4], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'WHEAT', 32], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['EAST'], ['HARVEST'], ['WEST'], ['NORTH'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'CARROT', 9], ['SELL', 'STRAWBERRY', 6], ['SELL', 'EGG', 2]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['EAST'], ['HARVEST'], ['EAST'], ['HARVEST'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['HARVEST'], ['HARVEST'], ['EAST'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['EAST'], ['WEST'], ['EAST'], ['EAST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'MILK', 3]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['SOUTH'], ['NORTH'], ['DROP'], ['WATER'], ['SOUTH'], ['EAST'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 4]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['DROP'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 2], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['SOUTH'], ['DROP'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['DROP'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'EGG', 3]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['DROP'], ['PASS'], ['DROP'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PASS'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'MILK', 2], ['SELL', 'EGG', 1], ['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['SOUTH'], ['DROP'], ['NORTH'], ['WEST'], ['DROP']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'FERTILIZER', 4]]}, {'farmer': ['DROP'], 'hands': [['EAST'], ['NORTH'], ['PASS'], ['NORTH'], ['WEST'], ['PASS'], ['NORTH'], ['SOUTH'], ['PASS']], 'market': [['SELL', 'EGG', 4], ['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['NORTH'], ['PASS'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['DROP'], ['NORTH']], 'market': [['SELL', 'EGG', 4], ['SELL', 'CARROT', 1], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['EAST'], ['PASS'], ['EAST'], ['SOUTH'], ['NORTH'], ['EAST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 3], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['EAST'], ['PASS'], ['EAST'], ['DROP'], ['NORTH'], ['EAST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 18], ['SELL', 'EGG', 4]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['EAST'], ['PASS'], ['EAST'], ['PASS'], ['EAST'], ['EAST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'CARROT', 2], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['PASS'], ['EAST'], ['PASS'], ['EAST'], ['PASS'], ['EAST'], ['EAST'], ['EAST'], ['EAST']], 'market': [['SELL', 'WHEAT', 3]]}, {'farmer': ['EAST'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['EAST'], ['PASS'], ['EAST'], ['EAST'], ['EAST'], ['EAST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['EAST'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['EAST'], ['PASS'], ['EAST'], ['EAST']], 'market': []}]
_PROXY=make_agent({0:_DEMO})
def recent_demo_agent(observation,configuration=None):
    return _PROXY(observation,configuration)
recent_demo_agent.telemetry=_PROXY.chassis.diagnostics
agent=recent_demo_agent
