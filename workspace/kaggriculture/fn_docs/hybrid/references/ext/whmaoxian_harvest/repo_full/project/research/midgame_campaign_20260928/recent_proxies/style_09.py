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
_DEMO=json.loads(zlib.decompress(base64.b85decode('c-rlKO^;;PvD|-|H5YR~tIE3(*-s=Mr6Fc0H)KH&9^hvfFrF8(cZUDFDR%d*TQ?&kBlDc<ZVFzpd8fL%>U`wMlMxy5m;dwOzx~_a|Ks2P{^39U<-<>(zJC4i*Ka=j_ka7J|Mh?U^5B;r|Ks2O{y+ZxfB*9HUq1ZqPk;W~PhUQN_or`v{_xF*$L}9L{qo=GuiyOT!}mXYdHA6I@Q=6o`tb1G;XVHN`SVZCzt1m^KmGBCKYaS}mw)*B{lmjgAHEs>`q%&a&CM71;oE=x(@*;sT))g;K0H2r{rSVw-}>_N_rLzMJp#Y^@~?IjZa?1e^6|{z%)u8M$as8x`0>ZXqune2@bKg3KR&+!`UCramqzY)fBNCa@Ba470{Hn)zs}Qc*q&F#?uUm@FQaz*#2qR4aqSPv7x?z`<MU%MLbs3HUp}syA3uHj;4PYMVO;<4_3J18P2Ee;VBk@^zSqAzeEIo@AAk5S4`1jnL_?x&BrpK%-}sm~lV^r$v@<=D0olLb^KY3k@~49h?qSScqRMWdj=O3%JlhZ3ib2t4`%bA(?v0STQou|&?*<m=@s|^U=6N52#dM9>UqAop`KPDg1J{uM)%=-umLJ=K;8&tWm<c`LnA(2W4a3W(+UBOVtp;-HfE5-m{_DrL+rU1#zWQJOG2-!;(6_trZ88(~$Dg<La9qAO|0FKxZ$JHG1lZRd$?^ni`S6J!KmGj6Hn@%7&yV;V9X~7kh{4#BGe5au=sLUpL`FVdUXwn!+2!!Z>zm=jazAR~%JA2}GVIMWLf6;zC-UXd!KZ#tB@o%@dHq<|eC_u0b^0`o>jRwtPanP0=POU%)7tDkdC%W6xU*e9)^;;_tI4|#$h(`ohp#`s@!Z{n<KyPvKIl_CzWXG;{AoIg=wQrD-q0&-nuwK{v&4sZj()q(u*Jjc0Bn!0Ij4{jBtFHrpMU)E;oG18w#(YxA{6)|TV-iGxV$G$^1Z(;TrR=Uk-2pUw|x79{qX()k4j33^KiF85BbOB6?JaMe=eldV{ZDLe<!)q;7yYqYdz1FDlz39@UpYeMs&XZF+hdWlv_^hzH8Qb?bf{%_TzV7p5GDVbp9~x-*Czn(Izs*lQ^*M3d!7VwruAbhsE!#1|#;Xex)b)OUYGXPlr#(I?=HNwErPHBFC?FT#^SwWdFyvBU##tmA}qXDkm(Y&ghjR7qvR7Q@~Gc4CPjL{icTsYE(*1)>QK)*W~^wmYeP3fCnK+=-|o-3#0oFGsfq>_I=Z3{85HJ;^BHeZl2%yA14h=cH=Z?DZwz_xC-BHEW}Zp>t9#IcB~$={)VGv*4IvAi;0)3aBqxm)or_vKCgh}#0R;glq!WGR2wk3>Egh;oom~nx;<$ck|mQOFP-oebADgT4Yw(Slt`z(+@fc`U>3HIcSH&rFJ`k^{bg5(a2AuH_)whR{~+FOQlV*)@KJJ2@ydb#p39&pOP^1y6bfzT+$Zj}eNeky!SyFdWYiRQ=~5<>l8C#1Ku|xpPB1#;44!`Xk617A)hK2P$e#fEo--tlDtY{}a4Q9cm3B-|i)<475?(=Dj?uZE944!ZY}TX#i*iL`)uQzLZIrFwfByXSK?+k*>C^(|$J(1*(-=Dd&bhB^w`5c^_2C`i>v;^h?c>2u;$Oc5MConE)<%Nuig>NISh$KE$nWh79kOW$VpgYUc=d0@?hMy5Iau-PB)$GuLV2p)X3j%E?tqim>l@J<`{9dy|LMzr_RrSqO;p-ZkWl&UXE#3q7hP$2m$3F<4-ps=K_-9w9GPlc;se<e(T>V>ZtgcQ6zn%FmMbGDb9rP}{%~0KgMgM}W?T{<<oV8N7}MXr>@9$KU4Pm>^!+a{pFFPeO<1xY)>2@eC%54v>pc1RmS}5z=(7uxeku&}7%vA~tveKkI3wfE18U0^HoVvojz4c=2Qh$>ugCj-3eq%m_@UEBc=P(g*u((oUth?=n&r~S-Kz!(v_q_XOsU#;y|#e9KQAt1IP_Z8XsLjz&-v`vpTB&1{N2NsFMn>N6(%m^ohuRQj$DgGg+wP_K>o2I;5sNbNh;_e0mG|prSPCsYLc%*1Oiw1hy&wq#MY2Gr9r1TgVW9>6g*E(35WPvQrif~_L5p(ern?-Ib%O&I1_p9PU?9$oY$qf<*{&U$EndE@mEKQo>A!y%(D`_>iF%pimP0f?&Xr!qsou^WzXW5^}E!I*_gI~mD=D|5<HSQ3d5E_u!NpspKR+4X@+V*DvH-P-1eefS_~fb&V%scdm?GpRBC8Dw1;dZ;7SrOi&Vz_r*3U8Po0ZF9)*f+gkQ29XK}k_s)JZboH7@gyaIq0D|l@hM2i%~I8O&FH#)ym*mmnO*fn4g2w&+UBlG%Z@v0hP^ESIE<bwH};ZKywxS$g0l;MwEj5m{;xI%-abt+wUr$YX%e1E2hz#0|fI^H>A^SLKck7f<fi4R}}N!4S&|NM|5sdK17<{X!(EshM*QM7!M<#d<|0zIi{hfl5HODOl)BE1WChNBRL9529D;*y<R&<Bi8!uY;+YQ!K!U8l+xh18Tx<7?$Bj=!nWenaQ5-()-Ys^$C1aSfJh0WvfRhlhZuC1oyh0skCtlhYlTg*0|_R{KhcAUVV2kHIixHt>7I1JW5Au8lYJeUX7poKOrTI7(<WmuN@nGSIv1pIDb`=C(2`y-(4)w1t*rH)R@PIyJR_H8i`9nOZE%9OSj<r+q^qaI3<9sW#`SvFxn_E<hnifd}?~Zq00*YJxeHdRBw23F;mI)!Q~B2LiP?7u}FSAzD%ZQ7hwFZBcSAx-?RK>CA<q{vy}xkHx0jYwXzE{Jhq108map2*oAkMZ~z2DnNNzzN#@o5_Ax9Ziu0H#Z@I&a)LBwaFoO<sezjS5{QnkD9Bpw;eJBAQ#D%r)>9L86s#Is3L}_`s*(`}n-s6Ni&_)eK>*)B{Lrc+QD!h`G?a8W8fmF9-cg7c2U^}$4ca7bIg~V^Q+cEUx7p(VKJEf3z8I^V)507>M>NM){ZVt(_I2W|aTbgI`R!3{mSuHR(4&xSE7fYL?aMq7_H1$7bgmrGIsdVfxwbd-SEwmnvo!TskIxhilOf#!5ermDZ|c=Hkq0U4T4UG01a0orOTpz;F&kSz1-%`27qkh=31uCEu^-?w-U;wg+B1%M|G6Sh*@e=hX}(rKm`aY}Kk`@KrAiK>iAoD{Lv30*(VJ7(z$G*IqfVnjU4lAVa}a24g%}c(D`2u{?VB^CGg7j4=rBJXVV)Glb^hbYV_;EA#zFYjA&}Nds%uS$2%!a)>0NYKG!1gSIld_=i=5M<NkNT~Y4);(Cl{wHT>=qWQ2pcJUi3z#`IwAHL<Ji$lw3>Ys`XtaUF(SKr)vbXKiWmk{8(4T&9){DeM-G!2?U5s+f%=*`YIN97;GkhFK0awVq`#2=T#EKI}D6^WuIHLhrJ=P5eCz^Eilll0@hb`c9I53-KojmKwAVxhi3mGVr2-Yba^t>DcwZbWwqyRw<`CPa>Y@7@tk9_r&P4Vooc03u2LmLGW5M|*`<&~S2VDFA=<ZDJKZ8)LDR<j;ceDN3JK;V1Vw(h^5rjYwK1B$eE60BX(k@v(zcriD7Li=W8Loz*0wu<qx&{ggg<nsw9gR()%`d8T|a;RaTmIO{Pf4~K8TgB8va^yK?x|7EyeDA7S9|3d2LakM9*0orEt&b(yId)Jw$inI7UT{qT6-nwPZ$J#i{jos$Xc_U;G#qs3)aB9oDV46rT15S7-<{tlv(Ogj_Akl%jELHR0k-k?=){B8b%nLL{FAc%&xO2{EgPCtM^E)@9VjTn)t;z3uXbx_`h76*b4DHsQM<7|d_xQg7s;(qP+Y9Z1h8c;p4e7N;-q`O(AgfA3@D83`VjzZ4YD3G!vNgLr4Vvg?m&bxL7}^}?H&w;$jEj(E%<|Mj&aANc1#5N>Z<O$SOu%&Oja)*r?`W8J1#g!kX_T<8utlgn#G?4J5R<_FE1-TPV%a7-4sT>Kn?rD{5^lcg`ywMtwcY;oE$C!CSp#oXNPzb>`#tjSo|CUmPtaiX$PpR&<`DP;r6A~34pOd~<z*KwYrhDXPgFn8M>Mf>e*u&xl&865!Dwpqm>x@IIE`=j3?LFqKp0q0dEEM=^*hg5$@$Ty@B*qyqXNx>4;T{LOUq{dLIXU)MK0kAkwu;nV$RPr%t0-5tGa|Db;uQCuqfhU7ydq9JOxKzL%KkIT;9d$IB)XI^6X>B!4I7nC`#7(yXt<V%V@mb>>$pKYct5ge%N&b2)2uzi5Iml&A&#1vN+YpnGxK4SI*!rp+xhs0jx8~JLCq}BqQtAzQ*L8)HzRU+kTNg~G;2F&PYVysg8qr-=wrlU@CD-$VlrAO%Jj!*Vl#^U$$yFhw82>eU=(_6;so3BwF_d~79ASFcSffFSt-zuZwcR`Jy(-srHMIoU%;L`XQJIx^7h{~MN0*cA2f=aU(&@^-aaG${(BMsiykV<tAAg~-kLyLr+{d{=q{9IKDKod%jyjG*cL9qwxJDRG0c4LF4LFh|4(gQPX~-+Gs958U6-C4CHOkZCQDK+X-5ZAPZf(viqxDz<!K%`f-OFZZYYsz!z`<D3dKPeG9RsyV4ENT|mMFt=E-eB3>VV1qg;R$4yJh{v9i+6~mK>rH-+Hbi)rk;}>a4WFD5g#eLsa9nQ=uu1aVJn%f((3KP8snEkWg$3E!_!Nao!oFj?NL{<bkdC*Y6)5ergskH0_$;S{Z>^BLlOfPQ<jQx%cH6)VKW()C+?zlZ=Vty;ZH_4fQuo$yCqrWe<QK%u&72+X=P@ILHJ%g#A_-?a;3#9P*6h3R~sY>k0L_(lZB`ah_;nQhZ&I!Bv}orhNN;rc5v=z_NXCVc0`IA)BeeyyQ~2G@qLa#NhBkOAKg393FKsY3`vPvL;GwcHP)u%ez!l*DhvR<IinePYa7bkhpA+O+KZy;zF$tIdAAacWj9Q{j?ULLwH+5d8(#*QUO9Vty|j)C#7boMz2)EZ-e#&ax`+kR#nM1|NR88K$o?MdX~@_#44+udNqgU{oWV(8Smca*ACuHK?MusFsZYMLp)RIfL$7Of<dVOBxnGA)k;_0WC~lVTiQ;K@talXZH#sP`l4a`OTr(1`0-!Eo4_noqmG09^u{IK_n}1*QwMmcq}ujKXoDgX@-zwq8HQ@@K26|b^OutH0~ZfloQ@7UW>cv*?w*tUy0zKU<Eb6824kY+doD@;IfHtYlVK|wydTF|!bN<_Xb22z(xS!_pNntlA=m(-t1CZqZe7+gO!G9}i|PFL>Z;H4BLxyzj!p=WF!@R3Pj;w$A{}w9c<i2C-q$*rSI&|O=xoNFM}$iT&hr(tzKKjIIBh5#%Rwa4Q>1Ljb$?FzZUX`cT2|=QiCS*vfacYx>B;?7rIxU=HJK6Um29a<U>*JL{ilDTop|gl(m3N{_eZMxR)a;u1T{=H*ADU~XefYcBl<^rV8iWR5&awlj4}q#OQNDvex+v(V8Cew0>Oi8lzx2?U%yHVjvqk1Q_GtVjcGyudBH<I6^^@%vJL960l7l%WkLRsVaes4I9L2e3rk#^oH=c8K8hy{6#<=5S|*n2tLWld8oZ$>n~;|ul!S>{kkAqjFiqKJz7@vfLgh=5@>UAlz`YTjY4#V77lb^g<kaDN_yu_Hm=1N}ri_63qH@v3ay4iYYH|U2m~qRD#05BM-Sr;DF8QF%uaPDKR$UT+N-5BPM9K9rOa%kf=m^5^jxjUXk~#fqAl`J~>{E9dh@4>^1pDaOH7qRMZ@8IQ^Fp89Dp2wY6IHsjija?kC9Z#~<%1T5MECD{egid8kt4Ud50!LI1s$Kn1n0n+MNF)<gv52tJm%xc#d;7_j}bR`-s@73HM!+Mxt)nkAs@?0^`f*YAm8V3b*mt#7A8T!&=I0x(t9^jX1l|jAz_}i=B8gaBDztHNiow;J`WY4_aLur-ULxl`Phub%{h$eV-nQ6uAoeVm}P;Z%^($~Oq8<g{ivqcBxu0Ufs$N~S42D~a>KCq4(J!sXyO~%7DQgmQt^RMb*j#dSbjke`Q;O#Ysr;QL9%reK#mb7%)?F%mFhzESS<i1%6CJCDt;2`*A{Ns=Ee3LXvJ=edR_Y*3W~?H%VLhSpekKs5{!71EEHpPM9*@sGeRbUa;c%k1*-&wHFdrKpcK{6BDH9{bnQB2K%@N_<Y3%mx_YU2_MVAnsCN^;$-Q&rp(QsP=m6an7Y>4+0BnpabE>mK5wP`lQBHy>RpJIg7!={66;3s+g1n<9+cnm;{Dz?^;}}W}oQGk*k(5*o!^2eDQB~dlF)b@mR*uzu#6Wbkh}buc!6Xe}5XG#Nn^_Mty&f7JteA>+q1#SH7f5ssDu^njhaw1RYvOVRh6A8>s?3_%0j+$Vv1wgN+K8;zFKI(cuzISzK#Sy=HXv1}PW`Qc<@}|R<J2rJ36`BLcIAd!v$|F(Vhz%pV-r6@JM**fq;0_S{L(RcCmF>C6#Yc(Of)&rFKZhtfhUIl{hPn*Sw4&7j-;1w0J<v44H*1d`+jLmF&f$~w6p?b|F*;Sy0~v_ru`ALFKZaWrB~0J@E)m~Q%`%f>jI71WHBP2RnuH`fOD)+xXanz)VZbha(Ap-cfk@d@Hy%sO`_dbAu00JT0_p*B<<nrQdxYPS0_;><O^Fu@>*ysThm0CMD$r~xhMKo`y&-DE&!4u%en_bO#&|?@&uJqFH<=ZDrJJn2#xNr5!_-!l<7@6Kb*nLIJ>4c=u%R-kpbn^Asw`JGk{*OeRbOzEa;*OGZ)(BSLtJXvUgZZNL;y{QK_M<GF3KF9tMPAw9X+LnsDd}d*FHCgWL8gjoV8V6-~}=4~jg0+))>zBW?ezkOio65b@)|ixgsB3{58c?Ucy~_~5`xORM3i7p>#pNoDxfCIw|^LQ~seGGM66#vlsb1+!8y@)-lJ5tz|b_O!;8vV`|BpoG~(6EP)SEiO72qa6X{SA7oZh_~->O3%cYp9vu1H_jC^m%t2y$v2>RAZfmKB@BSCfCMs2-C^SXSgHi4vm&nnZd)2Aq}bPaBy6c;@nr=TwMzsx?|{_6R&u7_ezIh@UB=|d9vM354#HTO3BQje^2Oe4CPhK!_75)Fob6KyL<3i-mW6|2`(F=L73v7<%>;qNpH%AhXGAczQ$Wh}Qz-E?kU0}|p@0Wf?gs*gfCPw+7<Vedo19vIn6!gekb^Cukdt%;PZZ?{fhR8_5GMj>bgWbmrGSby$9#fTp8l9x34?;v1=lvQZ}QOxZ!~iFO_ttW4R?~9AS)~|q4>H0e$&lzhFjxc4NMMruwfL4Rc#f#q-!5Ap_M2;N_$lRI=Ov5RB|6$4bww`5y<Qu`NvAU8|GXG&JuMAmUt28^qbAfC4wr=FybvOgzQ6^-3kQ|dC&rg*h#nsIa6dEFeou6!G0#;$c!S2F|;5X`Ft7U-|L3TDtMe~=k9=o@SIv+kOOPmX%%XOAYRdSPeP&r#U(&oQ34Yf1aD=Bng0cg=Y|ac&cuvLhb_}ezrCEnVyUFI0bFaWdvkJWFTD5GxA&VRmV1CSxC+FoK}f=jKyMA8Uc`}jF>s^Oj)D`_4|U55x7CO1Y6qJ|X^GS-fNO69;o&z*dXcV#_!es4k0{MfY;kDtbwH8LyLhF*v%#I1(3zN)saPTrGSfiL5zR_o5u&9FFcivUN0wZE8|REZE^IZhy~tD(sAP>?;;U<GJCFoi6XnV9=o34?!4$BzSXk+$E#HSkSs3e*8T-eOo|6|hh<(h!=<V|^YuU<hB})AWTRzT0SZ0f6iaNCK&=%-6zh>@uqD?Gq0i(Kvy7ll$@4kq{lctI_twL&Ix+qG`DLm~W-yB4}v4eh%^eVq2J4*SE<FTPzCo)S;-SdtWAugO7#usf}$4wZngN*7Tm&+$k@u2zi>D{rkzcoKnt`VxJMy@c)m@O)X5zLqFgR{i+b9^NxUBQGHeE$082XAFiGqnW@XQsfiCZ{Fs^;of$1|OBNT^;FETHFjS$--W?;+(l9<}9?7Ysu(_%1QMup?C?1n9;dKarte$75|*EU0NuwJd_Xy9pJu5iowf<dIDJ;bRcpJ{^0(ZDvIqKV!|xI`p$sy^2B45UIFszv#{W8U{LD5!P!S;U{gVNXK!SNuX3L_)A(IB{G8F7<ho)a+79T*WdJQSNX5Ahi9@R>$`x=vS=&ZA1&O@@*9s13f1uj*H_4s3NxqEu(`b5QO*4+8WZf_C{pIt|M4ZPBJSvH2NRitzpk6}R24GFkllMFTi7RD~G;hvy9tNX1=VTvz^zW20f)4v6H0PC?NP_|=rN~W#DAFc3U=#(v*z&aTIqa|FV$<S?Uoxot=){+ad$sruMf)jr&WTgaz?|BJfbr+2Vax%T`6g7Xm8KGSqTvRU(CTAt31}aJ#q$C8$hl>!JtV7?Mg2Osi^F~gSqH8(twJf=$5DjQWMz9oj=%<Qc3AUR{hB)6jnyS8Sg4UiDZoV-t1Va-%EoTTKy6%oTGW*EJQ3y0htO@LVqNj{SKo(sg~)6ed%IVFTg_E^KI~sulh@EO(|mi0hc`=5m@z>C)8MP9O^Z9ptf|z?ncwu$qa~@pdyw_8M-9w{$<e0Qy3uKG6^VDC_V=_KrohO;V1ilVw9ry;b}N#}O<@Tkj}MNET)Vr4{WFo@g^<c*3$iL@F=1emwO6H_5t}o?z{OO((ULz@GD9h%iUh)xuB;E|YT;l?SI5q>ry;2WgAzH&Z3&YY?4=e2bjU@cN$aI0hNM%?j&)K47CRUyr@^8Yvc)LWO9}}?m#XhbLb2X&OV?Q5rwsF2>sks#cRU&7qP>@{s4&;Mol;GKLxJK398wvz1n^^NldLy;G-!;81|lX<RG`ZSfKo)1ScG`7E5#f^WsF=$0otWk(LvTU&6M<IlE94NE(RxuKOw*wwkU30N?_}TEl~zNIP@5xbE7pS9W#;Vt?>2dFP|QN_weP*pSjXjf|;?KLGPc!uyTzA&Yja*m9RzsG99~bYf~E=eK>z34ERfm7pK4!s!(!D3v5np1S0rNNip<TO=pU;v{Y{r^CsV<K{Q_A7dnL|5Vn$VekY-gV;wc&gq>TC$0VzN=C!z8RWDVHTXa-g5;Pzj0!IhjxlbjP1cSo0GgLMAcUq?&H1Uq>YfY&xLne5TWV8@2NQj}g6Cor)oa_aVM09xtK#Zg@H##CaNz!_p&_9R*j5Nl3SQkCl;|x@4?VXao#X7g?V@z&(Sr?fj6-!xu^8FhhLuq?X!Q(yaod~*Mk>0YLlp_70DNakymXzEDGJV(CG&iQB9$DSX<sK1_AjdQB&BhtH(o&@t`P>(KKLbv0Jk$fZeJo5jH>VUZFw%JtiN~4_2H4hQg*%rUFs27}H-ej<v(-|cI|EXatJgyAPC1jytHR)-iWk{90exJKV@-zm;^AwK{czBU4>i*QN!?%;Cv{b8oGu}1Xs~~atgW|L)oxfXqIx6EB~<-K>;HFnnO$<hUDzRBuPu}5x$w}JfM>Tq(2ov+HKbd#D_VIW#WLoJm)TXa`xs>ZP`0LAxF;qkAhl0%JwiivwJ=sQeI>fuLoL@Go79#p$$+XV-CjuBxF0p<!KHS~V$MCoB7uk%Q|2kf_|P~7TqQ(u4G7nJLO*ONVpY1g=h#$z$DKz(c{r*=<`e+JMIA=ul#0SxV&csi%F~z$+G^Jf>7XQ4oiJNFtIfD$iu5(qow+q>;>0rFhhZAb;haDTT20P2S$I5U&{gkpb&*a{+R{GKCYzS?6FJKVYK4}thhvPWBoOm=!@A8mopvvtLc?uUAt7zQ#MO1-4h&eVI-*U=M2%qftXI9}rsyI{Vo!;_&2;dAu^V>r#p_;@q78@tBr39K{IW~H+em>*N(N(ZLtYvlDkpy<ba2-K`l;@reDQR6GD^)uCShM|DpC6Ya@(&iur+S+QtSSbt9G6<40!*{H3gfq{&vIA63khd9y9`~mV(&~MRDpvlGIR9XU@~!_u~rbWJ<N(j_w9lMCx3X<56(}4~ExdZWkJn{Vr-G!l%*l)`H*h=)?nNLZdVT2zcF4X3BZnTcIcFsd63dP_2n0Ph`fuPyx}PzG1qp!5Dfl=PY&6&ElgJuy5<u68{hZ1O%D$2|J!5s)O%@>Fs`lPbxGz_XXtO%^F#pdwmd6POBWpW>I=8aOwC+S(I!bF)a$f?v6gB0}zC{t1^}+ks#tNLv#Lkd_Hqo*2)l8UcpKzY)=5(XPNfiNpI&SE<tF?<Nl>Ys%Z(=`Ano>W3e$ZltAsnrlZ$^cMqL(b8&8;M+50m9_H$!C5x{%>l{awHM{x^q!Jd5CvO;i>C9vY-k_P>U?Gb}0>k;AoWS4`$wlqer$+Np1rCOR2OZ9G6?#fuk;<U!xAvkk%>5vPVNMdebwKSV2vk6urPR=DQ}vppMQw=Z%reb$A{g>pF#$->8|+B)w%R12fuRu<vx8JCb7el-U!3d50@McEr0<orYi;@W8`imo-HdTdS9lwydKH9-E=wnHz4M}rsRoeUB_z!fnO%LiwG?xd!Zsb`j12$V2a-yoZB`1z4xk483UZk#rB=<bZO)jpr{-!(Cze4Rr_EN{ampcGiv%|awZ8tkRy9EseIa;e+D`iLejG>%bz$^)fUR)Fy<Ziw%(bdDE<<Jm+W~Ck6V;(IPcyBT5R^*K8OMdWJ$+}#WVV(6n1Pmgge$luPBHYRdb=I;rH8B$j3P1@z!)J8hbk|*^E3g!D`ev_m=muG+7Nj%+(2S&&dHb#Y7fv8(XuxfJ2Otf0#A`0Ag)rxK$w_T#1Y}vn@y~en-Q33XRWkMCGVB?M~OyTxmZsxG_F~_D9<c48cL(Ryz<zJNPUoWP!)eqBt;$JiR#0nk)+k~*B)WTy~d~F@V;fg?xBybg7x`fcZqxKUpqEXLKJ8SxA^n*IJCE)uoryQMM#vi;*}zWt|epp0C4t;IVZTHnsG?U?s4Lb^4g)mp{kSnS#;^fycIO`kmyciu03MNEU>0uhFl^8B!*Y>yIE@9R=`As9B<t5M-08^%6fKl;sS@IZ8<*&M|44sG#??$3S0wWpGFvhmF@|3)acb@>3FAWr&v6F`O`lWxng^0D;`%ql>3_N2F5R`Te+fDb0V}-Vh9_rr-PovUD+5@fci%>YOX+;Ux@f21>2EJiofwOZD_aXU7`y6_teDSK>ljho`gzP0Lrk~Q`&%ir;5QYEh;q4Y?sa)+ekE?a0RHs7u`!#e&JA+-d=K+S)+tBY8|C(O1y$h1E4U`WnY&zo;t4klhd#v+p`DO1*z6gNPfS)8Ai&uv|Wj<W1)9D7^zg?T{AGPBp;%b;OwdeV%<(}{(j`WkaK*KmSyaUr^Rv?ew`#xSmVkpN|z$3%UPoaTj+?p7QzCk6t%^My9^dGbN+Z<%6=H)_TQ3018uMa&@~d^rkbW5gz5Q}leleU+aeBkm#ARpbSlO7aj!_{fPc>8u6_#*30uZnU}edCEH9GK<Mx9(Sj?0zwl}T6DN?mdgD6hPZlyI5elGfM8XNqiY)1Iq55JeX((zWZr-Xc#CTf98gU*@WqE*1tQ&|kL+zCaeL;Ar%zJejbrKy>cExelSlhc*sUa78Am7rPY%5uhthkKL;3<s0yw<<HVY>Tl24b8P8EKBKtn<&&Rif>ckDw{xjim_?c-R|7*enTuv^~pCK#o(9)9s!}#h(Ae&W3|5?#F>5qEnbD^!LiC3%|gZNxk<5(SdvOI1_4v*Q0pu$|Cwnz*julMmNLZ2@8I+~0uqxaQqci6?O_rGqE`PycP-c~uko5i;RZc(yk8VDj~Y?J`aqoS$igStI6^wYX|g%%>OE5irVsD)FS*Np^Ia|iy)tHUmzM9PZIC@h(PTgOZIP!Uf_5D<V7tzpimfUI>w>@W_Y-OEwUf`&LkSgHLs!Pqf`$nnNKahulx46e<2)z%J$Xg5MTkG<{*PjD)+ZgFgqR=YL=&*qQ4*pmf(UY7*<d}zfdJ(jEQ9uA$wjB?_Z13xf*W6(%n~0qE#e@yiHL63q!h?UXPYiT_zZ#iH8G|U6J;9$(bgp6HWW4s@jo7K)lQwVtuLPQighLU+$ytV;d2l$;fimyP*zXrMDOz&bq#f~fnZ)IQE5%Ub3nheF#f>^w0AUne1?L(VngFTV((h`5zhxsDFTH+X4ki~YV#)}V0V1foRKD}l&OsJgjR?~d`Ckb$bj%ha*#ITW*WUVdNhEe>v(_So`m|c=ryj)9s!!y%*BKdPlC|}M{G)?`T4t@6xUT^0vz}_i%#$#vt5t3ccM7(T(1}=L~!eZsJUZ%<MbLI#ug??K+l}A`N}W|sq77MU)6qB=sp4Jg`<pp<D8G70k*;;TH(&B=lnV9k5)u?oyZRoO}Ud7#~gbYpbkIFRg9*>F4=5_WRi$(IYX!Z((<<TESL{_P=GcmoQE=pkUWw=Cu`slDqqR+g^v6b0Xh0zWTu=bEns67su8m475Fz@&*7}Y>ATKhm9zXYv4_-5A;qD4R6YCbxn9@<3Ne%)7Z<7PtgH%y&kt1+Y*H(^>e>&BKD^Dz{;<s=sMCwh$|u?@?{Xs&e7hSAif^Dvp!IFXzK(guG~0k25fUt*<q1=xD4A+pq`c_Yfm;*2(MfjX8iYK%e70K=1C@~;9wJfMRqaPQQH>AFvB-DPXkkp@WDkiJCF(E3b^*t#c`AG?(8AHb;Y-cBb!*UeqqbUlfUMYSa)r$@eFXubm*2a+z8c%}PWsdLUsX{B@drI9!C6lADPg6aD8VR8KBz{6G9Wem2^qsK#53s3J0%J!&Wzr~3+Ht{uxY(z#Dr1SWk!i?P+o<#shrK=h2uHYh-u`Ef`GKJ<|K0k>!Cm;6<`m5ivtiNrs*d}CQ$uUBsD;_6-A?`S1F9i9i*M|m^Jr^=fMncpN&5Q4+X%p2^c#^R5TfTCOc@0eKh2}q!mQxtWM2b2L6T1Th!_vrJj#bKU-R^M`^k7#>>3{UPLDf@A7fF2M1^OY2S&GjBX`!ACn$ex)dOCAj0i8t1-Zo`x8I%^41;XVTch-XwcK;u{iH6w01IcnDy@5Q7EhBL3g~nnG8&h#KR3v9)&W?J2Zb-JlIjgsX#$QbnGd6_XrM>8ZP)w+<MkRUXl^Bwrm}{$VKsArNkQ`MshErf9;cGN*es!Mgg{!bd7>E8SMqH@OTJNDPmx<7&Y}+>4K7YQPztI+6q}SBkOPl;e-wF=?%ijoUZ;3?e^f@5k->b;YHgpi4r}4&IK#0rQ=4}Rm+kT2Hcy}O`Hd<dBPj)W9YW%U;k;~bQz^k<gV<P*FllzLF&_`2zp90*Vbqg_QH$K8DI5$K5O*Dyu>Q*j&Yat12N!!d}z`w=JN1P>vUk6#5yA@u|J0xai_3EpeJ5Ujo_$fO+Kf0LHXWL^+<7THxx>T*BKdhw2P6wsMjBB?%Y9XeyrK%y);cf<1Lp&leC-2=S^zdC4J8Hp3D*NIESRI`spy~v4*>?Kp{<$5ddyoIVraM$ewE>I|)kuUTu`CDT$iBX>Yv^?}^+NkPQwqa#7haikQHg#GR$-UK_Pdqwpl!?7<ymrXW($50I8s8131`a)z3yQkE+$NDc;cBJ!I$J@};R+E7jWAQCT4`Az<Q6zK+rrY+Pr%S#`P;^T85D~FLOYd6&0`=Vk<lxEKbErBY(D7Dn<S)w};^F4<-Y}CXxU()&nmiYBmfM!jwc&`a8?Z;;V5Et=U8ezgqJKQ043wT5a$@UjX36=oyYwi}YcQ3*jJLw(#$)<ekUIbKMyv)RAgkVTv@nHK^k#urWG3M6}(08;j8sAp+r9amsr}<*K$aA{lLnM{;lzxs;$7d(87Z+iAM+z@$%UBBdS~D-6*=9|2ifsS9IU{}j{^8*#t@3;q`4_wP<rzqlZaa{9RPZWUg39T^M9h$FS#MJ-T7c*~=O9O~&Q%JjFYE2)XQL+Flmde(K`7E}2n6P-cuWO>9EE-oHXCCV`pinKk3!onh0rRxGMos<^|e#tN+ECLT;&apP1Fbnb6eZ7O@4g@;4&voz%pN<dHtjapOpD*^eE@ImNnjq*&Dn~zNogpZ_X7|4kLfow&;}5-&itTR*C*ACXKRGCE$orM%-RSQ6RBs%Vh;pC+PiXVsq}r3E|`Dz}R%Acd6G_Hz195_<VWvy1n8St&wsqY`6K1ux>bmkrVQgK3`J*tiu|zN)6)zGwq;la_zZa*guNnw`ij@)Hz7X3J8RrF6nbe(^sT;sr7T-hwH;dv&tmX)XvQCw8>W9?6=4w$n5Bn-#rleBU~n{j6zu?**y|T6>I5OFe%VlPSo>1xql{%RY2)4!UfU211i32vNo~~L@BkBr|MO^PqGLL?YBl)<MxxCUxuBlb8$*v374K{$ZO9CFRtJ^v98X`qF$qN&824KEDE1Z)go5B8>gDilW(id2=?0^VOk$bi=j&v%yKrT?irVQ`I&llzrhW`l3pmNm1!(0HG;O<O^$jYvb6<B&gFC&!6Kud9!U{O1`e+@&z~E!#xPaa!$>`Ox;B^UN@v^^iPw6pL{6RmGDvQVMWy{wVlyhf!N~-`{=nP;IfxQL0itM>bP^?;?$;y}{S?I2kSkeexwAij%s9BR989VTE$_n|_kcykENZ-1yxb?SM5Ms{GB8`NwEX~72qN{_>X8%Ji4;m+E+cPI=4^V$oTUJw_~%g0*&f=MbR`(Nudx-o1AjdLiL48jFEFVU?t->_-(IK_9V#oc!{|2AjGHe5XP74Rc^K}L79`2qd)G)hadz5ASqGJfC_zfYGP-zWdCybQqKQts;>0J?#%R0AS>OJ?<T+Bec4qVATc!0lrRzCeh?<fa=Tt?U#s-5flueRC2UEX<*XUq<$arjZY^H8|V@$}(-l9sAN?de6KC8sxl%*7(YmdALkin9G#Ho*9*1fdjrdpg%K^&~~iYO$ZXE`|h)ZUTvJJK&Z<ev$iAzbfNjt2P&Ta-fg@Y3uI-fT==Lp!DVJ4hl~Hw!X2iK$$f7pIW5xx@G&UcQ5@tvnQq;?TG&DiMwFHr`smLke%PV`(fd;bm)n7G9u(Ot2YENX(dKO^QwJTa7hgceZxwHYmB_AG<_$I(;pnO)Oliq7ai?$o8+bRox(v{%e_#EQ*s~>_Fjtjo1I2MXpn=QZVDqnM>IFIU*-f{giMr45N+Iu+F;g+gTCVcUhfNN=*T%uVkY=m<VPo5n#$F*hC)K_^H@cD<GTshNg&zqltY??FjVqHo!`LD!lJ3|ARf3?d}KAP|;2B?h+Q0%At0y%$YisaiEA?xdItK{Z4lKSll4W1lV&!N;1PugC}baMMG^ze-teO!5i8b6Q0F^?A8_12;6J3r-V<k;T;0E=Yw2DT!iRDQ=#ojrsPDbT)nu=gFMI^`dI#{y8?qAPZD>ds4vxXZ4}(xm8iY+5gu9u(U7~q!GYYimffJxVrNRFqXrAw9p#d^SwGl4%l-lN8;|>oJFmi4c*4Wtp<D4%bVw_!aOUOEJ%#v#%*g_+a-#(S^1$2J@!b!<k4g_Dm~><P7J|uq-$l+k&D86@l@$`+<)BC;-eSG5j)MqFOO`YnF5$M*U5aS^C-lII7DV0<%NHY>J}L&vv$jqGT%!|1hg@I-xrib^fX`M;|M2yS&iC!W&dV(~G_CfQFVYG0Or|_HJ8EUxs}x1GSDC{t%uryM6=uc|STkgsNOz^kw8_uUxnSK>8^~timXr*VB8Z?0wUFkoNE#dLO}Z09!p+=72IbhrB~o2cJ)pL=CD6ZpT~Ey^F1m3l_oLq&#h}=Fe=ltNk(yrn#6qT)*CdT=owO5^Sn0)T^+RfzrPc;kR>NT&HJB9^>g@Km<vQdf=mW1hBOP1s$f;vDNnG9sWGqtR0S@%0=%dsd<~y}KV&T`jNVe(F;Wosk*b~SgdB>5Jx2P()^}MO1IH4C^Qs-1MOtM)3llu;dYv1_(h6PYv@otb}+|d6#5_}>w_A_t64=UBf7RI$4t9Ig@UT-I~j=dz~W={`Wy3t$fK?&O`yWEKCTVhd*fJGunyWi~0q=tkTLusYG#A%`%z(E<L1O8y0CREKz1%Dsk!xmz)t?7xv(yCb>Z7w^qOU0fuhJqvFn?<sj!%-;%BK52ZaW+`D@gaSiJ%CvRf0TGA{uZ{&THx4~4kXQfSTd}?-6EJJAXn1tZ6-lay{C~JF$L7Ep+E*39Xnh}noL<Q+38dSd5cGCE1=vvv)vLI9h*t%H9F|<Mx6IE()mV%n>(}(-h$c}z-(To>v%g!34pod{4Tb_lx#O}4@M^kB4lZ5@CUuq$ml;s_c=*WipUyBMn~b5wyl0r)TQo;8zDyP!lb&x2SuL#6eV@I-#pwD84jSLv5l!${IiZ}gs2n=4z8Z`Q|LH-=@^)l#J|8)GOOyf`AT(SlFwF(&`%fi6eWfB5m6B_H2m$CWpqk2=4ZkTXrnHHs^f!L5ksZ~?JTCp(06=ognNCV+@%qsZZkCSQi^-=mcnwGn@MW{wOs_`?vm1dP~>Qj;p#mSSp^0CkbtgnJzB+}Qq8$j;7Ks01K?QGHCRguU6LwtV)xKM8j>@LUma_Tx`G2L->C(>N4#Y-)bLsZB<;A^%wwrcf0u|gSAnhTtR=?SDY6h)Fwr=Q2}m^WdM$CKrSUXhg@I4x<P2%F2^N!XWTxD(l+(WA7e>Hu7hmtf$II>uhAWa2z}0r(4b~4WJk`-~h;#v<MQ#6@bj7&DrkOJPfQZXPY}7|zt2?O};9F%jc$k4(npO{p4CzC~v4D2UMaKx~XJ0TQ7Ab1%S*tWdMXQwR103_7oqfDpj-&#I5`~n6e17)Y5_&;(@-EE@L<S}(V`{bh!M`EjbSz(=WvY^Tt%y*z`GI_Vi!km_YTR!y#cpB0x1^=Sj}a(5ptc@<;u7Dd)-55L{En(h-Z|)I^a|6S#Gcn~<=g}U0yO?-P2S`PLOt(`u3pMYloGD4W>$tlXEuOKS}OJ^a)t&9^zzS_6GChOZ^(+yi9<5p3%i4tn^rze&y=a-UbM8xu4)F)!cg>(5|LJ&{P;;=`>5Tj&ePcC9jXQ?%z0vBBqai{o*H{l*ay{ARrcf*>$zPT58HsUOBhS5>fO$aTbZ$!Ufls2>irb+E>iM%llFyuEQt!`m=GeH5-CkkC({BCoC4N?9*ZvMb%Z&-%3do&FzUowSCTUxS>J%5&Ap&$01?f)Jz7k{(Ws#C*iUn&cre1k0oPN5LHzi;73VG-MYPmSV;SYuWxP7D6&S=oN0A!?E<n4RkRWeP=t=JSH99?hHL#RY`^=iN=v3I3Aai*Og3Rt{=%nETJ)Wk#j1P~184s>iI!$g^ZJh*rA~BF&@;yCfagMj=+y_H@)fdl@Uzae@=&RTxuLxNlX3aP}zrM>x8QP2)Wf@xyPJRjJCst{w%~U4>)BRpN^=#8;K3R&(8BY3O&iGi>Hy*1xV3Vw>w7*O?6wyc3n!u^hio_w$4%(ImZPTQ<n<CnJst`W)g(Rkgv&7iiipQ?*7NWDoKrDfO{dd$Fet-&dbHN=>LVTKC|3j6lo}yw3X~qtxdi%dWhiQ3rX{&DfeM1pYCA0$Atik$-b)_-k@JRSpF3l);HU&;ZDp<3r>K_sf7g)d{hk6fscu)(E&YtCNH<-1p@eG4|bab&AHhv1<UQ|X{(~PgX++fx;!JIRpK(w+aHNZn`k1<n6Vz}QS61I|}-r^K7Elf{?Jp&v!L`Om)3Yg6j)v3s;1-@UeQv|?NQE-|v8lhh1e9OKu+6M{NYe-07>)taSvcIDXEZsfx;(mdeg(chym80xh)~sl_aovN2hmoT!_E40fy!2=vngwuc&4A|q-_}p?P~j7c6I$(x;{(sCq;d3b%H}@A?lXN-gb`1TWt7-N84f3Cks#7Hl*lZd;x^&E*U53x&0`bp;EGPpGaO$!JV5O*Jn2=-@Vwr4U~F{OHVEge6$@6LL=<FCj9z5g#x&#OMQJ~XX970a#<qw(OfN|_$yI`NN8waxcoavTfRz@h*uy&-80h1pvSivI`Ff3d<J&|e1M?oFvml*=Z@mI@g7s1W{tA#XxCagBLLfnOaC)o#=0(ng`2JqHFE2eTQA-ePGX=k3y{GJ39Dl9AHw?6O+;N>WQJp#6r#_UGx>EFUy<PofPi)bBn;Dfaeo>WB&_JJQX~Cz0u5kh4x8>h;4?Uc)BOs-R^D<>VWp_Ad*pDOEC*VB+#KWtf{tX;dTSF|0-?)E9;QNg4h{BUW*5?`s2p}bsNCCagS697ReuMO$CB;Pqm2=;Dwne;#?U{EeDY5k0OZCLTa(6)QQk#;^5u#0L8E8{9y*k!G^oasQ93rt`XIQ{AaCW%8?}S2L8ou;f+!kY^Ld%s=RjFIOGb&c9JH1;Lp;EA76P402_atfpj7haSBcZ4~4-gXqK_XFuZAW~o9*hyS864bnV|Zmo5{DAS@GK73GsN9P9Z*8T$yvcA5PZhSaRY`MBr*P)!tf=UrIgR<)E=fhNrXTjC(4h&T~Kn=5(8Jh&9D5b1g_*i&sg?75>gbG*b;UCgX=hCJgdqNi_r6SU+rz?mxKr~0ZdKSGCT{~{X@=4v<NkA&-a{{yr-LmcbGE{6x70zTr_nH1eg}#xvDRJ@6pzLkApTZrf>!>#0G-c6ZzBB475gF5dO{M2|$DBplK4K-p%$Ht5Rsgn=R2^f!gkS+6RKv5j9gtIY<N8%*f9WF58p{EHq@_#p4NFKQWu#3&RxUEC`SNh8HubK2oKDZ*&1N7YJ5mB!DBcJr|kX#~fIIl(@S~N1+Zt8qv)7f*P1!Bu=S{AsY<x?0qctoR}3$IaHm0kfEm(!+fsKjQ|iDaxXgNrlK0LLC3~R(1=RlfKUR)-M*dMw8`@7VHSf$%d@fX6*SbP*+%eSU6rzEvJOmy;F%+EZfp3X7)pj$4khjUlkJnA--3c7n)D<|C{T4~R!o7+FQnCJ0z#NANH|Xh-WBMVEU9l^8*jx{79Oc3T017+-K}Zv51Dtzz&glmFaf}q``*(!d%EvMM;%vPd(_KAZ>AbllkW|r9;fmS0;Cqk&o1)45+*>!Wf~H)1K{$tHfeSPIlT<Xt_fb(`Gz^-Y*l*>U3jE()Ve={NwtG?m@HEcbfz-9cit=8f~yN9EuAcn7vT>Apdk8r+{I1tH4gLcmQG+7*zgp$zDXhiySMp`t$4*5p(W>H4byfyaxKweL{iN?Mp@E*yqjZb?UXl-Nu9k8K<QFyF#_T09`ZA9LF%3zMgB-SAW#O1GFOR9#KoMBWzTLm!#hW>@;;>M{0dnWbR(j6-3JCa>HF;!Zt6YtXMDMtx<5hyhgbq0*%tJ*9vQ4)|1l~pa0~TkF_QZlnTwS3JGn2q_hl@uL78<Zxq7KYA9qV%i*b*n7aE4}Rqu&mPbroi2o$LD#JtWJ8%(-F2SyaJT}0l+X6<ti$Sw82ff3X1Fx5SXRA5#iGrO^Inl9<G4@H@vn$X4Y12<|(htwNJsK$pkxIGX)<fIG6tW+?@)6+l@BR@lDX7rf9Ba1CIbTJcwpF^pG!nTtLy+(AUESItkeM}ssw7!Y2wU`S<I~3yMbC?=<)o2!|umBxd^loiLCx8Ty#wI6r)3aH$A_}yQ1pBQeG;JCLd6IlPjqCPAIFeFd436vWQkLXO`b6)OED}S{UL|t);z$W|t=*WK1Uit{CiUd_KpZuu=_-;yR-w57Z-u_y0XbJDkXCqaU|*T{h~tZS3Upi8Gw&QY3wBa(z`J=9>6dO!Prkv^eW*6iHHJ~?YZx>wLlfSDvaPw*y_r8$g=pi?{0f>Z`U-j988|5Ve6)emiZzrJe-j2oUQ3LC(WOMt?^WfVOTD-Qsf{PMTF`vU=>s7b$C^SVIv3x5)_U&JUMx1jt0v*=1um*bK#&|hlfuPm19fJ-?Yv0M5vET|G8H{)JIa(NRS_d(m4WFUu|X@;1JxUvVd6Gt2s?n;|AjU!@it0a-7O-gX)#Q%E2dRR7EoY|c_HX0uWy*aS7drl+36X(O^+848G&tTmoj4=?}^qnW|zRUxX3Mec&nt%gTkjk!mI_hvH>c}vuG(U5S)O75(PW=wcRK6ZaHG?T-$UMT2IBYsbolDucfvjORLYJmv<)eXn~v`GcC{UJ7<_}Tw2cMHKQZM`xzFcS)cPwS7Lac@^M*`FxM=wP-^yrlhCqg&Qdr%=v)sD7-lJn-Yz8+@*H0V1>zlQf=m%=8EV{-zTLS80rc^~*RptwIEYLuD%O0uRE_3jF|s_2pheK@tQL8n#CZ^1`B>*#qR(tdUHaBq^>;`h$ZPIM)=4PZDb37;p&2T^)q8Cp#i>a6$!5@cx*_h`oDonU0>1>7B@w!4f2vOg$@D_JaIG%rHP{2$spZN?fWWlfL<ziD)`bC7@(b<)Czpmj80n~^ION7b(@4{Pd6=3m3K~m7f+tJS8ahG#lp_R$i*-TQ+AfMypkeOJ&x%fgF||L8>ugFCNf<QlbxlcJ;E@eUYW3A6{ey7jtNNg4mqbuIH8=-Gs!52J%LJ!(V;RJxxIt+nE&-BEToYgGx?v~r*;JX3F7XLzT^@{|B1^{IE_wOQ{j$Hxy(Q_QEWE6RXOvnOhoSktl%w(EZ<=xx%5wE!7=fKQEZ%m)njs&L(|Tc|XMqNJa0z{F=26La2dn@yMWQj)`|akW760k3d?QC<w3%*{XBn;U0aqX2OsK@Go>;~T$T4)H5lHi;p4;iS+5_EBF@sXQyy*kujbwsSvJ5&}5dnoj{U=asnqR#ov1Ap)udZ=Q9$!tz_qQPqIC~%ZYVv|a`d|W}J!<<>SjLuY7o4OO`KzD+jc&1`h5OKxkOK6_B7;wMuyEXkpCNo&JV<ZQsXkK&03cW$y)!T=QO0}1RhFsLZc^#+L|gUvG$+yZehLmcHGX#+@o~hE0wKEjq^%!c>+DGEuPJR@Wmh{mvpsrBSY2}~cCT<DoL+4<dT@fMI;B<h5r2vY`}AJZrde3}j)QyAI1jk3`g~B2b9l?}X_Vg&i6_%5HTRT*zs%6JX%cD{_AUx>nZK`y)s$2wj684rlFNEGGs%pon<iHhn()Oq`ykDNmL|?b6FO+AIYUsfMN<h35eiE2R50F~S`WOR<?X1GO4fVIv$mBrs5*hp3XRJek9m_8V3F#Gbc~5h*qkH-6&at&;ssjISjdX>YcTbcX0C(EX~?kMs0-A12PoIkNe4VQ?;=3`pR?Yo!zglmDiTb($;%+x<HkOSD3gh_=c6=<GJv{J*(%Q{Ra_b2rFn!IFFDFy!cqdmoUIH^K-N^XP^t_NkD69o#lh0Nj_t<a0I`5mq+a+SsW9Cl&bD+Eacf}$K1Ty&U?#x8k+m6*8ZbH~lSY}Axi&l-D&(9tr^L5*+j?FF@6T)t$h+dVNV&yM!K|azwhOyHjX}5t(wmFQk2((S6lAFdm!RYQFFK1-?K7{#teMjay~+iSw8_{u)m$V+sv{A}>79)Gon9QL3;4$7R5IF_Xfmbg^2WojI+m5BL#!~jQ{A9CJl<p_rbDj0+G8NdnBQ#qccgFFGa1D&fPC5@hUdo@Nq(0BN-=Cms42{K!%}cc;7d9hYji|7_wn~N@bt<);u%V;_mH-1;Lhu{g;hOJX)u=P`z`K(xd4eI2r$vffZJW~TH<zr(Dz2$Q%v|oeH_HYaK*ZK!HU#OOsVLdSn?%YdvKK3#UhEsXW*LTEP7PXe&?4iT_i_lSm1O&q<Z0B3&Tt1WL@9e$*K{#6qs4@FJzi0kDTjkqf5boYLNBor=mVhW4w-Uw>pW=ChH<i7f7}@1n@VrT|?93MxT-qRjk(=>SsC8rFqns*BtdFPSt^iUCEz0sz^pqJF<p&PBd>iC@-OuWl_Z>i}n;m2Z|Ux%)&tt01s>&wR;c}PqIqrz2_o<U-GOw6r&_`62ywu<N-V%3(EJ1#z|bClcp6^^O165E?&O3FGlS|_E?qe0Y5TdB8Dw4otCJqT~Z?Ipz;T^feI>xrC}9Z7yGW$ehdb;yNwXPw?W+id9>}z+40yQ%W{rqrB&mrWNHSD_&5Lr$Ri!KpytkevZb%g%5%XJQEd+0G@c{vH;J>2b|2o2<8ew1<Ee`l)IW{pN(<v-y0hog)S$=`9iR3vAMkOZaXS3cPu6{-B+qiF&Z=yX5O$SUhfpb--Wxow^}Y1-stFZSVZA*e&Qjnkygm!0$)dpv-Q{{c>q{-rrzoFIb#Y2XoRQw2gSzn`*XRch=V-10RPrktT9B2*DlCOYCB5D(OZ-<1%i3a^ShOw)<4A4}-aWhqvP^GG)+st@X%J0DP9kpLgG?Ppbx25eDTLOE0)eiuL{W)rscx@HuzhAi(h*_+^eDsQUzF(D<+`f6%@iHHC%FZ%7Rz#K1&_%1f^<cOwoD)viH<!1WpF783uqbV)GSAls#@DjNO6U!V(G3o3m@3y8V(fAE{TTuvAyM8b{9d*nIc+V2XJ8Ka^iJ)gPjV2T(n3^s5veDv<9>yp$`Fo^uN8CU1`LH0s!vuIqNF1ga(!A$@4m#!&Wce23%IKlFXrGR|NH{TH~nF?gi!^6lq|1QekY#p4II?C#XY-iwUaO3dNwR@C#GGRs20fjuL7X?Q3Y30SeT{XOJeQG6tv?7y+?h)tY)_Xp_~!W#gVbycx`kWD$;2a)u_OHB*xe;^O4O1;oFCdCh&XFcdc!T}x^&<CF~{YK$GF5VEQt5}4k$o|(t39Zg$QLZd2ZJ-r1io3;08Te_ibn4>}MJWeuWZZx$z3M9-$frQL!Q@pO@UUrZH!#>=|6&E*6?qJ4)s2exfCgXTSc09bKvED&oWg{VgQFqFmCf7T1Y3}CuRS7XP>8|Q~1aKE#k=9}don)zgi{tF2M}E13Qc$BH*<3jF-dflr#6JVJZ%Rqxu~6O{&U#*X67(GWxsv!F8VLjO*=bFbve*2yMmu=V0#u9(7)bMk7nbAqiM%NK*bNEz7n}%ua<~wTih&gsBS%50Y;@+xV;|cYG4Jd&+fh(HjQF|7>QNp~12`RTV*9pY8R|9oYkRFRRK_MUM9CtO@>N2DSB6?F$cdDyiJtK7EHE|IUL>c<F6<l42&J(atyoChExzoioHL8uZ(bc4Xa4#4&9v5`HpW~OkB(Mk<cK%*lmrUe{9AAnga7&^4p+)`H2}j|+<>dqDTs&eVMu5#a4@_%xuV3wm&^9o`w&w+QmRCe-jo17hM{*3^f_-36}o)RlqyIR@yz{om{lgG*WB!DexQ;{D#2s9^V6sQSoUGfuRJ@@PD-rTrc;3u-|&u%y~xMu_^qz(KPsz8iGZk-IH23(C`$I>@+Qln?82;CC=N~@>Sm@dzo)>~PD9op>&76opX<I*Vxg^!9)B;4bBm0T&H`333{tjp<^?wtZ*hJZ^aFxwW^_)IeoOJ>;3MiaM9%D*Nof>QQ0Gb32*8j!$OTN&t#>>B*Rqlz@`3*7HB@TB&tn}1y#TPJdVxK3p%O4_n6@j@=TCv7J+*MRa{yJXrU?AVz@Dt&<<W!$=^|M3AVUeN@!)tO!2NzCFH%eJaHa<d5tLuG1oD(Dh$%%XD$0+L3~;I6>FvIZdZ|wY?)Twb>`L{ItCIvz451?O+)nhN|CkUuW-$SdBsy7K+l>=DyN;XO3qcgJ8^X0~@0g$;J-u{aFuj}Ieo<ot9NAz!&Kl)s;O!p%qcK)>Qqr#L2)%4+if@w4HKB#R2+N4qpca^Rc~{Ldxj<Y5VxK+l?PzU3Y$Ixi)}C62AL7uNAcyXU=bTfhI$nnU`u_kKz(}e')))
_PROXY=make_agent({0:_DEMO})
def recent_style_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
recent_style_proxy.telemetry=_PROXY.chassis.diagnostics
agent=recent_style_proxy
