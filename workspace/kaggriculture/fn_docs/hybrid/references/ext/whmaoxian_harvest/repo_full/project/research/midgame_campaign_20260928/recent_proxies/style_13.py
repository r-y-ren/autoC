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
_DEMO=json.loads(zlib.decompress(base64.b85decode('c-rk<U5{JYar`gyJP#{!G?w!=mgrr<+MR_)3gIjS!$2Ga2%HBeZ$bWh<Qekv@^*Dqb)QShHUbC`!I`=De4p;>>gr$q=jPx3_?JKb=`T0`^vli94^K}wUv6*y{g40oumAP+i?1L5{Kvoi$DjWD>*rr?e)IYFe|Y%m{f`eHZf<YhKJIUBUwyfK`TFONkMBOe{q*(w{SUi`um8XP^5uVT&mR5$?e9MSJp04sB~QB#A5M>Xe!&m#KkjbC2hz6b>!%-fyRR+SE}Qn7&+k9H`@`41fBO9Vw5esYRv-TM`Jw#F)63)U@vbgM?8C#`9U8D-Zhm_F`00n|expzO-P5O=FLGGnyuC{2?eGiRvxdC9>UQ?w)QrWjuGF62?so6a=V&>7urbHMG^fID&f!(_C9{0fEo$Onr~PvC_8|_=Utj(7*M8pK{J8t@_|whpW@La~UU7??wwS?rLu6N<9zUNgx!Zg)bO&WOmMifUp5fE}JN%4v=`b?MSpD>AYTx2j&y!ags@d**__X`TUr`>c<&$PFK8z!7fqLIzq{I7;Pk<ea-I`X%@kcMu_4eR-Q{ug{xU%LenvC?}XR7C~^y}C{DUY=AzSA?~;Y-K2_qOEG@SF7qH9Y$^4nX;Jad(~`c{<YKf^LuMqBGYXUa(tdCpQ?^c)nThIX)Ei@ASg(iJYV0iR3}nBi}xL_^^BX=?}l%ef;$P!~1_ZADQz$JBFwHuz3HwkB>j!6pXpfB{q%vbek={fd}twM2H2n`BJ&-;t8d$PI4uK-hjz0UCVGapaBF6%etBQa+@#R-NWIX(}$x)b3QSSsp!w%;bpKzYH*eY*`~0r#IVI?;lVf?uA@n9TT!Qhs{F(pS=8VSHE1{4q;Jl;_hQklHq`O*olM5*m3(Ny%Qxf07Y7I4n{W)-P^Hs7{Tpj|JY=fldHohHT^rFv?WzTvczRs0cn-fqp3kh(&|GCC9fqrA*n_tzrx`ppJmmCYU`WVg!H^WZjO9YGtgQIJcue~?fz>=<LD!#qy8M=-H*T*^PrQ`5+JsIqn5uy$&yodL978I{ZChnMCzqvM8qBIqe^y$2(a=3T7krg@zoU1nZ4)D$L!UJaMoeBkogMjN>I?%wO2zxLp#hLg^BQ8K6Fr1<C6?a{@9@MB%`EZs2N1hiZGa#y9B-NIgFGAV76#YTr;iW&-|Rkq{JqsYU|Ru%lHM|f*GH&lvOeia{KLb?e|FapZNce5{OmM_rPqL?9WeVPVLJk2!Ut}v(*a&KAA9&^%Ye&G<X|$L4b|~@X^uX*H?@g6@Ap;TKeN)nn5@+lHWkMYr?Y)%6SUq<PsYo>dcNG@66l!j11o+dAiC&3uweToY<(RVAr@|840*<PW|NiR-_+o!a3KZ(?IHn#IvuR@YOp=$M_PTSzg9+X$LEQ#Zt`%A_MTP)2?xsV&JK;m*1HpiHawmU7?z%$_V}D2#nk4GHl}l~9%mJf5jEoiu$SMUqr+5iR?sSKcq82#FG9cYq8mWgi{6NH7blnGrN&5uxtA~tt=IcY`m)y1m1o2<)Q9}k<}fVG_0^oR(#sp{uQaNX&+XEjW$$x3gji9l^vG*|>2<)`1`7~yOZ<?6Y0x8LQ21%Vpuby_Yf?tWwlzz>fzDHVRGI5dLZuUHSi=@)(A7}16b;omJ=j`nifSTp{lpZvW1Wmka@t51U!#lES6oBEaw{6@=^?~VJ~JAHd*c|ulrB0j0&z+vTNexk=N5t?2uT{iF@f=?9gdNd78mLXz=-P@6=Z?0K`I~=lOY;F(->RR)cm_?@1>sGpfLbkJDy74ti7h~g}`|^6gGgmA~RxhB}=Ty1|G7>dWk_K=n6cb>%pb9R;&n?cHRfTz-1zrL58hRGi);}MysNqxgzxj+-@lcq0{eXFzFIqRRhitnTvIFNkOSy8IsV<`qX%#V+#dC%)nhM2C1`ZI`?nE&KtBGtmR;^y)F&54I+vE|NJTwpn%m`8*nXFZ4s+hyZJ)Y+OA0nX;o<!#H;kn6=1VY`k(n)hodK1$RMhAi}RpS9L`|}?jIk&{&!!KN{F#!X{|=gY`x64>5<dGB&|T<-@~Bui#iO~VX=RB`03q^hLfguXsg#Co}vZl<k#UYBuXO?H~UBUnRL8>`blQV5}lOOSJUc*h}q)z>tG_;4uEbQy&W@Acd=N$e|&t}H6=|>&3gIS+sDK1m<D5dx{MbWuSPK2L24u2f$!db4{42fG&4Xt4&kkpk*-1_c<}5mBOxDjGybJdhDrOqJb)y0a9Yf?ck}b?e3>!gBuom1o70)hV&DaUF!6|=zbeXtq}xQzU4fG>;x~)op1KlG0?=P{&1EF+%GISkUNpWTe;pj_Y{L*sf`TawpIZzsr+XXAeYw<D9p`x9h9MQ37m9iiNtK}_2jl^Y;iG#N+z|8WTZ?c+FQWN?qn_a3JfE7i8VZ`nP6c_q>9yNraFw<av?1VWypxv0`b*;U3Gj?H<;fq3CRkfcIVi%!-&!L_Uza)CJzEu*XeS6jVW($mE{zj;cHt#DlB*czyz&BEP*ylfP_bWC?RyaVtT2Qc?Jj94-L?7ux))Fw1$866{VqXM@>9JPELHn@wh-DI&znNV_;dodU^?ItA8$oSigu=ruzOWpd#R6=d}_q{vjN}Mg+jMpqKrX`NPhr{Vm0|LU#&0(0jEC1WN&>^wDaLRa}#k0Ym(yeoyI=4S|hSYE&&k)qA~z}DeQ+8fFL~wghp~&NC*@nc~Zuo)Y&Zz93XrmbkFTaGUumJnLYrJ0x(W<I_jVb43j_M5e`ikBkm^jzNup9*#YFLw06DWkOFyziR4jXaFobJ0_6x7XbNNT>ok9BvSKqBt)6@U*F<9sTtk`7flu^d?`J_9ZjThWr2`rO=o5%I=~xV)0bGZukXZUZzW?yM=eQ_jDK=OMuBd>xM5lI1RkLl)fVbCt!Q8Bz*8qc8F5<M%&U9v=)kGK>ZH^<c0pm>zwg<@Q@UPc8LL*@f&<w4RFr2*QtMX2~31F{!CQ8^vdJV=&%1wDO0m!_lj3i-_7_{kPt7$N<?T|AL|8nErpHpPePpSDjhDhG^5xHnxN56y)Zx-RyE)lrN&BO~~#310kqb)>LD^3mY@5<Ft39W8@dL?t5iH2mf=GK+*M3J3bOg5fyoVH>}cXVogu*?hUuhXG48U+r0)`Zwj9;lMmH>0#%U`z_07ftF!y#~^LP8*ndQBh<s(@O4{R5VN0NFONieVOr*yLFTn4uJL2G~`&k=zr_|Z2ZkMO4QDR(16F450LSign7Y#GuiThf_hd)z)ac%#u+5PncV-^hPiU)%4LPm6z`rx=&bh)P&~Beg)x06!2cO#X;%P!^ORP?-oB#*bgqd#xe%uf6P;I}Rs}m|%dLbCjDrD8W1Mkx6~(@6Pk0(`ukidg5+=ZOtri)Ar$^*yQHLC)ROCYI&MLnYXFA~SGs=H(;HX-YL;`k#!m3!&_6dtNQjBa5k$a%kWeUre)e{Sw4%~&InHqco8!x(l%k^JAGd$Cin}a%n?{2%&COiN7)8mg1pB@{Vk0pl0c>~*!ri&b!MJAe0;lRqoB;tf2iYUx6tj9(sm66qJ(ws@uAs#aKAzog+k;6ilKzf`JM_zKu%Aea$G~3+kK^%9l1Sf~0Vca?HBzBydCdg*+Q~_%-jp;+umcu8$)gojU-CSTc*m~qB0B5nf!2YIx_(?K3xN=!{!NN4dD^?HAmXle>m#-zh_rzQjjx~HHL}LOBV01D##_7vV`^d1j#33-{R2)uCsV+|<kC3!hga)fz#>9Nz{_5iT4sST2Vr%eO?JqgZ^Gy>dIOvi(4jxru#l(YG_Z5$k5cgOyCh*mWh-Hl+4_pPpxutrWn(IKq+tdw9+KvT3AO`2##zn_0a$0bd#~}=)P-2T7bV{TU6qos%VsJh&$x}vZPXSqFg@EP3lpBx<J6K5oh884g2#_7{p8%j4AcLMMdMu%rmj>Rx)({I^7IE}bV*l%8-thiN%{i%}Vee4V_INy>xI@T!CyY`yBlm;;9E-)P^F7My#4Lb$2^<PKkVLU%SG#cZ(kMMU*$!PyLL9I^ej-!6+NKXLgJ|^|2AgPIKy_Kc8^-4^H6%*bU8>9lkr)`5p15hVOp<!;Rh*|J(<|)<xC5rOwg6#f%+2}2zQTb56nss11RU(5q}P1^D^O5P*uCAsIFUi(fr2G$(fWIj<Qf*Xp0B^*VgcarnTPq7gF%qN)ea7F?$e;6g@zGP2LOI7ezfi>5}Qe}V;TYx>u^mZ3MvLvFh`n7XHdi}D2m^+<`HMr02(axc~^m_Ufo?Ptp_PQAtTEFGAFLzQC6*ot&a<K#7o(NXb=gQqigWT?F@ms3k{AuC9yz*csq%GH<&e-sbF+wCuiB8SS&Wb4#8zG?xi7|BXa`gCL+3!!Gza?-JMc7Ov*xDR)$Yw{EE!EAf+R+k&Ss(@iYM53A^c`K>;lL^Q6wZm55xD%aZ~Fn{0j6VX!6cyq@+a)#nFp3j}y%k1#9>C}9hHp^4$1FHWjQO9R9Tee`aGRbA4dvbOAYW0jD@ke<L+Tjz?A^sX@&(Z-ccj<;Z}M+&WWp|*j?v<bdIq@62Y7)ll3l235N=o=n~WOXO^jN4%sqC?uY%!2}(#H?z1)x{fI2}6037eir}`JDvr`_*Q6ziTMEX&NV*UbHn9OM75N>xtv3oFFKUIdukakj0uWhJ&Ky6WfXxN$opJZFY@GqBc37LAVRE1?DZa%J5Sb7}mI`?WFpu3f|FaEbO|{?heJ9$%{rvcgV!aoW1B<qZJkx<&?QZRld9}ouE}pPv#!p89MUa71dtH7-qh(3?VcvyuGI%cDtXCVRlCuZ~h16G}6N#Zwi3N)Y18i@s~?(pAdMc<z;RPjajwErlx*u9hA|4bAZj>(NbIoA4$F@>3-4MBE&#o{%YEnRnO+Q4ChP4FF`e*gZYhBVU=|Xy-x$f23Rc{$YJsWXYth?l4Gc21t$Wm^?0FU#v|P(3GMA1T67Z@DkM0dqPcteBq3_`wCNX*6^0g*R5K=Eh`_75R?6H`-HR(NES6@4VsOtW_r=)!YCO<Ve`#fD>o6ubSoN4%n0PWE9QIIOKq~5%fK38tMad>K#vpU2>mH+VKP$*4+Wu;Wd^9S9ol+kkpIvsgcihT?6|kdS)@<YsLk2`#6dj$<0*8m&M43K&3oLmmjz8~yw*3{7afK|#N__+zrnFc@lzZ)FsJ^%}zqX|ZAUKi)wCu?c$VYZ@S@M_4DC)0X6FvcFeg))(YyOg}H+qCh^sG!v%we%L?m7phvIW^`EJnLRW*Q}Lf;qfd1T5bhyYIjMx-)(i*$K5_RvAys>TxrP;nH7~kM|9cx*{D9Cg;H4OqH1P<?x1Kb!LwV0Dx@i;0;KhMwqfD=(#G81~T-*kKm?|xW~8S<h9E)5q_SX7$ZGQ=mQYNafLJ~zbBJlD?xgy5pfw|0F0Z1F!!WhaGnrU<6uB|j`L6m4SorJG28C7%cXO5<b6ys2YQq5=o@Q%GSCWptpndOi3Uedt%v+t6j-q6b8%B2a_k|zkbR?$j!Hd&U88nL^CWi*I_fNZ>35foL+lCVnw*FYpqxz5VtAU&IZpR&Ek1zSGffGT8j&U^uI33A4o3s~v@N*GB3m1}k$Z_z?WluqDwYdQWh-@@Ra$Xr9>8>h+k1f`ZDy`Rl`zP;JRAz-qYV#;?oI1@<(3LlPOMo&*q>fB1?m@7F<FC!n1G6UE`^y+YYy>4<xGq>U)Hx_0~Fx3I%-e%h*whU*~Nc>I?iqAH%8Oz*`B%9NxQ6hM+)q6xt2`vixH}vTuWLRPuES`c7PmL;|mu=o)v6k@Q$7P#b{J_nzUpWLz=a_m$!*uAI!c|A`;zg@<}U}tx_&rM%!I330}(%f@BNYNu|D-Z`?VuZm2e;Q#_O>Yl2H<>n=jSYye}W75rKGNB-(AAqX-1uB0G`L-*l>g<kdOE^6EOS|rpBPU{_8Yj83HR!U1HxoMSnemq0nL{(#_RcvT>pABgtRSwnE4eNOb6;f}8DAQZYiSn)H%@eR1YX?kiis_=5YAWNIO}R|T-{ob}$*CZ8`j(iR+%tE{?X<aUHao4`N`uN(;e{OO?rySt6Va2z=AOB-47J1|bz0N9kX0?9uKG8HlXI;Q3hOyoL#2|>I+$3&U~@Cw^U9)WOs+sbGUA|k2Qnd8y3@hQK;orq=(8m}w|w20sK1v|+a*kaj%XPgS4Ru)k_=-cPF>tQ3BpFVjqVr+;hdV=o?U$gxjln$_a%`{k?DTx)Ak$=ma0q^Q2)h0*7*odC3W$}*j%sv7TH`35qzyqKSJCJk;}#SuL=c{kZ05<RxZYsm|oC!?r`9I_CP9NyfN541r~wH6T2uO%%|`{W7fcf;}VmMnZ3acW5wz%RZ--`<?Jxe5_C40%Hip#h<0JU^%ysiA3@D-zi<d+la+{8_WIAQKtFZW;|liZSY!)WfC4Z)26jMO9*^gN+1mwJ=4DK*nHhgIHj7WMPAzxKkx6ZsCVHN88*?B_3CvVEAxx_-Sq-GJNkW;;oyb}mgk3{}Vz*ffG_BDh#tg7U(g2a|Ya?<+lEc<e7AjEe&R@zh-|$7~GS0HeG|1K4^~;=i`F}!i91n;=dQ$|p3zc*cFfPzxvE={voowV4m{`On*2^w-Hgg9qs@gA-xoNo^Gd#9prX$@*Uhxvp36A!$wMzGqygzG*d+WeX<8`%M$jyL4T)id%?lq_$=7El*nA(|{p2>K<xgOTm<J76k)4|wYP|7z37xYS~8xSOmI002H8wKAu`_9a_RAj|&nt}%6wz-AH@)WL`m?<Z#q?*-%f1=yfOUzV=RD2H_=#()8vBZHqO~(8YtO}>zPZq`TQ8gT7X*p2#4jRaLfe4s^Q`1V8tE4R}S_S{qh33@8XQf%x#$X9_z5Rh~Pl9JcE-%kmhMO6h+C31hAhM<oLY^QBvj4SJJ07qR?xkOdv9@_^3QhI8P-vRTnc_rWkr^t_B3HZw)mFe|3#?SKZXHZ=$+4unq@txdH;bia&tup{{*VWrB9uSwWq1;Kg+k_i*bD<<N+G0DF^d95I+w^sigvl(To<j+H?e`(N8m?R2vGx0DQWZ32JX7O@;xK&(0~%_N$56GlTMV3G55rspJ64I7g#s~5LU-k&Md9~T|$+XrjHlYoBa$br`Qt$ERKnym8{VGe#ky6_6sU|<1D(D)_)ll_qWimSDSA~HQQ3`oMuecigsoxYR?0GcO`lm$SJgmW*psFon5xQG`q}e@Fs^Vc0~n}E3nI=b?l##wyU^0namcAuB=QJ3cd={Oy{jdP-sPVS>fv*)yxcq5toOUx@+zgFuW`m(aaHrc}OGMA(KWY`J1+?i&qu7Ml*Yk<_r{i>kxFI9vsLSZ*V&)2@u-SRQX&0hlO+`Y~i(vzSG=4Fpi9(z^=hUT8B$hWW<otz-G`!+{21FD@utR_Qx0>1|oa9#@Veq*HjU3UvhzXe_M+)cE+#aYe&mGV5-(Vm?{pjldgJHO}t;97Gj|pB5c|1&d+gITF_5kLq>!HQs_hb0*JB+X*$yOUX4*xGODc{&(~*`gy$d~F}z)%N7Hczs3bTYIRD6Sn#>H;@`BF>b)@1Wt(Gk1(GUr2`=uxBk2jzoDuWqiu6t$S48U9$(@?{Q_s*(In9JXZ9VU@2l)E|%ZV7l;RKZe$y%Lh}g1~ha(*cE}MMRh)ko0|MnpfN#l)zU2g=hGpcS1hHlP@p2XSV^^;luo{N~c*U7*(`JTMyYMo#|Vs?^L>BQ<*qBMzL?3b3|?Urc@9^0YQTe_=?!UwS=g4VOT(OR>8V)4eGIFMu3D^S{QE{k7TdZqPe-n7%Ol~Q2l+*XK^JyYKlo+M;YvGXxty`j^@VK0CWqIKWN1}@KqtNB-<S?n@UM~v^aCz3P<R)SN4fOrgh#8H!lSUonBMg6!D5%FKq9^296DiAt#`qPEHy~99e^`<qFt!RSj4jHF}j8t0{=voc>iQnxynxE4&G4MsB*QGmmiNB$kwt(^GaKTo{raVw5s-Cl7dLw8{@ya|{B8Zkj?5$C|H_o(kn{k`wW8ce30=Fhzx40l4V+QUG?+n#vR?sMZBYg|E_{z`X=6acv?W`Y-b!1%hBY&BxHrJ)nl&#yVUTwwNiyNXcNw(V#iIg^H0SM%ew;kusAIX6#}PrgbtS?N0yI(){`3<GasqKb>(88`?F02Qp(umC5Zjd0&DQ{*BTc{VH`7rz(ch*JObKFV3$wDQbJ~Mg^8On)yOS#~iT5BpIqy$YHgyE=8lu6{9t^IJvTt2Whj!z@ABF5}NW<J*}JU2sLM;3YzWa*%cFzFkvnVf0=y*1gPt3WJ1Aylrr|qif(RR)vQukSMXn&TuWCxfF|AMx-VSpC+BWCS(3uTD_wn7;awLd^%LT5y8_jYtRfQp5*u#mz#3qxTU>-N=d4YZkT!L;C}Ys^Y;4WfDOBtj@bD=?xPCO!%t8=SsWhHMQM0|7L1i>gQYu}T(q_p*9a)hs5vN$DR|{}axZ)X|7+8Z~nPn$^1M7>9>>&ELC)`JeYH8FNp7-T=Zl(ru%N`#=(&DM-CK=}!3X*QiLO&~^gvC>z?h>bB0i|XLg4`-6yvq8V1w0>~p7Qh08h~r#fUmCy16E)m>&vaG2+bDB*(rR%#L!Hd$}Vf&7C74!Dhd=+Jc*pPFSAcUiB9d%i<S?lKuTJ(lOh<aR1L6$wV2~$qZghoSDg`I)8^bFzO?SSNCmr8rYG4)6uhILcuuTefhN>l571-Z6Hc)K12*;v_XMbD7VbeIiP+l+_Z3;%qW*bW&m`umvDzWSh5Kl#(|$+tLiRFiUSSV<E7<ZVewne<nWEdfo-b<^#>3}F@Rwqn1yQ`CS>Cn7QGqam8ij=(845J!vqk|s&Q?7(2+*ZeWJ3hzEV4*P-l<WMlPN~TN%9>pGj+yYhLTh!Fx?VEiQ4`ZIrFY4m#XiOq}3wmT`C5$TfM*A%qzw#`T^<)QE-B%;&)e@APykPudre1-s7Cp-ht;J%3PC?U7K#QA%U2w)4R7)wT}y5mL(F=9dMr|Tg3-6(mc`o8vDG(#-!?%Dy@VW6n<S3{^#4PE2Z&K?vmt~+JZHX-(4U_l(68M8orVjnA5bkYvEudgS5we(_O_iMYuf}PEtyU6d>~kXPWw4I2(|PE5w4v6xYS3Q!wG(BK@nI5axhp$D-36@pA*xQtp<|c~PsospQTwNzrZ*h)-h+6;#?$GyJNj6_vn71q^#<!1Y55Htqd|6E_<-b<#4@c>B|(Bo!VFX9Z7PRWWU)LM1c@$g9<6&#{i8Z(Sh45Y`YLH~c;2%0i39RT(<(+Sh^q_=rqvDe)Z<sKc{ZW^J6**&nrJ+AG*lPmXNoih=uu6lq#jqVYIPjw|r1{AzUoPEfy?FPs{-O$6?^cdjxYjf@V7a|_Khr`SWJg%YQ|C1}vy5-;r#D+g?FdSsvj5FQR*ISO_#99>8^dttfK=pw{CD5Ls!<yhfzB5NP~bh|TReadW6pmOabz!02Z6uNmN`%;O{qnC55)I(58P;zG$Dv@~7dBn%%HmqO9(<|rWRBz(K>1pMH<8fK3yTUL8ACx;Q`0(uucjmOT#5PHYTuS<M?V6kSPR-4GCs*<6JhbnwS65S(Q&TuWhp+Z+t8a2fj-Q~i4uQ?q5_S{N{0=y%+iaUuQ|nlfPMwOugZufxf3eyG?uLuV6f@P>&x(PKN$25qjp*wNY*0%ws?Bi&c3cc9^0J&<4J)`!&85{v@QBMQK#wj94vYdJ2ar=^7GvuYorG~=1ty&QP5@BUOSOo-1hpTd1RembNRm5pP*@Vha_Lxv1-MKg=H!Ovgao;H38~5<YgP&n+n*P=HX)_K6f>dI=(1s^NTld8w4hYtb)5iAa!R-s5jMo**=fliyG1!p)x!qz=Xgc!1e3t7d4dL&!k>ZaHj-NHp+_XcgOyrD1+N$w6C-vEOfDwpmKETVYmMNw8QrQ}jX^gQ$W%IItdw_xBLlTML<t*QX!g=*Wh6)gM15BgW6ovr_F`jug~N1F9T1q-xVF-h+ge5tKd9qi+X`5wD&T4e-FMeR<A&;pZU^d!&cNq?q{5&^V(milZ54zrL*O>eTA=hIylN>>hUW+|p;iG<qaYor0GcB-158Y(0;roRRKx|yR$BqI@v=pmFY?5cnAn?DtJ_n>mspp+PJD<u(=#Nd9QfntZ&!9ZsSBEk7p4w7O$m)Vt?uEE)&TAAZByN`$>(mF;Eempu(~ENUaz56PMb+AckR|l{}rhY)5-=5tY(cQtdf(RCvwhV-aPhB(o|ZSiMMOyJ*imy9;qHJ4<l46qkza1#Uab7t3ng2pqPn_K`Y6#tfZgpJG5zvl3%x4)ZR#Y)O#zQaxv@!AWiN`WZanrhpvH6_ZA+d!7&1x3w?TkLNo>u;jSk$v|SaX=gJBKib9swaAGKzLIW`rn$1DWH~`gtg4z}cizrxR(e!9Mwd4)f@YzV8qgp$Xq)tkS3GazS|C10NJ7ZE5?#@l?rH70{WknLNW}fEQg}k`~7-^iSgG9W43|Y8Zoru{jb|vjMv2RwQ-5JQ<;qTsLTj{%Xbm5xSFD}Bs`=*L<#u8OZaUHOORv>CQ@kJdhF)S`bSf+w|0*r?D=4Lb-z!{-;Gf6ls*)lUqrHV^(RaJHiU|S4V!gOU@nBP2(S7u{E!|XewiXlM9E7C>$wimflIfJ68rKUulkP~gXx#X~lMwV&^L}%m1AVK1;qK{u>u|n?+ru1yTpQ3D5lJ9<J<*5{_)397?PRMA)SSSs~Gq1Vm{AQHG<5dmd8Its}7GST5eZK0?Zuv+-9x}Y5fy<QdTn)xtM$Hbhl&JC%zty;JKbnlZE7560+yLT;W59coP3FfHXsRsBY!Lz%e%){m`xRvo6j=@wS++=CV3-uF&unr|_%sg19TlQhmIaNf3;?&Q@K~WqHe>zZxQ;<z1A%X9L+7m3Sz$~;Do-+SNme&k4KT~6QktSw55nW~(Q23I5F!l}Yns8|nUm*P&}GE$8)Vr^UZ0QhHH*Q%tmM}hCHQSI<nXso@H-l`zaGE=Rm?YH8zpJ7ekIs-06#w^mKWP=lz$!L0NSd3ZWO9q4Aw{YMhJkYN3N>$aPe1W`xcW^$<6`<3&lS5)P$ljyb|-zf}E;S=R-ANtyt>uJVfFYLxSSW*%hmmG7A}fQK?U?nzB^N6dWvmUOH9*L8o+}!d(@UIFcB;m2S5@!RpyRz&=I5p&!}NL}5)YtZ|$?CbP((7xWi>F4gm(5fDmA29(M~&|V60Lz<HrZg4@tWbGw6nM#g}9fUmRpVUgdsCpx9m0j>lZbFt#Qq<9Pi<-KZQg+-0tcF7Hy5Yd*r`~h5?l1|WQuCms@xb=E#v6^$5KB^Rsx7*Jja#^xa`&zL%%brH7L(%nGQuJ1NlfH(6k01g!eRh3!hE&(39eY3f#@~1URHZy(`4&8uzj|vrm35Xx60Fv%-eRDf_Lt2{Eg_|>3x##Y6?4kw+;r!B=1fWeD+J5wLOrl5%IR;vUomnh>h#jOSfK03ePW2+mqu@b&Xcici%f&Rk~U@OxGQt<>f-iJ~k=&p-kDN!5`@X#&%U&fYV8a2VsW*np-!CxU)$b`651`KL9TV1re}HghsX$aU#-h7t{s^VY56MER>HJg1}5WR}=0mVl-F^z!vM=+i0IfZxq?*mqZk@SDW-=F6U&cp?5Xc1nZO)hoQa+O`Ymh{w!CDDdfE}STafE-S<nhRy4OH41sSbLMg1#GX<?@MXkSdtrKJvB5Q*8PgzA2G#bxPHWm136IT;WGnuplI+RAi9!iW=%P>C0AreKbkFG{`|EfX`su&<7R&`lzW9hGU%+{pr$<wkaJ0}Z7_+@)|E%<#+Gt#JbVFLP!VaTQ=8FgKH#S{fdYhSprC8YB)VRzswAGOZ;+L}7&;51%^TE;iH94H9QIIEJXN8h9M&UKyAH!BsXRfRA%?fk%tqk@W;x7FopfxMOC=T%D7`n7f}`@L16)(7^wKd&GhW`#k0%6GG$sktc3T<*YBYVcCmim1Bf0Z$rtUnNajgHx>32arc&F|@iGu(OUL_NPGBqDFQMJ9EX(0xEv^8+3S?^&kD>kqT&0tDYxJ7`#<G^u$7%qEdty7aw^j0L-R95s0JPrkbYjiM&N#9~vS+yE<gh)YOZ+KxI%Ok0f<+eNU4b_uT>aL-{;?D9?NvXY52)r%36^rL(dnEMYOrR2QsuK7zpWnYN;zJs=C*y)o9eM++2`HE3)jLnHdS^%IcgG{ze;@voskpIf3WQiKQU_3XWkN_96`c&Q{k@M>FGGD*PFPzZHIa1vCdLu^*4-o8a;kBbfNb(i8i%aU{4O;PutSBRA{)IgFCli;Lx!Nw`|FdvGeH~!iJ9n=j?^B9RTESCn#5#T#x^60j_zZ4D?;FvB=O;_Nm6lm>(a!y=71)!!QN1SZj?V4?(LA+@m?Oubh)r6lKbGr&A&?IyDD2*%tLqh(8(p^nBOio2ArQC#T93EO-WIg1KLe@La>d*3!ngY*~08=pyOr&J*=a%g2%bcsd<K}uSownOVvr3$@>b_^IgB-pHNBN+wrke1&@lqarzpF#s22)7^F9_D4AX?vQcVocR-rzm1uH}7h0k|5o`mna0WNI`dtC+xDG?^nf(NoW+Z%X%+i5}??_K1TWy*ci`nvONIWbe$Ivl6d}-B3mlB^%cgjU24T_Qm6(Vp9~)#a2yUBO!`ZbV>-NG$WGUgEg$iOy6=*ifm;?<t(~v<e?*%a;3tHlb2y+O1;+6eQvzcN?~?xj{xmXT#aU$JZdFuoHRCRJ+$Qy$IF1ef!L6%phV3fH71-4*z&F{!H_sE#sTbcpw3_>Jc1X(pM1}_SVFB$fSNAs`wV)5NKB`vM<^;hN&aA_c_#NG^|`E_DJ6LvY>GLs1zycg=CCUirJe`b@V)Dbgf!)0rF=%=pl~L^u88$#`m*)G<V<s6$P!M#z)0#cvtqi1>sR#UIVJ|r0(#%6UiW=v?z3~f<9!xltgJt3B)4U)8URkM7AHC=?5JyzM5|8CUTdTOzzHX*YHPPCd+tL}N~Q_B1!MLNubpKBGjZ@pLbb8|&r;8xA6XAd`HlA7h!$$Gcuy;PAUX-LKLqarr62diiE>&@W1toH6l7~qp54@g*x#2&HJVF`F_w>O(6i|SI9uq+==2ON9kjozh45nQSzb*P&WS%_=2&NbVv5?!D^VwA3IJ0o(C%z-@h|18vpg9aSLdkKjrhUqh9Otrw`;Lb;RpYBa#%M@75nmkU$PSO')))
_PROXY=make_agent({0:_DEMO})
def recent_style_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
recent_style_proxy.telemetry=_PROXY.chassis.diagnostics
agent=recent_style_proxy
