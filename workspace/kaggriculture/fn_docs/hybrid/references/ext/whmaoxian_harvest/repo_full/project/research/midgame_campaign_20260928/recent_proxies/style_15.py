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
_DEMO=json.loads(zlib.decompress(base64.b85decode('c-rk<%Z?mJcKsKwdtt-e%<NiJ&WKQtNHi%I#)2RS@E8V+@nY<q;eR(rU7eMg_r$s9#ygANHTqFq6&Z2kKF;H(|9SIozy9s7fBD;+-~aUHvV8jd=I4hu|NiTL{_B5z`No$o|N86S{^KwI{pIVQ-hA`ppMQD$;r*W;pWZyYdH3P+=HVZIeyH^A@7_NzZ}1npzxedsvV1)L4gQUv|My}0*?#!&{Q0}>hx_Tx$M^5P|MBDDRrxn>@A&vFyH+2cKYaV+yU$;K<?`L~_<6Gcck>f}jlcQv{nNL<e0==$`N!+iS{Ls6DsTV(&DXzt-Glqp{IonhZT{^)yuPDP%ku4)@Be9e`tZZ%jf&qEHptWCyXCMIu4iQP#q|&E2Dtvi>)ZaP!~0mjeRv;V{^<|<<wslgwh{mE_m|tfA+|LS|LpSkd3oM{=;Nb!Ko1do=A69%cE@$eHwSJ19r7<<SMK)UH~;*$I{rf?|6_UFhe-4p)+b^gWzNTe8{zssHeb9xO5sD$r~d8phmXPrPo2qVWSQ!94(s&k!;k(Re)o9Wy69=|w`9p8&b(A4dV)K18~P*rb~zrtb&syQ_O_8vwf1>;1vtpJc(4h0W?x?aFtpaUm0h>|?b*Hj+uUe|-s0`wZEht0ZQB(&Zm`6XTn{^WZ4eG#zqP$W)_-UIOYF7RSG@g`$Vz|{x$ceI>m0UA=;mABVDfci9~eFH^`-sCW8WZnU$?b%-{HFtPfyFc&%gX(dH($V>HWX#_tid_kox823ws)Vi;bJte)!$*ewWx=Xkpl;ynWUDP}M#dYFCSmMED*ti8*?J+0UCk1t}vY2MGS_UBr!j6lHs%GjR+#{dd>#gV-m%`3Sc3VISb|($_!67o7JzUeb-g^2AEjy2oW*CXgGL^$o4qnh4lee)&;eGMC)GsK%o$gLV(2S^DTM`t7(n`LrLBuFntc6_8Nd8?$W|-D`>MPP`?!$Bc2iIarWv{-!~CM-y}svE05|q|d@~Ou17gB=w8=H|P;%L?K>_+!oZoVR$Wad?D$;(yTeUStDH`Qbgt^KVT^W**<u;w}nJsWpo!nZ;dso>(vj3SGvYxvi-%&&n;8B_l-yvknFVchV7|alYu5o@T+@WBCl#or1D@-f!&q7ux4Ei(gV?pO?tRyYfq2cIh(7+b{J0?m)y;SKJx8*-#tG6^OCwT%je^T`@+3bN!7XiWS}tG{y5&3gW!g~w=e)b@J2M~b{~_aDeFYPh`KB!=i5H$_4BUZ{CcvGb&+;Q-fk0?&!6wYVA&Wb6>iJ0hKxuD<ysSe`uzNO`DS^3{xf(-x8<i}89TI2pJbt{41+|v+{gb8Errkuu<bAqff$&94&{PRLmSfCCfjW})^;1I;$w4L&>=uCv@Xo+56ve_@8~K`B-Ri>?H1dT^P3K=#h)C3Ci*8i%~Y@<QL30VFs2O^6Oz;KB({}~0iDfWq&5z^fk9&k?F|!N0=*r73oEUXNb>|Xc0lJD7ab00GFrq2D<K<2wPC9Y?5s0U90Ta7(5<(NDL?MQCM0jNx%1G#7PH|h@tSs~yM716oUD#HEn{fXQht<ZOPPIAKU~`-CKWBck=E_E{lmj>5mr4#Fa*@*J&dnl36@i8?+FPkxtjr8X;9xzMgyKwDyW!_PVBB$AY1r{%Kia`CmR~s+4YR|XZD2wVSuDHbBrd#;jf2}c&tj{{M|m~6x3w&K>i4Kb_SCcxop8S#qEMwn{3A?w*Amf?sM#_6fuSR_0VK)3NFU&p|;=QSgsSma>|->77qZTNOFPMj*M)yN$(CiwBm5u0D{71peQHd8A}9FO93{lLy^8fGut5`=Rw!?p^25r2S}sYA6S+!u07Hd8(yh_GN4;B1j-NFQj9CTT|avnwe3;RHW%$tgo4)ku|Rh|-5#j>0XL0r{J8@E9>fy%5p9B9ekOR#2VpFy-61|MJqTNj0K|OQCIxA{u<5vW*mplCJ&nxRA<VewG?KL`_{7+W&ZWJAbXrZ568vYO_kbZW>CR#%HB%b!-lBDgwV5hvY09&nu>d0ww1^*%9BXu*kN-836A2RD_22TQW8j~FXW;F(yrm;uh4geayTr-NA87lXj`#ZE#3;@jtSQJ$Q2lrkmVa%MChUYI^MFjSKB@BNsfmh;qo%`TAAsLd>!|Uzt%eR}DIVY^p(W3ls@^HZn>CJTRxi~mJvP-;|3N37NA@K{)y0?smGAD>XF*$KLec`w<*X+lca0`mKVcY@BYuFx>^UZ9IrRdCjPfz}eb0UL4P_^;U{Px#1~QIUFKQ31YRHUnjbv`C>;Hj%3<Yd%1}SH(op+ml;`G-C*tg2K#qM7}VM#4cxJio^wQXn+C;^HRA6&R&m<TOl#$KB0u-BkWQRHPZM2wRct_hCp1pJ^NTUI>QDq~J8*ershJ4-RJjW{H)59ugVVpDo(@-?*Cq6!zNfn1Y$+#*4$v!B3mObh4u^OHHNIgqNb6d8Q$Fz+fZLwZ$Y3|&T%66q6BH#MtE9OpPW@G+~2&vk$Jk*mT23RPV6EHWD<N8Qp@!7^O?4cC{wj$EjQTB|3VTOpR;lC5Tu`9n!Xm;ge5TFe~_Nc=6!oB(LUYl*XAH=Tfe`0%t{k*CKWuKnen>3};qIY93p@`nVPvCLsr^7caR?sDoHDq)+A)gwY-4sb&j6!WK5Emo~0ME8mhD(Kq54*(@9Z}j2HuVkc7(YkzIyAq7Pv$G-lMc@dO=4v(j%T5(gBf;^X-u}Pj$ee7GLr2U;tSpMFh*qPOat7jIZA3*1myeKChUqzD(bub?)_Zx|+8Bs!-zMXn<#oc`wdfNEYQ$;)6i@yxLGZ0N>ut>4U>G|Vz7#$P;dsI@?mPbm&P2rsDYsWHBy%z2Na>X#%^s3ifKbd-^lO}$jje>63E6iZ=E}6#K9(;M;FD={L~){+ryvIvd>lalKlfpPv8IoWf0g#wNYS)%-2hm#1fiaaYz>khf+#$u(^b2XI~_ELQiyPt$_|{+-=a{8Ok+be<V4495lu46)1pc;Z5%23b(eiWHBS`c-U!V#3FoI?aECSK=9B6*(P*MI1>2iwIa`Sm`|?B%j5;hTx4kNxH9vwLfn0fYNf()Zw^8R8+Xus_vI=KVa`rUO!f7h`DvIt>bizqDoJkJDO@p1_;8(%%ZI7m|72Ru~X3N7O=%g^EXZC1%V-iGyCke<X^#Z%lLeFEA&68l8OYlClcmO3})FFOOzP#sW$Vw0Z^IKdSx&$15<`JCej>vWk(A6r_v6zi^6d4h7J1Po6zBh}whI`PNucxe*zoH#Ui7ud{n%4F?Pb@=NMye=JA<T!wcerkID-1A*Q-0Z->?EITnMz_5MS%-8ToY-6_lrv)^ni9VV^oww(EBa|Q&pi7bf+<tEpo6Fz~;&J=L`x9oujqD&X7%0&ZK|lN-6Zl=5w#`ik8u58k&q~cjzPsRp>PK2mSe7JrR02_uGa`8v^7)bz1gVvOQlrL+Lu)s6>AQs2Azx<0RYq)BC6IPor0qMS!^>nR0;T_#WQwZOI$xxXdeAXiBy$f<^#zkH;vo&>Ld^v0b6i-W-7NT$|BHB!<(h*1#%2#XuK;wH0e@h}2SNrjk2*@@4D~BI~b9;}K8T^=w!facc};={Y1eX5m27Ivt}*#&{oZ-xxqkCKlOBY}?h!;vLEh0)D^Rx3d~kXhHF!*!C|-7Px4*wIi1V5V?s$`jkhxQtjl~9B<1&AQ6Fu0ELPks&yiBA5EWxxfmlSg%wO*Kql_#P^?FG151q|ZE5I3O?I0=+3jKPj}o_&Lexx|35pO7OHlyyJd$BI<~W&9m_+N$U$R!t?joldDKw)aOhK;TAc3P%c`)3p<5M*o0G^Cs@JS7B(PpnDmETR@YY}M82+;x3Q^OX8cg<k~hM1x0U|1iksJ>#>6@AOp*;3iqi=G6DzSZD={kyms!qGg%L6dv?L-ZQ5lwH5$T!*h7hy~2pi;Hp6r8RkfYZQ7}x!*DaagsDKSwMFZUwAJ5Ykz27t%a^aGYGqsnB~V72IO!MlBhsA*T|+k;~>BX>6eO;d+l{Vx+w73f7^7_@6Vq-I+@$!<f35WH-~GNr-C~fW&*P#<bMQmnshrz>H(ipL?nmI>rg#7Ez@?+?9e%)gIH;<)|QOR)Q$tpQ4Pa>wiLU(!S0gdC?hqgK)rL(sOjs~ZDFeR?|dpQO@}Fu#m<s?^MR&vqzhPM5&ARv4i{l6Zf|r@C(O;A^(irJd$?&?9s{JXZB)5a7YqoF?<%<Qz~mUk3GtbABILKXgKE;O0+ewpM8SIel=$U)9gXg6w4w65mm*C)XwxH@7xyzM8~7k{jk8Gu$<0^z^)T<?N|*^`h3xCEdYokQySXMw=Rlg+@XE+GG`E0c({h8P88j>M+RHYoay=o{z^hcAqEa69(0S6x7h7aRqgBLX?`;e??)IF7p<n}#oLc$Id{`=u@DqR9PRV<IgJ})_u1YkfcX{jLx&H&n6Wd_g^AwN~Gw&Ro50r=*-VS*B+%M9`l<v4nJ{9eC)S5MbM7j~%y3Xn^mE7&RoK@*y3R&vJW_8t9G;wN~^&h3)i;T&MND6h=(=@kdn8;IsF2=>8zom1)&rr(cFC~D&=drv?zL*m|U;JMJtG`8<@LMhH&R4}%?tJ}>UWVE(y9hl*C};s@Dcj#WW5nv)a%TC}E12|!N^Tr(dCw%GaA7AlT-O57-OtjahFCc;+IBnCB7q%XBRfgoPcD~48-vu;9ASY063<F-uD^8nQ8#Uoq4v}M`ooaGB^S~2aqkqwEbewDW<gDqiS4+7iUuVxdj}_uYs1__Ee_5ARkGtl3XA-Gy}w_m+2#V5lx428ZcSQd98#)I3k|I>%sb&;4jPgUSMuyJ7$TnP8(8W#a&WrRUOa01cWE!c9q*StB>x1I^Sa!pxvE>WVBc_HH@YIVAwNJJgO@meMDOG)OO=5na+Jc{dvK`nkwcLtRZd2Ft&7s2&xg;q(OqL(?gHI16k(=6N`VHT`an1bQ!VivuIAaIjt7==7K3nKRlc$MsLGS1DtB|`!Dh&gfL6mCGD9EBX`)MT^V0f=#%ykO8r$PD2Z(I7J%$WbPd@((aDVa_KK_BUiSKec6Y-a1x<~4RWErS+E>1+5Q;uE&65u6iiVvb37KutVnFhg9(NvfcSJqlA(XZfSub558`Mn5c)Thv#))So}biU9Y(uFC4gppo9$zDvR9!jCdH!_)KH&NI&Z7pI}pMOVTTw4Et*;XQ<NX0<5FFCK12$8gjsWMh_5naUTDf^q5kVBpVEfQKG^qY=hSijlpz-|KtF-Bclt-1v`0uf=eX5;a;gYyWKN-LBC2)XSX%%Y}7Nnun~a_LbZa5z?Wy+vT7R%{?$hjcqM6F^Q%2Kcm+V~j2v!FK1$KYHzY(<9JBZc~Fd^VY>rX#bge!w!b|379~pwFwH>E;QF6j?W*REe$Y1jzw>-qfUFebF(NTN=WkwuLZm%hdf^an;_6dr7rFiZHTg}ZG<{B_+%Jd4eiF>D-5<ZZ*Yl(N-ynk^I4|C`8A9SILz6(4iv*n@JR262;+hd={o3=q%4l7ZCCV&GE`-uv1qJ_<EJx7@bG{Q6zv1)DCds2&#K@-&VUSnV%0~c66<FbWy><h5!Xh$Ne|LuEDBW;!RWPy7A~R)x`u%WASaZfaCLQnCa8_Dvkjo5;oO(qY=mbXyu6AO%lmeO3)IAja7IAKkzafJK+&#W7?NEy`&HyFz4DW`Yi>wN8f)yZ<aOFc4Q#7Gzd4`b+yX0MQ)f|8Oc?&V4hW>{(|Ar$LstdFQrrkd0QSYX6u%a=g4Csm2Q_-zLE}{l-GBZ+Lw1IrK0iNRzFD51|2&tzlyK=0LL@S!k?5-7aB(Vml!E33lXDa8X(IEjj2#ZHtJB4%>;@_h@(yT-%@R<n_2id8?2f+1$1iE#^9S)EII~BvwoVzOHn(Tyu$pzuUtf_9=7yBlzuvtkd;w!Qkfjcudiq{eo;W7Gd?`!<uD0{EG-5|kE}}|v0PTFK!iRZghCCeMU+>-&6>jcZ)(<I&!J>q0qBQdzin=p5^$a0>K6hvvY_R4YL?$|NDwKZ71~>J4I)l%{g&L`<5)L5U;hl6~E-KA(K;kdX&8onJS^(MM4Ujb<^VEcbs<B9ED@k=VIp3L@J=E-+fqs0kM0g1U&9TcUglAtB2oTjNyoXadboBE%xblAY7nYq)3CeFk)ILwBq2{#`*<XbkmXY50>#;NcG5Lf2QAU@befPF+!X|8oPg9umc{R19p;(}%l9&w6Ln&zMTB6I&QA(<FT$%J1gh}U3v?lKSQwAhxFnHN3NI|)rM;N$K!ydh+n`%&jTRQwG(}|cI4%XwV6H2l;kJv;&Wa)wZKCnfcWlZ8mrjqXw@ByeF;l$ljdSbY7J{~Jtjw)abf5Q@{R3PhiDbh#!&pqjKX6-6Ti;YkCKqp?_jHBsn9h#3hd*5x0fYc7?UjUYLZPTiGrc1dwh|q+R%<e@UT5bw{5}uppv_=?!0Us5l>jEIW&E>ylz%XS=#s(m{TobaEL04bnl#JQ3r*98Z6Dq9ck*y+5_2-8GC@r?6<EqUGiE^xmS6W|gmZ0222*l3aV7}m9i@aN8jjnj8zHdw~YJE_!1jsp5p@gtuX)D>wCZ_IHMwsd0j7!MygL?1XJ-g%w9dV-E8nvT&+mG`=W5T4}mbe&WA>=V^pC^Y)tWnMVH|mkVo5YS@_o<H-qIB?>aN1n`lzvre{953{2F-tlcf!_a2A*}LJ9jGSAePpsFd-*xw_2{Xox~at#<h6OIQJ4*LUn6cv`BpqK7(LKriA51-%Z&luW9Mn(xcjzYA^-E^FxYfoe1$%bxS!*A>>#k&OxsB=~Px(og9r>_N2j&WaZ}O@S+w;D#Km?2MBEj$W6xTiEdTbF3GWSsErFK_jbr)wc;(W&@UyWhU*V@0dKz&4ILZ2VfVVdcU`rVG6#(eKK&1kz(Z1_16>@7(g<B`&i+Z-6FZVl+)<gE>kAh^5a2#rKyd;*JsBc;8ngMD4I-RB25fl<VL15czJggyUV0=#>;nhJJ7?XYsUw($#r!nN`-Wg_(Ph!SqeODxG;O@d90rbnHRBXf;Da!Gri=eQT89C88gCZRdpLB{MCA@zE5UXiU*uVmdE#0;=xl$pe0tCwwbQ_nCSze$amh8vdAzz7GqpaOxkoRFkwZlgtY|PH_mq3URi;D{;ZZY(wcy{Rt`mvNd%6%l7JExCYzN@N|AdR0r~mKC{J|?l9tj&NMVWCR+^+UlG_ZJ$B3+R5wby!mAJ;Z3Q46Tn>6;)71=Y9Y2_U7(iKTD;ojO9UNd;JF+A8=q<l)%qE|4HIIk3E#u^si3^umlU>JU%++R8Ij_90Yjn~M|=RK9&3BfOz*wuPRx0Q$Pf0yqUX*?j63PzcF*67dX`AAR{sN)DH+7;}uHplb3gmqog1GH;)@zPUC3SLnx~v1wb~h$gxTE6iZ~vESw+6w<F}e_dX#<bho|PYfaw-44-Jm4!F#lBB^SxK>KPl$GNH4TJQb50<sbYLdY12TQ~wJu{?AJOwaysE$xn5=86a0&)>}PM)O2pe=pA{+6!3o%TP~nqyxDD}eJoK@k;`unnkM3?Gb7=%r}uV7K20Nke<?2MAA8A~ACcK0iRM-C<gnm^aWEW(`CrNa5+qd6@H2BvmrD%cZ#2DshTx297Z+88Kb*F62bWQC&)wDY@#^;sfmMTK%(2T39639iHaw=bT(R>!sX&b<CMP*B>^j)H>v@U_P@;Ov%X#)Ad<Y@8-*`0~ZbD=A}tFC%b$`2=b+<(9S&BQw}C@qdPTobr~MADtMw)aX@ou{4_pEo)k3~6ao=l<POW7X5&cpeSymQ!(^I(?((Oi5O-Xmc4i`oV<g*>`hTvcF@_SNG7N6Qa{-CC8$xDvf~ylNR2zt}OAyx^xFg^5(#(ajF7Qyz$6%x#cGBt{cd+fNU4)4M5yK+0IbOrSJUie#U%<#MZ7IM>H7Gj~fvdY!NEL640N6txt7b}kpbxpnX!!ab?9Vb5EUQUNfEkW+Q%-lnn@DB(x%O3DD!sNHE*}6%V*qwaRSiEl2qAfaB=!&?y$_NMPKQ=tr+XmKS6oj$W}kZxJqUO_K<C-+dLUVJ;VE$P)n-2uJ-Dk3SRlu9taI;N#4z5?Xa+O%OeC@O=8JIaF2r7|s*``tdxVKB(ph2xQze`#k7_tERH`#mP(LS(nh#(&ixST6${wW$bB0eub)^gYoMxBRsqJzA7Ti4x%*Fs!71!c%TjL(N%13p=7*A=^I;83`P~-u9?XJvA<uc7JQ8(OJv+v8ISnGL`ADAbeIt7jgg}3|d54zi}j}~9&YW{K0r-a}XcMLw|A@OG#iv%qOU!~gUlJfNkVVq`0?ZTpp?r)CF0tVf~xFg1xp^i+|)O$s@4?5rh7qA3bF85cNtoym9e`?FXyDhm6tOHDJvU8is{iT2@*Xbc__Oo=GUugWNp;iLf#nUc*Ky01PqeN|1CNYqWb*|DR>x;z)BX_E>qQzQ%Wm2A0CIY21P(tvcW_wQ5P2v<}QRKdjL3Niv3zijZHcbW3(RQ}>PyJY3Ba9kjRcq4fq&En}9mu+rWLOshk&3v`2Wo6d8XsjgFcG~J!S99q4sD(Q9vk!d6xX?Vx>DU;sp!ri*-3y@uNf%vUdS03!ns`%Z(8l%tbitDw?FyftP5Uw-pxlu+z6F6xNr@N9_#%9oxwCB_tNCTb-KZoTG_swp|1%BatWS^0FhLb!mN1<oSCy2fWA_-(M7T>_CU8^JrpXA9`J7OFkdbakj@8$a#4V^iw4q4nh1H4-6tQxHA+(LL&0l?&Hxh#%n|s$KYhSlaE&^FzATC^iTrB0y6M@{zVkuL0y2%{UUq=6w1w^ZP~AJs6;1wG`4!*Z_{v?!v8U8H6Gz}=f~bC_8N1{CKHr#o4F3TQ|8W+t_bT}Qj;MCEMwd?8!(c=eRp(2bziaHUxgqyj%mMI84)0jX7f>?sY7vIgY0wm0cz+a-<h@640v^H|^4~jR8VZS_EWgpcka#!(Ak{NV4HRVd!PJM=TcX#XAmx6KI5ncoW=Djo2V*=@ZRji8HC_;1Rz@$Q7D9l|jP~RFqA+<qmvbwU<j&O`7n%%seVOA<5pZOe*rk36m<v!4Cy7&x&p)lBr7I%3Fv<XmAfoim{k5!EU>2Q%1q8LKE<s=Oe)UI{-7l;%%JM9bW`)$l-mHj*YAeDrwbQph|6@aItGN!5wBQdCWzq=A^|p^gl7nL5pOq{UDV243PlKuNG2Ia9*ty0=x?gIzwYa%HR#5Ssu;sVwatrnl%?C;-Chq&12JBWW+KOz~1sHe`P-*YVwR@*R?cWs4R_|JF88r?$Z*$F-Y?4GZC?t8bQmf%+t^7vz?#x{WW<pL^EX{^1+VpyMGnDmRFqq=NV^2oYna_e7X2R2uoy$8Q_<~U>R@CS%%GAF}2_gkk7{)40@Bf%iHZ5puBSrf6KWyDPpE4^9^$++hDGI#PPJMM!xD$lyOt7=>ltQI4c4nymrSvVguYQd2)dG58od(>bTxr+o+fY0K>3o(qcP8jF92U|B48D=+_4*q7J!KW5vC<p?oI$I!Cwx71ekUE~7vlHaE{xZli3zvOL?P~`$HpVF1ioIsaI5_mF5Oc+lt@&8*|k%VCjBk;r{p!i1c~NYN!v2@M^?z~3chRn^-3eS*so3Z>-*ZNC46o8>Dw0l@ZssV9a>FJqy(su!ZCmo<@mHZDk1jsCw`H=4jx3lfBIekxVYcT&a1>Fy~cFMk1yR=0ph`2k~@lksWEJ7uGUq|9?2j_G2;cLqRQ0Fm|IV=fnT5OeXD7`up9ogUVU|TxjG`rQA!Y){S8>*JzMkMU2h}3mi2?Sram?2QRr@bFI+@Cv8M2cO3t@>N937V_guEoiy&yv`#tN3&`1VFuzXP`hOX&X0!(-Gn}GVa5^mMkp`PQK@}y}tDFrFpnE;YseYk49HgoWXWw-*_nyNhb56w|34Riqojllv_R7?;Mz=M!Aj!XJE{e=-CU?#e+J=-(4GSvi+=fE-zcjZdjMWM7O)h?#sk@GQ5<mNqQH*Gu8*G{uK$)adhYI)&m6x8=F8-*)zgEue#@kNLUSsO89s0*_Hc0)vn-lVG0tc=8Rv_D_By&bd!t^cO1N(0rpsBz>;<WUKx<8GY<I3201BbSi6eh_=$R1EXNeQGMoQieZQbXgRIsUVEDt1VbDZlHl~7nq4TY8SOJ6SGTST7VU}qB-`SD&Gh7SE@P9HM)@yM4@PhIy2p*H0+4;KC;q^;vqClQhz7}!ZqA*&)|nSf&`3)-30vr;SJ6P6hRLGB(fUhckNSzDIu-9wlYr@;SgcHBEMt{u>{;fV|7yE=v$>`dzzvcB&9#nOqF>=?S<!BB8J?2a;;<B$l`I{<jpP$GX56+&*R!&p-u&BxwbeYHJ=EcVXpG1C0s`>^J6C<F%+AjrPS}@2*`VDj-K3}mZUjN5SuOOErre*ygmvHv7A}Wy@H_DBKEgy=2*irdcy&DkdmN-4c5@WChJ-}B^#HuxlkOp>}GW)({6g$l2q7W=%S1lsTq|BSxSiMNHg@2^6^c??)_viGOB>-2p{`$N@BzH%FQJk4n*8$01MWswLjh|&QRlcVBC;Dri$z#s#&6_Kou=y8P0L47ju((*yN4cH-HCJY{oF^LB#nB(dHli7S1~xm_^l+y=vlCM74w5_J=0la{M3X#y7=M4LaqdD0M!uYt+~7JQMYmD43);_Lb)3rftu<L0`J33R}bf6;h*F8{K?ffa?_xG(4<!??oP<QWBeWc%39};m>b{d43pwRTZw%&3>Cjj&*}lAx#SY+Xs#iakS+{)lD;{5HA7FXJ_Sz!?BTd4;)_)B<`&VMTjA*6@0>3Hrm6bh98$4;)fM$2?8gMm3&Km?fO5-o;qWJdJ0c*sgs_|y$BR)&Z=)d$Dl|nI%~s|pDctC9fHm*itTklJR_Z(9<~`t2#dNQdK|UO?nY&!%9KtaL5Yp=U9b&Xjjjb8(8)c`IIc!yq3e}}u1F!ZWb2C%KdPYy?qp<4jv2U3AkxT|ROhjme9BCc(=`E(o?jc4Brs|d_6F*KNUAxY6C$VEDRyPB2m%zPM(N2#8|Ut61)Q?+jj9|bjZU7>gm@j#Yhzp!B+X$l4i)*P-s+WL1t6w+Q<O^AcBr$!_pAy<qJnT@dozg)$k1tGOKUn5l`7&)WCj=qvbo?Pvs8?{GJB`<2u@TtSXg3MRL;LgqO3uImAlUuz1D;?X_RN-+YHAyUG8S3mJ1LojQpBP7HlRk5zouQTunjKXlT}+B?fg{3qL31^DKrJ^|}Ez+qBQ>6!u0j07uYF1;k$o+;Jj^oXe$n-6@<g%X)xb9aF^nuQ5(N7vfMP27$3AwA%x}r{>ZHJn=p}AVH=Zqq^e!syuk?bixaT!YT<!R+1Fx^g5tm&DmUjk0pV~;iv+jNI?Q@nc~hJK&*G*6kZOJkF8j9lqP@+s{Y}jF@nLI6cY}F$t2Mt$u8Z-EgaLuP#Qzq;{~!^UWXOWPa}|+0Jxy$UDGYB7Qxwq$IA^tnv1tcJ*Zrt)&_HzHz~7D2U;mu8wi>)b_|;}(P-v|o-FPGq}6vEAhZJ>X82D@5B?k~!G(R7GC*EHWGkRY<)p+_It=4Pi@<(#N{aQM6Jd-p+nN))L-;WzA&`uG9DJNn+I|TjNL#eLYB#Nsst}hk1EUzoQ?e@!#c)gSs_C34YwusHT@j<nIt`u*H(wR4n~_mt8zPdCBdjUM(>);j+No1MC&38>BEFO!Faq$Im=nr5G>dy^i+~tJA-jNd<}_ER>C$EC;nER|S%q|)T*-NPfJ`M66l!H1ckSA&q}tgIx?Y!*USi@wNY)2}Alm$3lpaRiOsKAeccFuM*QsAHJyjT=Giqu0N5Ye9bt@)MH5$}jQ>eRC&0eBT$^clQLM$9f%Ne8>n>1h|#S_J$?S8%n1kvQM8dqWq8kpDPA-4~X>5a64inCn!UE9%FFCv0LD}1Yct6gg#JsHMy=%DG~hXOD}NGiN*jAa5;K7&2jj3A86;U$gF%@i)Qa8gg_B2fIVtDFXIxB*+iVI-c%x`5lied}6N>%wfQa<xtYT9=|y(2>aOk&&Cy9nitia=9^cOO0c9J$KuoJF>!Ea#-i0EC^KwH(7y0+L~Xr_Ui5w8@XSY+#1KM(9~X+BxyEwf2i4htJ}S_Et`O6fSn4$mQ9Xp(h#Z0uFyL+tW7xoYLa=04x2?BR0{r0dNXyYN3O^*>yYiAfsblJxlk6)Wsp3G*D(~cKDV7%Nqc^bcv?KJ;sNyTZR3@9ct#jLm@B<I=R6th*EHJiz{cDzy8|$EfzG(^Roz8lkhH6-vBfVS$&fs8J4LeTdP=W3U8?zTM%Q8iEAgsY-HX5<V?)$R!W3r_*ox{Ph~^0b`FT{7IVmGr+Pn{3x;?;$JdxUvQk1JQ+^#o{jEDhwX7M<AWSg)sZg>kT`aGpQa^}-$ZPH!L(Gn63LwHie>@}vul-IlrB2YPTKo2fP?>ww3UN7H!HRS5;7f>FPVrZXK2ZJbl#y5JyojgmbC&GbHKc8lHsovfWC}fS~D5<A<zMXf_X@ALJGkG6L^L%Ouw{PTGSS^HRZ8z(O<JgB}(C7!FQO}`E!SW8vrhh?|y-j^j)5z}b@DUcFXagq+8M~)(_PV8Hw$RIPDT4r`A~WAcR&xZrBN<7dOT!6Y=So#-TY3i0h8J4Esjy1q=tbIawPv<Cmo5RYp3ZPRn7nsaC?AP9p=fgcl`nqd^tN)n=I@IP4HDNxMhZDwo{)`4?xn4nQ5F^ciRg^93jwd=L%uXkTEPoU;~71g9v`z+OVOyUu-Z!@v2Txs27#obrqN+$oLRZ<l8g=FVQCz?wKKD_+?)BhVuiP~=*N}lo)yfg$c0m&N>>!HLm5}y7{i#oiaIJq?N+_7`*iur9!2Du1rdVIIJT`~*5JP^LEkjD#XL*DUSXkoTa8(66<gh(eIR1J5hzju?BKK}chbJKx>R!I1K$uH<7!sZyxNgB<ApBcyH8^%H(dTNr{M;10h;ia=x4XNjqi&mynih>`inOxr=7;e;o*F|gD}+KkuamX&{~svL@5lhxvt`2jp=~F5sXd5De3^M;a3ZFq^eBKu4xRx3rny|p&N;Q-5yfV*vh2aEj`^q^CE=?kqr3L<43|nx<l0JB3Wq%KadJUa09-pb}4lw2XnD^w-|=E2&zWx*+b~ZVa*9-ER@UXZeadlj&Ds^MnGKLGFKJ#Z28>QQ*Wy>L~T|#Uec6%-kL5IcP}IyPuRDvrLZ3c5Gk4-Dnoe&<nxGXJm3Tc*P144G&hVWw2m`5XyvV)$ByBnFrGNG0A(dBX5-flK+H0fjLIYh(G3(wAVnqPoraUIP9RLF@`1O7N0__Fao@-Iq4J{0Nnnh_>F}|Cn3V^vh}6TdV?KFQ9cPI&4E_Bu1S(V*=&D^J1Cgmv7=!eE1Hv6nml2I+nPHs;Csk^`k94Ik)$$Ps9ePE=?(_yX#lWcH4@te7*`}BTJt_8g??AZ+i9^$}DS;EFvmXx{H+(!+)<WP{8bhx@w@NO)1Hp351^Nbv0ysfnNqgitjW48fUdO7d-@wog)}70R)hh8~a-)3y+bm7)>+YuwJvD6ts0Es}asrUJ;%Ug0$ct@VwACIXveXl#n|6{weUGWoV;#gn)eJs5<;`P)q!>LS)hacltU((b*-NN$(NkDtiWQJjKZL*hayPXX125g`85I%FG%XbdO2xSMmS*db5?YjRw2?UBOh|{;lu7MY-`XR+=Zj`8O)#gG@N=V~6`5nUw421mNH3UQx#22)Yhk{11r_sw82goM==)LWW#BWCG{(aZDlN(&O83k6x!3=gRZFp+^UX~H=6Y*vm&9C8zJ=d}lEniV=z8Ciy04^E*V^Ndhfjr_#s{XQakSCv`cn6;N-VTlMQtS$^OUTg17uNz7H7q1bvol7PB=9M;4fT|dImDnE?!L4B1sOmkeQ!&Wbcri_Ka31t+is@uCHH~rOG(29pZTd6}KsyPsIC-Bz%h+Rq`B+C9`J{r-3pQ^x}NMR`flFbj$C?k4drnR#6mU<%c0I$cx*luB*$eg;0g*QbI}2N&|7axw4-@zhy4QW&L5PV%~&hcST|JB;C6T%(!|VTG*mXS_;usOX3dXmj?K-K2if2Xb^RJ!EU8GmEnk!2!=s;pG1&daQnI5Fmt4oR3HJ=SX6-vFO*cE&DsuYacb!W9Gh+>tU+-KlX+%4FJoYXQvW>+WW9ZBCE;@)mQJ{#78x_xXQ2GxBXCEmfaE1X@dnFu_GfN$b{)YT<7h3pxD4(Xo_E2V$0!J9ITqFG`r2qk&N+nP{UvfIB~9@FVAQk4ik6K1p+cYBI93gFSP-g*2533%_r}hFA!jytBOn_ff-|O;1}F%*0ofa_Jp^P)%=6)bF^<gQ*auOYP(dw}a(yspzt?5vzGMq0T=cwgMM_{{C*m*o?=ZjgHiL_^VO}oY5Q7!(aTJGCSj~jpXs0rQ(sqtaP032>A~7h8oMB{F&{!ejI%tDtlZwX#l}WwNS(Nu$r~5NtDYCl9{C(L-NQkcsbv0+k#U8psLgmh@om$mCp5s*Ll?i7klKtZ7d#*vkml|lIa4fbMXZ9_xe%hsV@O|MDId%uZfw38ymKzWSNh;fL>?n3t!*9wp0;f8LFf;fOz*?XatGV1>igg~Hvr1vz3Z7~1VmAY{otSc}PzJ{hC+UsR$yB|{U@vORrszT+Ss1MmGSk`SrCS-e$DIO=q>p}syv09Gs(nS=oeQi^zP4%as7+nX82>}a)7Vb1;i-6ZKAEs+J3llruCZDe+!Hste`UzlR8}q$me5Yo$rlziLQQ=Ipv`<r9(jvvsp@=AZ{J1RY5nWldx2uVO+-O=+Qo4y<oEjX@GDK;YitgAP@gkar|z<YZS?x}_3Yiwt^_djq7&WfVCdmWp*cIv!>U%_Y+Z8>2M^C9U%GcRk0@&0Yi^xba`0(b6fDLIosWyv!4=Er7Qq&QQ@ox=ucFclTSq*<pMFtHxRzE16N6T>P)iVS3LUIJDzLTCLL7&X`BsObqafr6m7(im=qp(}r12z3;taPur)9<^K%I3P7(oL<U{OpADf9-=5qc!fGU<{VH7ZKI69FzFY<%V<5NMkhyKXiL)5FKFPP1OCPN)xGPc`-itX8J>d<o0uy48nW!NdEx_Cq&s2k`2+9Sz5LF)u}DJW%W_+IA{KOyE={bQ^nkFJpX4KB)ggn_P@1Qo(j-b{;Y#({e`_MRO@9V;a?3&C0CVS|w1epkKX4&EVLepD;5UB71V;9-aO8=_7EnGb*=JYS!%nO<xD(i!vd(sRddo54i3aF~?{fj8v#%L;n1*Zkp3x^t)b)<k_{+$pl?_w=;aQq^KL(_(E);z)crAC3B*UM==f*TOSTjfb~Sv@#RT4rZLD6pFOcWPb4{>Mwhy`rkS_&;;@ySi1WC4I+|~&W>dQQ{*)vbG5Sa^jzZVqk|vEwN^(N-0mbuhlltC>T#?ul?c+45bDLSf3oJ1H^yWD=xl9@5_;eHvH*Tcvd(NtG@hpszJKh3pLXBt=(e<&(qHty|6LewvG9(I@TGu?2ycTA!-kY=~^X^Pf0u$!iIP^5eD|X<<1)zh8jL&v(9Rx`qM0I}%9O!cgm==`fWCkZD1B`LahA0BK!}OGgs_)4TMk-!C$kr`;^pw{~u6W^7mt4;$gNZ7`jDW3SGay2Pi-S(6BKZ#vjCf!ebiA)Huqeyv@uvVEH>t=iwGD%$*-1w`Su1Q;kTt=-eg8-AmQc+WBL*%#LR^^`qBf9uT|TWKs*Q$jw84J<KLILsN&')))
_PROXY=make_agent({0:_DEMO})
def recent_style_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
recent_style_proxy.telemetry=_PROXY.chassis.diagnostics
agent=recent_style_proxy
