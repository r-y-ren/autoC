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
_DEMO=json.loads(zlib.decompress(base64.b85decode('c-rk<!H!%<a{QM$&w=b7Qj~8avR5LO(g;Ix8*70O1b7Vt#`+-pX87OD)l7H4ei<1NnN>Zc0iQVN8TPAJl~t7)85#M@e_#FUZ@>TjZ@*vt(=S&)-@bo;_38TR-+ud#fBDbPAAJ7t@4x;2?|=KR&p-ci_1(w6{(Ae<+aGV=U0q+jzT012KmT<7@bS<0cW*wv{_y$p{SUj_&;PzS{O0%{-v6-M{k-@ug<pL7pX;+xzJ2}Yk3TQQkc{{J?%li7i2nHgAKu>YuEY<?Yd-vbHI(l@zJ2%R*U!`T;o~3w`#6%tD3|ZYKRi9m`aAx%>q&ce`+A4w?3b&b?(RSQ@W-p8pZ2@=AC@1<IfnL-FXH1LY|n;teCYb=*Ky91k$J;-eY;+_`1OaWTdu`vIOMl+K<{_EH=qCZ$KAWTpRTSq{&YRg!_vOMb06OZ&ELZhdPJ+|{^=jTK6`F_Mw~G?hd+HdKId#4t0(Sm*Khj%?qjgZwK?PY*x!EG-IKS@X8Z6QxJg#8QrIlUljD4!R`B6vmQRU8IehZ){q^-e%=NjUrSH3X-1#WI$=_;IKYb^C-k_<+=PuTD=G^;hAD<B(Z_oVsNxjhr;bPVw+=AstYm+ap^4itluNH5C(a9#yXXchp`_ut|Ex$6r36FCw`-@C;oI~M(%$s4hvIiqy{V?INrwa`1De^cylgXEqzV`LqyLY?SAAbGQ?*7BucW?jsj{znwb>=oF&gSAPeV>yIl^xOadydE7YD9_q6;3NYM~i&}{}63j>GdSvw6G=hop0{%e$EW>@ps3MnAxp7^-c1XN5}Bt2RZ#4fBNCgh%5}o6|P6%xPf3YmZpamZNLtlTl#2uhv|PXrSi+hIez?P`F`=cweuDR_+WdbFFF3-<Cx+?81w88wy@3CP8xJ+jvkcyw!;m9LyyDPJWNCFu898Xz|E6hWK-_1|NoMw|B{Lu&_vee`wGMU0|T0p8`yU*icSP@!#n4Z?Mh@HpP$nn@)vF@=6pPkaLju%;&=0jAij`aeVm))4;B#NUvx$==zCaeI9uO20FyoqZOWU14d=aT<-*JZXlKwA20VVv54ZP!=?t8I`|*nq`gwe0>gB!vaDTi1Zg+qGS8u(SFLAsxVBGrXMl2rC90hoPfE$CctR}l=8vr;yJmP5J1%LN6Z}8k%Ic#WQ4bO5p*Wx+HgKoK?A|gn04srItIePNQS4&m8qCl(>eHie?T?p#<-2?{;ztS%T;ByN8tUvm?(Vz1x|C=GVFZu_Ubn_^}`P6<M^Esc;&pSSy`FT(6)%h#{%iTjxhUq*R4~$MAH>K?6))ynVn!tq!&qvEI%qE#3U@-BFycK<Hav$#e8aq2RB@SX81*btTZ_Nl}wnn{1TCE8&eZ%Np#0lZstm!UBM=e5KYn$kKiO|6!xqj?3YP?LiT3`c$$B2wkb(T>^(toH%lj98nry+?BR*qkXeG>=30}W_i{r3mEj7|B<#7kE*OZ<_E^w}ZtYsm!l;oT?lEnn7r%O}GYdr-%K_xZGbD7X;|FFxv!o*uRKNH6P~S`5c==n;`;GS_?#B1x9j@k1SSlD~lRdIr5yhFey>)8?!jAzab*Gx1DdR>y^x-VVF?(2D@4$4v4+9|<*>Hw|v64CZP%0?flj9Dp+y3H?FUGjCZx^^1>w#?f|;Q>W;vRUr4c<CfF1hE<)lYkJP$QGh})<?UgB0^rf(4=cZHMs$++${GDY?c*Lc%zQ?GR1X23IcghMx8tpoC?GCh>rD5-+pj8l|CFBg69c^oPwafUZY~4%T0@}D{ygV9rPfV%#v?Us+!g0_MQjj|Iarv)lAY%K#q1Xf#b3W##}5KLOEf9azp1*tgT8-cLiz=FAR1(|S2%RQg@>MzBBGro+LOFJ2&p6cvQIt*FAf~^4!0*`#J==N!z{?L%zBG60wa(N4RTVxtvDE^g`^de&_DJ0F<=kUQpv?l>>T)V-^H;LdRH^RU$NT7>U8M6`y5$El&cP}$bxe#5a*yj+j@!G6E6J<(j^aXa0xHmchF&&8l6*k1~Ou53nB+JnX_}&gv75oi?A@D=&qh1ip(Jc&%tPiHK3D4+}*uf+;g8J-8WapH3A^>i1$z!e2pkNqf6u<Qf&tas1#DsD%yhX9=LYmj3B1y>U=L})idw}nEwf;Dn)Gx@RR3H=B~4|WEvTW?nzGe#Bv!^Ce2roC<dL#DOyt#@CrFuq_S16#V4FaB!OX6V2GjX?Mej#&wRo-UhP$Deexioa@eqVrvMh5UWHlu0wPV&T${KyzTU|F3dHGnh=xn^^v7srPd^btyF>z_Z7!yghX2wWkLPH*BW;DG;hQhVJ5CP*BWK13zCl`{na0}8dT$yr=lgLZ%<=duFj3X|<$=r5d^_J_qlXi~AZ@aGkjHP2Mg=Mzz>BCiLT1*IP^ro}Md6Dz0WH+gg1cE{)v7x^m@g`q(1I}6R8dCPt~+@_!h`{}ZSj(aG}mO%<<VK{M#s@bL@Y50I{0qUicBoUg0|piAzO&0Li4m<qUi!Zmt=7xF97^7Uyr7a`#f2eHe5It1&MU5hIr8E>OH}xK9(c$1c}b1PPOHVAQ+~pAU@6f;2Z*HJfNz;7%kH1CY}{JkfQaisU1pdX`_!7C;*rzlX?w95?{DvqtCF2^?`M-%_tiD#W0fP)rB`-UP0@z7c4acF9}&n%0i$ZctQ&=DFLm}DNDZmvPEDtRSDL|K%nO&!@>RJv&~I@5D8BpT2Dlqj`IksggMQ^3_FH6rodrdKP^!WM8FHPhiS5gR68XD6_Y$@COl}IcBG^RFt+*SG3Fv|DpHVuG8*R$44dwZG4VI9KZk?}C>BIuFs$je23Kaj8-rHBQFay*2M_~a5hN6x67ic57P4z_i-4%Msb0Zq@EA&lrai+eN~Gd=(wr<dkA#UTuE8fO$Llew1=kD{a0SN&iP#&lIaSdB_vzYIAAEdPx^T@|;}RPH{0#3NzbGIOc@ZZ^-F8U#4PFP6;5p94k8j`o`K(s7Ex1OhB^5jXZ3O?Se%SzI1T7eVn5#9qsR>sAC%z6EfH82;kj(3~W=|jw(7XH|9Qq;`M<>FS;<h5-=asF#ccNb{hF2V4O4Z>NY*SpAxc$BNiPzn6_9B%OaZq--x3KmkMuM>GuHywf94jY)pdN6W*>1*lGg((D)yeey@Jp<t{fky2B!j023GoGif(!r&PQxn@WCpT%j)w|hQl~<q%r2-@DTYd704&ODgygVN!o|dOp)zwEaRhq<R8u0~4ju0y44uZ21WOlJOc4A|FGNWR&^x%Dykt5rwNb=Wu!dQTB@%SqRl4af9;LNt^qU0809WhA!(M+076`kZW<kJhP^lA4vKKF30&s{EOh|;*n7G#OC|LkZEcBI#MMzR8cweeX(sd50i)$W>q&3q-+hw4SX02SShC4PKRVzY*TGLM9Rihe89^fy&a6ysce_#)zm#7v=k+a60g@V$TpK4W05LYo`d5trPqOAO;ziHMy#R5cC<D^_NuLk&`>f~kuu~tEUAcY0k(2P|f{6`nW@Lu^sq;d@}(mnu0*hj&V#=fX#5|4BA{oURBU8!#{jz$T$nN{0?DdV!TMOz35)lDfp3``q9iZ7H{-R89f-0vMoqrNa+nCN#&lnKOF<~6njVr7JHpIU0(teJ4ZflxB(9Sh@`@H%sqgn>ha`p4NcoaMekse+u8kR1)j72&p|b^|*^K-`xp;`9m#Fw1>qHQWw}ks**j8qmqId)=5=jhIl9h(9zL1P@F1`Yu;8iVH}9id4Q_5DV(pIW%HgXrl_C(e;?ZQ8UUi7*``+Q&DFz$q=xdY`gi25BIY=t+Yt0+~3A6u}wCV!Ygu%>57s>x5{b(O--@cXd!E-DXHG6YJk-<$;p|cWBn*fsIJTy+QCaSM^$SwK#@zi7{KEY6|(0gERBt9Q859GBX<HgVMf%1rAd5yaZsnCnRQe9&=9qf2o8sGo^LAoKO%g^DGl)L;BL~k>4IoZ$jvH#R+`{7X&$*FRGkmqG2pM5{TL~^Z#5MZUwt4J!G~j5AgB_jPXGeJsW~k$ojQ!EM3CXYym^q6cv;wrobeTXJ60kCo7_#vvS~|-logbx6-!6!5!jX8O|dY!D3)ylC|4ZRsd|PrAU`*p=MSYUD`P5)k=`T%+ZC)Pu7KU-fG~-&cVdz<)@k2>TH^%{gYzjx>D}s0jw%2<lvj>%c=`I0yrPqpKVe%-MI|RB)N{>96%!K#g$P`FWm+p=UX$hcl+%^TluWPBA)OhSYTWzxJj6i-b0Cnhco*GHt_JM_jcNIM5NkESg5^}qo_-JOu{lMIU=_j9{wYc}En^*{qtSjhW>xLOhtQ5FluLG~U{Q>4H^@^xk(ylCyxWaBUIgbGW(Ahm67ay+JpU>knxd{Q%{!gn?v&stB;rO9mFL@wLn@m1c{2fB;V6wQ<#1M6vF*HEbjMj@u8@i~z4{vq<zOv~nBq6B6XOtdv10@{D@wc1bC8X@eCYez(3jIA1RNJMPt_9TF`A}QXH*`JMHkA`+iq4!$D{{%H-(+~K*-|FYKWu+$MT#Zm66#y7+$yfJU8S>GoxNe7O<5E8R18D7$nIXg+;u1`+YE-)b%R`?OYs!CGmW`Fn6Z0Lho`#iLh-wNRWOO$qsPOOG*e{N){qJ=0J5;uourcZWtAjbHa2Kq1lr-_uN6AsOi9JgUIiw00vqPeyq<{y`(?UcC0k^nBE08x-w{{M4Mi(&EPKU=f13j!zP#vg`$c54LDlfthV9a&I*bD??j!;Y2ZCby-F2JamA?4nIWcyoTR+qF3Zh{N^^EZKi2qH7|v#C6*~k$m2#m&9MO^C(@1NHNClA`QA=IsnSeWL^$J}r+9MXB%5D~oD3~&SZWDx)|9oT2#c(wSO_7tf?&1u~OT#N56Pul9jwlL+tyq@dPH?i?kzr|F)`FZNu&bc7)VPnz%)$w!WzhiQs-aT0)P*P#!`HXL=I~2OD&YvI6(RIvKOA)Ia@`5;)mU2|((=NXUhY#jOd3d^#;;@TDXAY{x96eRR%b>;Z%Ek%kHRNgKg3#DabrmijBy{GvzUSLB%MI3(h1M7+3`N{@>L}e%O>DsFu~Zy69`>$juOY?P*}8-S^80otPE^A1z+mnW2XtPWyuV|OCogb>cmUCW}G4j%uCjsQ)q71DRU>NG@U*_ecBtzTREHz(Li*v02=_ZBIoYh?2=F;9L4EzFq*TFU`v4|<0*u%9S>T%Z4@9_d^?7$aL}%v(Ij|gwx0l=k>KIv51C{3O(i(iP=?()C-DV0UnTS7rEC^zwHY>FC*C8B;^C|6`C_3Bq{0ueQRfIE6Ryw+v&T;HqG?`>g)`A#je>{Ibk*!`L0}Qo6+Z=g0kg=7yc!aj9p4dQTdS%dk#^*T#5Gi-Bwj17Yd;Zg0vZkTpjkbK@CNVL)go0=BF^y)jKQ0;s;u4gyl=5MCgV)01EZ5;oo<$L=h5QqIbQUhptsTVvoZ*bp;LdPK>D{?V41_r$PXz4Yepg)Fc)DdDUZgj^n0xy*{7Xa53f{vITVv-K{Ztk$A^O<ewtH}NC9MG=A=G~iiH!7nyc=vTAGa&MI~USc@BGQwLwPA7)&5T<pe(|GoxwOLsh&b+q#<s$w7_=KhG@Q3&_5v(HZkdW6qkfUr75Ot~DEeSZm1F;To6AVMO>-n+7AI28`IXXe!qap_R9$yl5<R0aO3VczMd%h(+?8yivhDJpI=ymE$IvifzTK;ZzS$n+8@iJ5G7kgEMjv>dQKXwMVI1hB96Ymvg8Fc_h$Rx@5?oV1>!Uq?)df%zkGyMOYe%S{|aonoPV)XD6yQ65W(-IJSPblni$P)OHfDF#vRL0dI}$WVC3%+?;z!sn*5}qL?oU%4(#29qoO!7`C8nQkZ9mUZv$@wc&Q!1rmw^PP4|t-Hn9CyIcXJP}J$j6ZF<msBJQ~0HA`eX2=dw6@*nT;;0l2RUotLCe)V~3c$vb_BgCI$sNp9X&g2R>9)aA715&VD&pa8Dk>JFD;rDNgA?9+?>T*5AmqZ26Kpxqrz&?k+<dA59L(8>Kn6b54PlWf6-mT1rBrNl^wwM_E-Mqi1bJ*;B13JP&#WMJkVe@6>!B4gs4rRoZU{6Kx(_^lzWe@r!0qvx@+`t?mwz&$cn0n;AB>@;G_=_9`1i}XywTJBs#{;9K}Q0@$QhANM5;x8GYgODcjUfdYWT_eahIAU`tfi%J{AK_5TYHIt>iwKBAinMkPt(pph4+(Au;t2S*eyrl%%WT`ZPS9laUf?Bpts^FjBt3E`0<b#s~sXLm0-*Lwa@v%*76!(q^_s1j_tk3yBG)J5(7Z4{%beqY7M_l5Iv8zk+^j24vKjQ$}8{U1$UVy`t{nZVIksHyWzJV~!Z8hc-Q$!qUQDewuk0vgsBe!aQIp+d-<vpum)Bt?(?Q#uu)VZ-kMLy|OkCg7yW8h$@bixtCfa;KXs5?1%98+S@nL4s*7KE&D?y_Rqg_h+?RKR|lrbxRG#urlFRI$A`z^O2|4oHifH;;i|wgc@~=ro|+lFI$B9HUC;`B1sWIZGel)rja-CxD8GjM+1FTIG_x;H19^af2n{nOlW|*kiCXU27yYN*5%@G|_mN*0G1$Q%OkF66kgP`-7;do*tf(!CeGuu*miYA19#F?nrUbk9uIor78Pp8q-AbAam;&)s0tQkwij<VFGK`3`I(_|2g9oi-x}_wPPfZ*9qSOxUlW-BVkyWS>@&lLQUQJFtE@hcuFNnmYBcxlT0}RjD(WKXGA@&9`F-SBt-B@FML7NN#fF)iaQPPZw-O`Wme!-?h0M4-6QSuhrodP~Da;m6i%*c?ySVvdW753d&!x}1uNxWMQNW|7`7t-7y!Z5|ku7a|SP5kSW8Z*FOp(TTz{A9XoW1~X7!ut#^3U-LSeTs0$bE$-0(8f-CU8#h(Ib;MiYKE4J@ye`D<-8OPYk^sg>jPf9Rxc?!CeUP<o^w-HLZL_qnvTg%(#&3Q$Uywf8BYYX`GbD*s@;vv9_r%7EgfEcSe9X>g=_FNG$ra)YE@ehSyfwEjTQvo{5v<ss$&02osUjnUoT=J*Dw!Vt)S78tC%li!xS`HbRe&us6?vF?^)E#%@G1|yG6AEKq6dHwBI~5A5dKD6$Y98o}jNH6!wZm2n?4ef{$tqARs_PQl6)o8Lm({X@cK)Y#>{|x9Hvz@<IDV7hu-jQ}GxV1!HZ8u3LpL(NJrRNNBYrgN|8&C#Ymdx5QJJe-f&h4aO=IA}O0Qc^}Y@oY~vvz#vP)k1S5BSI}tXquljbO0&CNSn7w85Ja_<W<)eP@W9-tnUrfF_mugwF<}LW$T*2A+NJiI^w_>2sm5~>=+y-0BcavIY;R`{4-eFP@2s3}#^@!zYFC1!%S|b*3&GtJG;3(KVB?TyR1>bL^#BCR0c(H)kA!JgB0hBrl&jeDROnB+wNelAK}i@~9yWjlox3|1((yS=*rJ$^G*VX4oi80s$V*coBe#NscF$7qbwRRXxTYT<E^4-mxwgXF_>_)RY$vCFgRBP2v{y>Pcm-2K@I<DRq1QAb$_sqYlqO}DgDJqV$fUw_T-KE*8{x(G9jn@dhKkrOl}?=P#O|gA*t+Ln76pSpSa0bG<rcQoh=(ueX2kGqMh#!}v*CaQ^`{Fuv0BziO-`dLAv|`%MM_-5ZLLYJWQbbrabk+BmF2&gLE9o>c|k)E!s~0kx$#2dZK_1)PC_Vo^Y(io{<u-0BKH<uCOKJ>m}Pavmeb5x0|$EbsjD<*F{yZ^O70DnJTlhIP0_CC!77O`^=KDF=8Us9kjCXFT};IF(JB{haJY%$1O{TG|Jdrv7aCNelg*`U(aI<SC|ju3kRRewz&<7i^hTVuQ8H-F0+NkHDPO6~1v)>&zCeXpAO6|S#)K-eLJzmWO|B#K^ZnhMkFP&0`)D<~H!}G^K`*PO|F@2QQlsl*ywxz+K$(i9xyREqw=#7;Ie<NvzD^T*4D6x0F9w2<M$HeKV$(5nALoH)@3g%v$TSb6i;W%OR@K9zWT(>Vl6n(!_m`x_h~o|=!nq1Xp^yyVWvowJmXpg0x@ZXQ0#Ae*P8xC*wPjpk?4c&ymB9&KV{ir6zndZd<;<Z<*AA8741;7eRs;K~)>C`}v#4Bkd%!DLUYk{8aIC6}a@6_*dD31`4nNCwP?Gtqi{WAJMGs=yg$b1U92WHa-B!z7FCQkIuqgIx?0E=~QSBTZ*f;Q~X_7hnolK_f>sc;S&DTvGYQ-KG7}?u(YE^+cCf+P$kv(mRGTo@TuVq%sN(<$&NXtkzt!8&R*GZtKoUMwJt`O_&ZBg1I&SWTo^0V|kYPS9r08Na1RP1DBz)Vrlqscsa81A?87)CkmiitDE7vn@6B6}{qYY=4FJ-S8r1{yJxJmpiXrySMdOhl(7YXH@P_9>-Z^f~S7&c)!oa#q9s5`lE?^%gfM<KnePz(u#26y&q;UYZCO5~oW4()U?qWJl~->J?wS*_}GQ!3|4OHTR9_rlF0b{rqjA6FU>UcYDMm8yhbo1JzZgg#L9RVZv0J2<|{ph7P5Y9aH2J7%j4XETy8J#IdV1F_a6Hx4o{Db(m~TQE*O_oWskS6h3o~k)c+@*brvtaNW9bQ$8L)5A^=-!#t@PsYp)v5?Bt5Sye&Om}rfIj}BA)I6cW<`MS~DcH1?M2T(?e7g}pw7f&n<Eto}KA(D)R+F;p}G{6`lwJ35S5u!v~vxWW0+(`I8NszSMR^T}-K`1itIkjv8F9@I*0Pk(JqoljlBt$S<x{<US#6~;7D;YqKWHcirLoW%lRBT&83Di<QH9x4*<H(0@AW*Y)DMO3`Zl|{7WT-1RUZtc;?1Jh-b=uT+puwcmH99Bj*VJLCE{R<mW+YB(6W;G;>j{()_OVe9QPO=}8ODoG6KaNB^w3FNr<{)3#FO@uj%BljND2KVyFNHE@dQzFcN`Zy|K5^m623k|0yO}9nS`tB2Srmz+MFvwqEoIysn-`*v57Vgl{>n$5?-~@;_BI2!zE>7TE)@HxfP0<cBzk$R52)hQ!go76is290?KLU^5L@Yw1EzCHV-S4aq3J6?tqmc1bRNuNGXMX*n*Jrrb*p1^<-wBS6Zlt0{N;Yo`QM($f4IU95Mz@7)C6e8|=XSd~43P+r>)X>qgl>Z}yQE15uP+4-DWFvClo}ZU@kv!$&0uEL(w;O%DMTz7?q8>pVpv)}Rc)O3|3(Un~AGm=u!fb`)bax{DcL@Tk&uC@NG_0yMVwv*ew|u_jts_4Ml0vp7QhzYHlAZHC&T)r!tQy;iruZMg_|JHPyl38640|8d4nvkuK-CTcNOgPPqen%O)3#+5~M)kbtk(#kpe#c3WVlz7mjyzmK1)L4reGuG1N+EH1=1~-YQWV2!+(ceRAn>KXObG7S!Hzpy}pb4orc72XeplSl%l6`}6u())@)PEXNEwNfYxop3^qdt0g*}286ypAF1Zl($>=ud1SW>mGNfCp3XvhPsVwLrARy+pO#9*{J$l|nRZy}rB{9&uNI%*b>IM^^JdS1@j-_zC8jU#Reg0*%?_+U!x12Dj$9)5PY|?FjC88(O3K-$F+tJAN;OS&({F?NhRXX9vNlUwrUBV5XDouL#g60vplEtndsN$4V!CbxCbpPjJ*TqL^HhO-;3nFz^=ZC8%pDn=M0=*`d&LERk>!FmcUuycVgYh{rlC&lBjam}2tE@|Xw;4HPn|NqUvN+h!85_kW`8+{W<O=G6M#3_*54GJJWZpO-*Nk<htpFfJ=)SGAZO=in04MhA=<_Ql{mSr@h+Y(^(($ncJ*G%?c7+UmzxlV)-XG8jIocw+qW)WQb736Xuxv1*lWCgd4kMvXx0iWo!CM6WH$dbP?Bp>4!)za_J8OIp}w+m7QS;$S!5-dizLMTK6KivV)GC`kZ@W5_Cb82b~nSZ{XtGZ+^<5kJ^ay+n)^8jdS&`cr5>8Q{0wRLhHaR+~>Mw>Bk!<L*2L&|v0Sr5ilt?CqVnY#;!Q#}jn0#qL%onFwS}e&5ErJN6DvimWQTf1j=)oh5_=+&b-B&>|}<Y#yy3YuSz1=-dJ1UG}CamxBjdc&w{dPDv#ReT>VKhk|mS&L?XcAp&}78W~VZBCI`6y>*Rzn)~|zlYiq9$yDYi0h3t$A#d2S!lRg7y)28EZ@!lDM7yVh#ShywXkmuZRI@noU}Fy$<`Y&X64j|O<Y`kB&PZ~E;A$jeFSK_1^7V(NbabhruTXNhw@QH|SIpoeSJcY=;u^c;kTD6R;G|S6wofIdOjE$RDpIv2<F1sy8NQu%V3E1aHff$+=CEi<gLDjInpbE`JqBH0R;eBCB7vfTING;f6XLx{s`*(>*|q?d#p#1yt3zGBeK>a|@wWAXo>cp$m4hB2$?<G6WvJ*QtWZ$%ynqJC+>=U(8a+7J3$-n-ZHOduwI|@Fz8Lw7w;A09_9CP{ooT2aLQ!2_UFnfH1F=dt5>N{3G$7KLFk$If<d7)^!i*S-(o!A?2X7{DlCp68g#q&vTL_t~qhvpEN>nQ|BhXE>0$iN0SPfszbmaQO7Ezor-j~18N{MERnzoAI5jHY}*a=9b4`idH@g@P+o(~hBD712Ego@Fed|2w{LL{ghxs#h3aG%O;^Q01%S;SZqwn3{<ZkNX+$NkP#WY;~a%OHnv`*!8J3SDUhFc5;@v1<&?YgawIt9si6KZK&Cs>ee_+WKYOtwCh{(vXEmC(ce-R$*at1H>On#aww~h09S^*d_s`)MBcO5o$3i02G!%opyQV2URrXOI0FqJBcDP^0sDBZj_gj*imUnwLmB=OZj#@c&##C>CM1Y1C(`DL(NP`q*^Y)8xVjg1ThEpM0|mrgh3?Onq2N$()jb<i|K}#RnT`m-p4nqV00U$)9^e`|I9<CRDZbwuNFk-hG*uhw7+n-mpU<M*AHNUf{{c~@|uzrD}V!snZ}}zCd5Fs^FNw`s3qW0lyx#Jgke*F&Q#Ihvb4nb)+C0(>RSnXd!fd|Hh)86(~KD4Z08AlDOq?2Lt4~#HnF*gVzJeEBucHAQ=4Jt)E9-O`Wo&VgUK?dKJVo?8;Xg5fFiwa<yQl$>b5Vo+nmA0%qYUTK(WzY(5Av*VdeGWjF#Uu;KD**GRQfBc`>8qqrNO&%p#YtW`9&AR#XI~6K1rQ<H0*?WN)F+*3cB-GODCi-!9SCcw7nY?TUa_V>ghU4Sb_+*E4dKRwc6<d&4~k3}z6e!wolu0{9|rlxJrI7>G4pFb`~Ys!<}{UP14f(c9ajRN(s-Lp!dx6`^TdsAR)xSPvR*Si~LPP`>U>@%Yb#cMXmh5x=k3#L*p)`w}&77-*+`@fzNy7z@AjklNI)LQEXr5;_;g5RSN4K<GlcWv1XqY%5?j=_FTqd<}^AYAx$l>lRHs!ANDepe@bOfh@kFKV)a63N?XO7ta3~$v>_{3Cp$d%8*9EiuI*mXJc`qXxACx1{_c$*(aMwS(S=D%ZSob$+!C|z%m;4Yw)&p_EV)hUS5^=YGP3y6OH0s(#R2Qm$6st@VM-g*9DMuHG$E>6W8JK$hkYU<K6!J@{D~Y0Xz*iYLw!!?#P_CRzLzSBVx|7A{Cw&z|Ra|Rm6`?F3$N_`94U<{J{<F6(F&FAcT_Rv8Woe_qKx&#jWpw>}(PSrcWM4`_5ZeK(=PHW-!+un^Q)p5g-2#SR6z&vPzU#4nXn7W@($z3M-)&)+T38QS^&-JIhZ^gxKdIPlsTpa`M=kEh2#<RGw-z*?U&V$l*(?XOQN^siOtVskk-Fnc~%DBaOZdQY7F3fqCRRRLDc>*e}90B=c)^AELl!a=x!gUNu|j9>hj3wF>4cof1_v>_rCPB3C3haN?VQMzMkG@sO3^3~<Sjh!jDWZIEwCp1Cpa8^F|w>f1mGDMOJn=;q-+8rZxd0Rh|k(%hfGq!=zx6ZNxG%F?z>8K8y1$fn)}={lzU$Xa6;Qah{?M_%Oyi&TxR=XJyD6dr)G8<+oaZH7xVh_x%rll8q&IBIo5Qb|fzBcjp>!`^tJVN<UMVeRsl29Zscmf0zs3(@ymWZ2B(iYG@eTt!dIDk`1wF!sq06r+bG?b{+{u!yRA{(B}~T1vQ4#~!EH+?;wPz(!IPHszeU(F%2(Xs6&MlHvwh4o9@i8igZUW0Z-J;q8K^R!F|PZGnwogipzSCwl(4{Mf?Es`L-zkg%RoGc59P1H<{_W|rMdS-@8SC$?@a2R-+lE=gp~k@Y}Gd6)^N_6zG?b3B08C7fpAPjz~gCU{C7(tTkR=DHnGNsi|P>tsMP%mA?9&W3I4=&cI;s!|J+lRWh?AP=fLYck4Z3b5GpY@dCBS|#8ui0z1)P59Ex+f<sFVp!I|m5)?>*QyuUYX0ucYa^;*firUvM8sO16j}9UP!U*;uC31ZvJ&?D5zO9|xNL;|W~NHDB@o_KR|XUWQ6|SqOB3_+Uxu$D@w<A37IG>FOk8h5Ip?ognlZ3GU<78dzhgOZ2nIR<91gkEYyk_QOPqb+&G7?M`=c-1<0u9z1te`>)m0;;_e`iIOWsty?C90A_$01PrT5G8R~L8z;6fe;r+fmmKGqAx%WcB2S-T_kN|glEvWPIz&WVRd>Z!xw8ZULRu$+yQ28eMhI5rKuXX#Ey=OWH!jFIA=i+^MBF|G$%mVsJ<I107|>n|vV;Wtj>E0SAhg0Hpdd?;9b_Uu^<p|?cz_0#_XGh#DG')))
_PROXY=make_agent({0:_DEMO})
def recent_style_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
recent_style_proxy.telemetry=_PROXY.chassis.diagnostics
agent=recent_style_proxy
