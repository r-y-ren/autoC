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


# Public actions only; no hidden-state or rival-identity input.
import base64,json,zlib
_DEMO=json.loads(zlib.decompress(base64.b85decode('c-qxnU5{MXar`g)JP+QTB_-yKrp6LsN-L0*2aZ4(2I3$<;5;~a3-aGXad+<Axm{gV-RI0oe&S$edGGl?-PP6AKmYH|zyI|gfB)M*ZvN%xn;&0)_;B-Sck>^A{jY!f@6TU+{`mL5{^LLY_CKFL|9tcNpZ@%p*FU`d{`I??-OZba<IV2&)9&%>AKyQG^V6G;pT9qTcX<8z-xsG}mjCeKyTjqfU;fLd|Jz->^X;2I{`BMOiOJhP9NxV<KmW^{zkB=sa3emDM$4xC{-?L^zWK}NLHYR8m!~Z)TeW)mzdQBi`Q`ENcvrV0_U`qY0~)ZOZ+>`q|M9yo{YIaThYufbKFMK)6PnN4(;w_F8uIw6-Rc8xMs2B_$9MJ0?QEfMSR*zsJN@Z;(w_$YVtUbckK1T@M(ipWUVGr5Ms(G#H?N<%w|rPe{d4nv_~l{WAKpFufLik5aQJ5VeRo&b0v{fJx)@71;G^%4!;3cIdJxxLzt|?9e|r7#@SaZkAAV^~vZFR#0c)E)_-STV4}N;p(kl3d(cwGI5$w=;k1j0$BXseeWv>s7TR5B4`@$YLyx#7C(_0?@2Oih+Z<}w*@Bilg!;hEmKfi4?z}0az_Ih_c!joQHH1X|M9pydP{1;EW{%}7%0bOLVd)ouB{5pKaJmWI{ry1a<Pvn3FC*5j(mWEdz`R3u>yThB0fBD1V{l~ZO-u~-l%P;$$S)lUVAQoHAI9bMVV+6oMVAUmJdfbs;N@ImA6KR0ayK7_ekjI?NfK8X7`Gh**Ovly`xx0Kme(cj7hPsf<le~1#t2^m6ZcJ^VtzLrcug7lrt4>%jv6E@n&Z`6LZFeDWU0^u5n`;;}XK2^SCM}!jY(%<yT|Rqx<l@E1oeIY6^nW)W>h^!@(bsqgIF6Pbyjl&iE%c~>YwdhPs)qxEZR3hMPeEqM<yvr_0yge4*3r)yn8KBTH1L$wsn%Et;4yRUizfOt!x{kyP60-VOEN-3XVZmVzyrseZJwY$0-!^7J36Sqb_r00bz6HDiL`oF?ZGcW9zZau>r(+1#PT9=prUs(_ZHr<TL8G=Wg{m-UH%r-^xf<Ce<DL+SUD-iI&ENx<pE&r;2r{uslHy~P6AIq52iUR^0I<Y1dxl>Qwav1S6PHm^H&%E+J}$tUmt&ec>n&-*3d==;yk^}=3Ea=00)Xr>*ns>ZJHoPyVq^%H=UXR;91&N|MhWGEh7u8wdJ>SJC^aE^?uNO&;VvZj=cTJ3V|<2*wfs%15Y5aP7B`5a2vqBc)oYXV{fXbW$k%@XpUIn{L?>|jh;qScQ%^1ZR^WV4Xa%mkk>cc=?Kg*+f8t=VZ>`#MI)C2S#-RaGEzqmn7DA3#(<k_%($1YHsDZf%P8Z!M;nMv!s*SS_uAS3BXZ}uJ241@toevB61#iuDuTWd*zC*ZOsDb7WwLr#^WOC0=+urHvKd)?9RLfc<H~K2J__?pke6I=h+sHBb3c~#NL=%htG6_C6OqAph+0%~9HT`<j=`>D6<@Lp8`#g<4q|9-_yG37M2voiT!s;7-2cEY>$v3%1ikk*aD*fKmQBrINS(f}@|NwyFgx{rj!g|1bj(CkrnWTXlo_iHgetFdqFHMaID1eYfEi?ip52^Ir{}!PlmAKK@`CvaER1Em>X!4}rvaPQFp|;H&_f5w_DkPhvE8{DZTUNd(1cnYL6+IZJ@MS5X~yh+ZA!7uTZsHPY)oBUpJ!T~<MWdjYf2o^qwydbp*(*Y#D+ak?c6Hn6BG?)-~+@ruU8du5%g%Yj-DAXi5nF+R3tt5_VYO$Oowh4pp>51K~862!VM20@d+A(=9#vIPOwm%;}<+OaomU|3{{KdNRn|pqH4ov1~0{z9{RiZWzT0<mizX6F0F+%pdu`E!n$pP+SCY-E3XTanpaB)TG8IcvhFwdM03xo<*@DRHM};otCM!gz5@0G1C2NRoa>_T)2iiv-6hmh?R{+Ez!I`_-qtZD$qrr5n*#4k{7S&h?9#ToY+pt_AQyG_b>MOZwueD)i)bNUUD$s0k?C4Md%HJh3|V|1@OiYMQ|w3q8g`zX2TQKd<TfLJWG)K)VTS^P4x~D9yKDLta_d9-!dF%>FEtKt(=RRSq-e1K>l}v?4Lp>5AT5ae4zRt?7b7>hS(A9E_W1Dd4)8#DlK--7Gb`BqK<<}QyPj6tXTSKH8w0+i<`#4hBnevDa;+d*df$hXeqj2X@s1F|e4H9*NEbZu+lPk_hZv~OQaJ&{a9S+uCnbZWCaB;zoK2YU{`rg}aNe`1F(OZ9Q;v24ouK%GKHVMxyEhL{8@HJ-i2Jy@fze86O^@4E9o#uDlQeRGTFoXr`!KU#u}%4Gx*a&18$8?m%P_5<RSu!Z{^iUMzI1l&3597K=nvO}J2ImznzS1s>yve8Zota!-A+q6j+Ui(g6kU`o13K`dwO9%3jCbemxTkkH*Jw$zTL+8&eMxpPopI$vy~-sx_Z$KAte#-L%1l>f7tSubWZWk6~ovx1g*%;TyY0P^6(fOd97mustm;=SF85y)YNv>eH52UXp=+-Egq0D<G><`7IaP6+m|IAcRpV)Sn+C_xR6wsf!~BENpdnB9BavFH;4wI%tNq9D0P&EeVgG39_nK>(`{7v$~raIfqo*mkwM`|_rUsc@3KHjGq_mD6kG9GgYBdSW*jXGHh#kxH{+2nFx=4zHbSO8G*BNn%Gd`dLIH3XCqlNVi09@8piM?Td!y}VgeyuZJ$xx+I5}?iHMFvZM8$6Tx<e!B?o@CI-4i0VXb*8uaSG+WaDWSkg_Z+1vkAiN-+%H?@k%@yUNE@@wyzB6{!=3>fkwsevP+7hBX^CaIvF68NiuMN?o*TFz5q*i%m_g59M;@Y*J~utfpG<_!EN(<2>~&*X*pCa%4IweqA5cm{|Tgj`l66ghr}uU9KY1z%_%B8xQC<Po0hhXPeK>rxCadmbVwJ(<^>KMI%y=?l)RLz0v7zKu)l#_#gi*3U$jEs0O9#xgEsJWW+Q+9_T3-9gew*E)b}9)n5yFGY#}Y1X=!Rgq2=0tW+s8}hvphCwQP&%Yd|TW=zMAy&_Bqd`4P_q;9<nJ6FFmxy_=JSl><ah24%#}@riA}Uin0eVIAjOK7-^;ppBHWK7cs^c2G5}4a_QMiY5riFK-6DSjM}xvd*6fD}+Vv3TBHKRh=i9tAPvIH`fR2cTT3DqN~`^5o7k{1Y0uNOio5Cz^181GOxXk`ob#ukS6VBrdpm?TUIg2It31=q@9sN=Nf(}om15VP@(LP58uE3_)zAdL^kI|2q=KjB0v(Eg4HBh9>q?3X$u1&Y9@-5C6x51KYeOPHmzH8rW&kIyO{;*(KP}tL<T*81B5P0V-i0<=>5aTl{p~SDhuROp)faa=jxmGPKtEhh@<Xlppvg*#C!E)S?-|_#a~`ilNWGCJNdM}=PsHs%{ZX(e$-y;2+UPK%NNsm({waAycJblclihzx;khT@zgZ;6XArQb)#28Ezrcz9AvcQ_CY^4Bm>>Aiuv5`$8tsXwJ!zi!=NICh?(6J=_b*e_R>yp$jaC8AUP<}E9KZv8K)vC3ir)y6y=1*t}x%*E2@SY>}RI5aSECG9Q(#IS?1)g#Nd(ge-v=!RFDeuu`_|O9Mof67a$gXaM7>SUIZadJNSu&oHl#r9wVmWY&0bTx)IU1up-d~tYdqyk%Z}xN`LK&_kwx(Uv=wqA+Jnub6^m(v6g+}2r_5l!HoWD7TM3Vwvu507$i42%Z`+S?ZHr{L10KvM?vkR$V1N+1a?o(2C=cy6?{U`;(4AqT6>^1&@##+;U4|1F~l{R0Nrc(&PZFDx}X^H$RUY|n{nHXsh|d*Sey!)d&^+G7-FiH9HCgUCh~HfHA`J}Fktk^20ylR&1%dRd4Lr}bLbGc@?kElIZ3Sd!ql6JBACKtsbhR!`;tG0yWb{oP(=_(XS?VDm60r}%z*P}{V3vsA1x>W=|4V_1@?Bp=<)CGEa(Y>9n2G9bQ8LoDx*wNft!vAC@w{FE^)3&L+2kP+Q8`k#rP|KM3jXPG3$$E^1_7>2%{F<6sm9wTzA;G>CA(jmjxJAB<ozdnTB77=i)JwmlJ}(w&LZ{<5DIxQ)B`dM(D&cnWOnDaqwez!FIIj1z8is<XoX#w1N!nRW>Hnp7ye=kc0fkr6u_|tiQB7@3B9-eWRk>+!2aYLA(sW5od)(SN4G8jj~lqd^SlyA}US5jRBWM4{C{v?s9>dOrp#Ggc>YC!LVXyZY>3gF@bm%=B9%JR^+%7?8%=vdH5cZT7z1qagG>pV!F~$uiV{^H1hB6HS<WJ)p@8zVOG>)hiUWN$i*PU?x5?5B3ws?)a7rV&^7GtU<^z!l4yeuPK}n%Msbb<^2Z3pa=>Cf8I@h&?r#oQ(a?b*Fl(#kgIfw2@psRMabZX*O;f&0frlI;tqQ(XJ4K?tM*=~}10K>?J>8ML%?dw!`z=UXW7$Enu2nDru{CTah3Oh0!iJKr5<u#FhU&3^?BprHrFvQjharHZ=fo`kaRW`7RjkP#Fb0N(>|h}g@toACWL5bpyMRS-xM%>K1@}yt9(!kL$gFT~>K&!k&LoHalr$%SNdj9l%u-w~6f9<|2%n@h4^`o)g)0KrDdSLbN9kF`R`Bmef>`DJP0htAFhiOM(`X+a1T&eg>AU9sTwXF~-L?yuC7(fb2?Fj{_Pkl{or{Djc33$(gC}LQ`f^FQS&tiwIPhA9`pc#}$^f5&+&n)fXyQ*I_dF>9mFLE=lg~W{IF>W8(9H7y%wP#*wT^_WOhON(Gk8KC>uV&_X8Yh8uhlgQSt2R+s2u#MNV+1brxe+9Fqd|TU8cZf0^iC^;V6xqc1m~hC(k83rQ-g>iBt+H+FuJPf;1M5a&nOiPde~)UYecr6Jb{oy~SNxcY}J6&WaQ(AcPiY$=vScM%Odvd&5>2&D5(q#X&;_^-9hf?rn$nTU0v|5D9SD3B{HNK3c$*oerRwAq8GFmM2)7JUuQ<dpdlXq2$J5gMgsC09Z9k*+Y0w^@f{17H(Ec&H-8v<gmpfN8P~+Av<CX^!&EZQ|1oA+3|H&22sV!twn{CI~`g>_zbj|7W}7dAr*FIy`l#$vTYB8`5)^6qwGRuW^q{r{%d*px$-y6k?BEqhg734m5{yWLbTK`7$`y@bI8&|+jEt6Qz5;EzP0<jJzfNG3GPZpM1YZJ19>_POLelVYoMHUlpU9mHA~?rArriDqV7g^Eu&`BLL?NP3zM!Ea$)W)9gqxbw}K?V{Dyg&XnekT`|Uuk;HfnN%fdGX0I;QLDy~R>qgCz)nqCM_4q+-nJJ|~;o|^AeniH*H=a#R!OTz1xcEXnk>Fw`USW;F2!{l7mnO5{<V{%U6U@NJ*u#54LZ3V!!uYWxjRxTuzN6+uEkKyHAJms?Ow$b#tEG&3Xc4P0dbV;?sMwyC5Le&`$--z2+<ldXyD-gt#v31Pk$L6|MHoJy=zysgX^QQn?p+1_k!l}At2Qh0G371PFQUx3ZK_khtl7h;!Wof!7kH6c5eqIK2%TU{mvRVv$lS(FAde++~Tr*-F9aydlYKHh)x5AY;2Eb?$MmCGvF8{UMTDVzEeSCCXaf3f6!%XDhuq*`~vnoUxTzr$K2KGHs=3O&)lK|%)pvjHuxnL~4ELQ7Kaa?lEnk!&==vs$J7S(LQxHtj+wq&?Dr-8;c2rF3Xh+hQih~YG{QCO6QUmjVH>AZokUP*X@Z#e^#hCYI+Jl$gn`k)b5`gomFfs8pT`*L=@fK8nOos+7Xt3t(Z$O*Bnw-T1Pr#7(AX<p0&emDsY6qJZ%L_Nihbxry^qy1$NX#IkWW%bpyfFK1V0`ykU7}AVPLejYy*Dv4P4&gqr6bXp+`(`UD4eOO?V<^wA4Eta~+a7JCLfXjrK8iiptrv>Vb+z<7a}=cgJ$~rclC!i*<us{dI!0#+j(XeI?=JZ{gtP*#6El0SxTr`yJx@H=6cWKxrIp}Yc_1F{<g(gRglq<Shxe+fgdwt{;>J`9Jq~4-h_nLHv0Zm8c~feCP7Wd063F~jUf7vU0TD&!<n<YR>bza7p_i}e9RH^92<=m8@mpYGAzx15j+7hR&blIy!V!dB@aFY6P_@dEXTz<#YboW_Ea@Y{4ula8+g~n9#*>5?%0p*opq6Cx99qjvWds$lUbEJDv*aq60jY8(wMdo1=tSvpm$!BhY-M%AqFG?UHfIO(nf20<n0&{aQ{P>a#q*NET7oJQfRoz<>bUz<$n~SuX<cO|DyBeaOwWS++}{4m93V$FL(4DKAfQDvywNQiW8f@~ijh>L0o~atY#10KA`bL81bmBPF`8n!OZ3cr%uOOE_>Qh{fGX*A5sYK#U@G(O6v-g+&chjXzVw)>l%ci2>@>%c0#*!4L;i|oEBkpkg;e?^y~dN!^>gRE?98H$(dqpCon?5Ed)JTiCGn+^{NKyK%@jOT0p<2?hsDXjqIH65doPQm;7n){HExvGtxxEPu(j!yH*N%<U4CDoz#KVBROVaeo=-sBXrd|8Powm@at?3s-#hY$1uwloKCrSa>(l{Og2Ie-dr&(oobgK{ke@k5!@IzUjE6#A9iUG~474Fvsfm>hHJJrP^B_3!yYWP&jBW%IIjNw<acC`hJiH{P8_2uonE=^{1uZ$p3^4P+cn-bAxy^ym-1ECHvNb$PQcU)QsbegwSw|1yDd<@WwLHO`BV17g*w|EGM=-*!z)Y8vs_K}id7ALmRTab6`v}2#FP{&mI>+}<omkJv{*n`dFfFo&O=8PPhnS=)t*&5mu(%Bd1q<;=3ir@Na2cUC5xFE~^?ZpLu2XavRVSi5Fu8+aXL)46W8T!R=j0r6^_B{Dcf3YGZ&%||34E}EN7Rl6%fShYSrA9FU^g>TkG85jTKh(CI<;F{ie{0RdGYHPpF}vO!UnK(NObpjLscmR4<#v*vgg&Diu*<+dN&B7p85*)#fMU)ooWX1FoM?(@Ji&q^gP4bEOPN^8VOptzeyq#$XVb~EJ~ipXR_bfG(2JmadGWUgNrbFyjZ+hTEZY-(t<>t*dw#_!z7K_H4|Dm9u;hvE~ZbA^W%ZkMx)?}Q7p1nc-<DvXYMm<pD1zZ-;HL?Qk(rkck;6L<JMcPng~MJ>YLX6)s9}U!cu0%pH|6ctCUnIq~!o648)}}A*v8b;%za^-Ky{zGQvjF{23q2q!4pph=(8Quqh}J?t3O8zl`08D*Wb}9+d#Mg6!NxM6Vv^_H?2+)XQN8+InMV47B}khJco*-|dG8XluIJ<##V9%TEClyinn(!5Pu%Nt3GpLN~cuF=A$(lFh{$&ec<<YcUUnB!$t^Mrid5&?HY4s|4x+-H-TaN&1xshBy@kXC&rzX@9O5Awh+@q8v5_5E}|55wnf1Xnl<X*H~fC7Q<7hr+DJrjvNQ|0X@QupCFlLfR>aY1WFP?SV#AVmwlU+2}x3YYvM%Z3S0_1DATm!$x?2e&fb9_sJ>DeV3nBQR@Enuoo+(kqj^TWG4rce%**w%tLLyZFx15K^slXzvbv48+@m$AD<^xIQCuaWEdo~<MUiTjq^iJMj*@`HF=5a~h+1BPx76VZb}83Izj|vz)qk;~2CQBjL|WQes`NAiZDgTv6dj^C#H*F#oQh+cg&L`q$<L8Q-hp{C*z08_!YG39^4H}>J*#rl#pKUU(sPUB4QV);dchDBdu2fN^%{8q67K0V&6aXz*j6R?&d-l9>!H@Fve}w8#}Z?}&m*9C_>34{A!?e~4;*YM89<fFv*eybJGN4#*isFs^B0PW+$?vFrm@4LfE!RJAHF~mv<Mc49m?ZX2dBmzoLe{ri$=-sDp6qwQR@Zes8Q4ZS5F$s)v~E^<W-zg()rVrwL#S&KmFL0dN_1IpKCHfp#LD~M)CTg=xZ&98pLdgsuj0COl4yW$<cNcH2_kbVoCFgrlI5@4yL5Rf?S{oZ#?=<tC4I7$~?Sa^!M&E1V3@cAa~{z$YmAHsO8!*5oI3aq52gnr)RV4hpXOWONJ(vP*l_~>-DydW6NX;*ePyOPEGxy^8RLvgy!;t35fgvN-(juGDVZX0!s1+PiooR&a^}jkF}b2r%Tq+3XkRLVUQI_f7_C@nLsIqIwi^E#V}=ODXTe86MR;cxWF39+2ea3oUsHACvtT1?o>)BF{rqr6J;dkjSKgZ7)uvwqPd7IcT~#8Vj)mJm#rY^QHYqZn6<~iAm%spGMJX2pErZdvqn)irkKoTW(tbO##f*k%mhgVqoo<-hI0&?i#hqGyeg@NIL6X|nIXiwV<@WuwXm%`TCS}xqU5W^W?h6%c&?)YN=ml1$aD2yLyC<PtvrGbiDS9aNyYV<0GizMqcZHB%FiQHL)E`+mRYm`RH8+^g=$W0zNE45Y#n$ER-@`flNklIQrr--@;&h0`qDF`q;LT4lv>e*7>3jK(p0)Dp57#u!p^UQW7(aaC_;cu6pQQ57q<>eGNVOeuR#7J;e<-g6V(MXi{u%pMf(|vVU*`D!+|vXFicE*LRAc5GJJTjY*XmgfW%EdQg|vaUjxJ>x5x^5C;<3qlx{d(`Y*R-!!A^K;x{z&QeMS{D&al{VrU-Md0A8{t<2%N6nEMT`>Wqf4qSnwTug&oBgfZOUKetz!e}K|l9kz7man2E$2s!_Ikeiot#Nx?rTQ5{?S%uOlh+ubE;gg>L_lyBnFU*X(f^8mCOn6o(2&Z3)*AVR@fCL^rU6mgn5B9biFaPMcQ?z3B8mkSVHPkRuBroabp`aDi_v59ABr3s{cXsy9;~Fba+PI&`bdt+6b$s_1Jb-Z-ZGEnH8D*>mEHqhJcuUnC6+;<QsQmE`_B<g5y&v4`|YZ<wNhsS64-Tdp5(-ct5wQ06@BYrRJ4N{<Wmbmqb8`WOxo$yLCt#UVCpbD9rf-4TqO#p_m&=T3t50V&KVJQQuJ4ckMgR&tAx6urj>9JK0qNXr?vO=smyy?<RuY%M5K!z<~ez^v`s1SkoH_DR2?sLQ2Um+GDBB#S5I48%TTyRR^8T1EG2+0XE>rk8YD}sEe!vJJN4HWOUqpGYZ#SK`W}v)%a@MaZF_b%jHoSv%KfjvR7+NC9+jfZwu^(iNmldJ<E1akN$sGX2{zj$LqZn~n$Apf6DE;{P!5;)1U28T$umJpSv)CcjrkLPJpf)7dJOgO3uQV16((7cgc7Tyu*9=D?IyE!f-R&q0Tv|UQ(5RF)-~d{HriCVVr@^XjHxHc#lyWW!3`Ttccdv=o^DW~#9cFkQOT9FJPUhq4CexR36318tEFfjEpzx8U<PWy39}6sHT7|e=jS(iDtA`gTyd|(8fo{v?dLZH0fcL8@a?Xj%IYi5P`CGZa8A<($xCKvbu!eeRZYuQreF_wUUFSq$*l%MtWyV=uB@tDEsg6!r&Zv>`LL<xB5=Oqdg4MAX1XXy{q|)|SWY6R_X#loZO-PmZ7(GTfVd*~#ntM&8PVx#pt_BRZmC>mk6RhjIj{o>Vr}X~E%VL%gmU1Wasx|g#%V~^-ETjqGXF)&5XxON54W<pU?~aEtwlFf6tP$Ku)q(a#N3j0pkr-xvJnd|cnvAk^0cMWaYizuPXKeB=Nc~wOc`hOR0@i8BXY9VS3$OOhSr+_MDl<Tw{-2IFQ?d7woHv2Wtwkw5ZPojhfI;_a#li}=u=-Yu&5B?%=l}F2c@euycw2Pps<p0=Os7G8H(+4P&87`%l?#b3WK5FOtccUabegx6z3!<RW-T%xEltF`B*Fr9)4F6yq#K9PUXI;<^XcKBgK(c*XpewljO;Gi!qyrOo&w|yvjI68=EaBwQton;MVuNA_vvld|sY=AkhL8Wt@Xdh3GP)!4$I9wGO&L-5D_qr0vecB}HeOsbduHGf;uAjKv7K6n5}VxYPuPEn#`Qs?c)E(g-?;_bFOPw>IEogU}5Rkvg-!;j&{+{ayZz89c?@FP=2%q>Mt_SCO<htcQ;pOZ1TUXK$C~9HV<}zx)j*P@0-#1$DRER^B8LC8K45dn#lV@v-oFsf%AOM@9)1wj7!Iox5w-kRxM}inP!|C+IyYJqFY$J*4uG>p)Br9#c25tX|(uO>M~(Q-I2%x+p88$IPk<O!#%X8UF;RAdT^}z+<SWhek0rnhtK=!4c@v(uYxCxuw7A)LdwYmI+NLuM82&<gJx$o|>NG(fqLbmjXz;RXl?g?N?4IDn}8}L#K~h)7HVLm@f(w`E@3Xoh0l~fH+>gHYlf(?tIoXyTn~pxNIcKtC`|kf&vE|Jc{bGr10lKwpb>&5C`P2_a(?(cg-OQ*XFiU8CX)Nj~GFb6*Hcb2-cditKd`sQc9u_$sDfQ^=q<);0cVT2lN3H>V5pH8s|YQCCHFmG;>&bJuZ<<N!<gnL+_fYWq4SJvM8gQTxS}4=m~+zn}+6OiyYIq2CF=_^}R`|1S~|Qt3h1zYdVf5G)i)gU4*5gLif0`u378Rb$>zoeI8hk{nf{b-TX#TrMDmkhg_Sc>bg||5_BfRV9+Ii<?IcZvp^DyDoIOdf$1pt{+H(i`y+ML{Kp|uh^qzMfqN)l2X7FjNyNo>MB?wZgv;&<>iEo)VIe)AV#TulW-u{4wet$n#+`8zL?6;q?u#dF8<ZUBjIKbH$>r+367LKe`(C1-bYH0LnC1}A>REu<G+VR58stZm>pniCcD6{q5v2#2uc`QKQ}!kUXROTAEWxW?ti|Ia4QelSBq;$_;Aq8r$$)1kO}3quC$vho<GIbFM)R=1LT)Co=54|{EAP@%Kc~`hytEXR^R}bfM-ReDvtp5t<r(A$BNQJY=%XRR=@eSMuayw-rPKMIIXc?=UI0!{M3owct`ak>+oh^8^w0C+z=Wt`IUt_lp<oNVg>bNYR4r2%(4^}wCAre#pd<y?D*3<`UO|4%L}>=g1pF3KMV*p6b#XJG4ITcTVuUZ|FyL6pkRWwNT90;HJB!jLwMlajD42ChJ(&6#T~-^l&LX=7{89AeCZ@2`sHvh$ax+a~(tcW}Pk^KK4CBfcRmG>2?{=#GL9EHch>bQ{ax+E3o>~wHqZK>bR@BmTqG8P~<_0TN6}av+b(H`ClXwb@JWv;25n8g_D`i*^K>6VYwLt814JOViV!#T1+Iy;4>BDFBw6K(+@~sS8GKEhv7TWX61#pHW&qZSMmS1Z5^t~wa6r9zi(s2x6ow}xTv=QlA@=EC1ymGD*Jpzr<BubM?g5Bs`&>{ES2Nlb**g!}_rKyWjs>0(9@d#ywe<{`R5I#<-9vk%Nk`z|~yXcfVrp^P+AlGIy+}Ugmv*M~$5R59?c((}O4-6~IFvy0uCmMR%UoS=NbU@uTfmhxv-c(ze!>G#mPlR3xBRB`EDzHaS(af%N*=4e&QDiqBQeYqve9q&uME@n`pxZgMN3-V3a2{tT`;n&A$~P)2s*rl>02YL(=84L=`8*7*vo7fDCQ(^1a@7?|i0Vu%YQh`2bv;CqGf140mYMV0<#BRw#Ug17@Ld{|3|*1CK*+r2_(_D?^`fx^7dX!Ah6<dVk_Nq&*4yo_p}18U8w^3V96pd-cYklvrt;)Q1bwnXGqUP^v)Y3x=A4wMKdNl`3hF!`fl7`ey%(D4IbN!y2V$?%Av%1!qBgWy30ZLWMhMQMl_&WXDAGI9oX-i0mumEM$#%Mis=<+ru9bs?brjS~n6<v0U(&QF!bsE3sOprcbFG6vcYV4z<0t^DYGK{TLhD+-g>%z(G4XCon|>TzF2m>+o?kk~C)5<~kzPqv^iQy6w=!ga92NhX5H|)=Jc~kRjD)KUu%(xD^3asYLf#vs>Lu-9h7E^#<f!0RD2w#=8IduIptY~Kk<J)jC7qL(psNUy9DSn>L0?zb_9qEQPHkgR8@Q!Eeyrvp6mC?dOr{%*MFVoWwJhg0;wP$r2blS|v}s_RPkFPLf;2|9U$v<YsLp6)1&N><xxcFm#Vq<PSH7jtDzG1)9@kOSvP&Db7E7|;`R0sDj0uW{Z9IeCq*nz>GGKS0q&?7s4*_#^={K6Uz;xlL#Z-)hNG=1;POYdlOD3CL4MeTeYO%9JUI(?F-%ib_yNc6CATG8T;Nmt{g~|Eb#xjKdG`*}jx+7>UdNh?%qK_@pSSEALl2r;CD=S@5@k}ASc(m($N8g?88s^vMrfvL2<^87h_JA2y=3Ck|E+=HdQN|m9b<{aeqZNh1CM@58n*CJC35oML>|B`3mLM80KUJ+mGx{p?+m50Zh1Q62a2U`XK4vcgLbtybSn>G)cyn0JxtBc+Z0TX->zy3BFU)Z$oG89_lyW_f^^>`fqEgp)_qqCWi|*z5du2I^76tQIV^$j;dIf-Jd19Sn>%#gvy3wo7BIVeJUqaX-kxkLF*6}<$wpU6*<Enl<os;Im=Tk7a@T>%!p=wS|7Iku#=-G73L^qQPX;ouN=C-5|x<dc>;!3<xf$4!YTM1*kq<CAJPAM+vdO%<6*qF(=a5E8wqrO2FUY4^{@R%e7Wz<xLr-^`FO)41gM~kMKLhZE%3SdFrTLkVD^#-IDabLm}C~^c^2kK~Ee&hRYSs+%yqBNu9XgPGHT;2VEe5-l11BV&kN|pjQih~zOCLS9Mx0M1@Rl36IyW6=FVCpj%(t9!+H6j!DJ=%dr2%e94(5;X}3n3pX1drRhY?Zj8I8O-0rPTM1{NM{sAE%TMrp66E5xf9vy&M~BTp@DGYdQ|6NS1POq(eeHy+KId23_DVDZtk-`Axe@-~<#AX*nLELPbeDMLKfT)rDPIwg=T7Mg5@${a2Mxp??^=sq&qoaTN|UGvO*Lt8zGiP(-C1Yg`M>q!M47+;B2HH_?ui19OjJgjDy7AEMN@i!Dpb_zE{5S5vH8)4Oitsn<-Mm_voGS#4;H^nxi~1~7gA?X38RuN?i!oN>fKiQ~a1&zF6a{R|4VDa8ssnNn>gN9R*TX;>nCA;UTU->e6(+<HB1=dt3FbboqHO|Z<TQ1RLu3CwusLrfod{6II@J*cxC=<;{3g0{ym@-UzNA4Muz^8')))
_PROXY=make_agent({0:_DEMO})
def recent_style_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
recent_style_proxy.telemetry=_PROXY.chassis.diagnostics
agent=recent_style_proxy
