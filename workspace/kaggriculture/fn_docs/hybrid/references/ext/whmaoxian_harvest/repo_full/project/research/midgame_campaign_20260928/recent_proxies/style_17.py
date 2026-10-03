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
_DEMO=json.loads(zlib.decompress(base64.b85decode('c-qxn!H!!=a{L#a`=BOUtsdXB8t#m+nrT7Om{<>l#R6W#fU!P|eKY*;?ol_%$Cr^2ky*uF`LtZNhVNBXR#j$XWaO{^^WxwB`rF_C_S=hp`t`+!H=jPe_;U5)-~alb|N37KUp##L`(J<ikH7u*!{=XL{P^zU?%}WAhd=!C=fAx9`Q1-%-oLnd@%DcI;_5nl{prWu?!)2_A3olH|I6FY4}aPJxO?;PzpuZ1`QNMM3x2x)<@1lrH#~jy@b>TC{^^$wtKa?k{^R=3r?-j!#d5@}XCHoP@$A!&^H2NTr_V3GoX_T`-TU{akzTJydVIB~f3P`w@Z%4HXMCN>ckjRd%fnKB{^e;c;^S8j`~KtohiqgY-oJUfODFX-`>V&+Ci3l@r&m3Gh@*(#JpB-P6tEZc?%%)r;d~CC{=`=-vGQyo4`#P`mpCL~qzeOoT8h)(9K(8g%}=}C_YYtHw0nR5GkVR{Z!g|5n;o)TB~yR;k;M}qUgqb|$Cv&6_jhleo_&1c@f%<T_FAbENljWjah99(&F9_6{A4P8c|IML<<92(X)VQB#*WN|5k8Ld{I!hPi|-KEoxas_%+LzZOJsM=CfgBWZI8PGoXIm5?y5PL$JdFI8jqbn{{HJDYYEQu_}s;Y2q)R;OhIRwcYvKe4lWkBE}=CYe(dqPhG{=N5$>;OF{ck=`ioWpR^@nXu7=1gdDiPV8~)5jRxfz8Qg?akci`C*l?ffcJ6=kY*AJKxxP(ui!fB~qWYae!Vn6Xunbi^3Z5@l8na1Pa*jMD2-`>A}zkB=nFMr&9{QU0yyMH;K;(E;ET_?=PCZFO8>PLaqB4-ZspB7V8xjOj_Cx1`BW~Za}_t|M%kBe$=o()KjgGYa-4Zn7RFSDHS+&(_{_+jA?$<aNX<I51^aiSL=E_DZiU?a|T@+BQ3oaF7uB<CLQM#Bpv+7Y2aT%F^+yLJ<mi))0(aXlgyP&fdHAB-+;5a-JuJWWFS%c-$``uy?D{tvs4AOAe$1jH#iEW_df)(K~VTI+C!O&IZ6z>H}O2i<1tjYyo1se_mH_jDf8qjG(G*CsRm-s(fir(&Me$j@aTCb?xGcK*gZwZ~`nK;7bg8NJ>S9$WHfTIWQ(X4VkE6~VbD+%rd4qvgCM|DfiZ!h0Q@6ILeSeD(c%k@<4^bdJk-{9)qM89`cDuj9Q790X!^+%FSW!%`I<IQrw8kN@nC+KSv#e9>Ak>waD@RM+>4C~0)+jx%I>O%<pu%^5M*p)|ypC|hS|TKHbU58y6~Hi(mjE`EJ!w%}Y?9Mu=_cnJ=Nh6uJ;KW?1lp@Y>Ss8|y=?7S<3gwf=#Z=;g$3w{O|lk_vu&8Zws>y0n=!_3iRp6u50WDA#u%SM1d9Pjr0=LBS<qkiRDN^npHrs0qarx^5Aif$eOx6+)`w&lbaJ}$V&k8afR*i>UQpD$qFXelw9-#HABw{rOEI9&O|@%Tzi4#X+PaXhYd2~q|p;_;>Hao<M8oY(5?j~-e%<{Y5JOml1Eb_Zcd@IiI{nLDF-n1wQk8ER*u%f{o6i@6-3IiVxNmSZH#OBQwQ&kN5Gep2@YVL~z5-DN>wcE_V@EU?_Bz76yAXoC8g@Nw4`8VDzWUr$e+`@1Ym5QqJCDuO!bcM_b`#ww$Cr7_7)(t*H*qxq3Yf`Q&3bIqh<T)#R<){lh!&VWgVFG7X>u-d*SVD6CvVH8{k?rKaR#t$8DHA6!|d{c5zp_fz-#}aq-%6Bu^=?2(gFc;c*$BLW9vjd|i1vu1>mjiI{=3cW5-HkX;%Is?nSOAhk?kmGN5@R~O!U*VrX7CiH_?7~0V(jn3gp){7jPG0Eq1n?)|KT`mz`6qp5NaHNk8IFaUaaAHe!fXdFesEx(td4FH_yPNoQHP~xSbRU<v!athKtggI&d!02Mz)<z?{OK^1ZW%qvLx6)Mg;*+-Ea@Hh~f?2S0sa6^}xZi0Kn=inH#6tHdcT%{2pBd(U7u0m*pJdxr8hkK>DOf9;VVKm%2PWuO=vEpQij!o>2%8gF9JF^*HSM(y1_$_N>;gm5_nyzZnt+~_5^1<ozn34x)D%oAGX%QFhQ0R|>;BMZMAF~EK~xvrgQQhbQD#D^>@l~<|q5)m})x~>d?Lv#_BAO7;_C^OFzz5}pS>ETgV(}h>z+eEB~UB4t-R;^*e21VhWc+8#%fp`Yvt&mpjVr=~W{^5Uai+&AAq(+x6M=)CW)H?0@!~OlIo#G2gf5{JQjw`o(FmM^9zcL5QCiP0uvG>?dP8_hX7hc<4%%vs}NVKZQ?C9J3Fz*4C<FHFjN}*$HAP7^Y0d4G%t6hG_lYfP%D%)xUi%WtM#P+7HOUX884#KujZ;wSDZb}uf*X-GhHQRe?MvTLzq88CLI(t*eMM4*uGoYD<NvhPPW#*~Pe9WX$YHWjnh>%=KMlo&$NS}N*tjYMtEt2vku3&{TOJQCj6@hkvJfHxCj+o$qk~cTsLK6uo0o%x&5(@hiy8Te~qdb_<C&t+set(d45yug*9}tnnu|Hl>m!5oin8ef+u(oJK@temhYwCEwra)(Yej2P^5mx5`3)95{^v!@pa6V2fS7?-24+=j%w?asrZB~3;0Nar2M(VZ?=(<F>#?r3Xjug3;5%o<$VU3nUpQelurc8|DvT7)xG8IoN;CApdSgFn=E2a?hh1{t@`JX(^nI%@8Iq`EkjTIxs0X`|uSre=*V^2bvpwn3{1*n4h6yULU2ruAg5U(-yX6I#c0FRwHyR8&zo`V@4ni4Q#u>JZ?Cm_(BV-<oEG=H^Yu*L;;j%QL}x8!-<%`gQGRdRuNr&4y~aS%8$-ai(=tZL{0ImJxX)TjieFc>=dBITo%7tcs3jZ*xAoJGldb&}AGbGXwO){uP;#4p34&7O)WK<B)c;Vo!hcgFxz<=_GnqroI($z7aLDC8&F^I}_-s9pJta5a8<_x?|dB(i?-xNS};t2b-8=Hu(pWb4V5x^QTu15_G|S_Le7s{%!>h2}=Jqu8yg((F{Mnd5g%usA$Y80HZyh-)of0a7~_X&?nobj;sruOz3^YC)>x#$I%wm>z_apqHKp#@`X_7zR~NY0ODCMf>1yOAD8U6hQLEpYMNq^Z9-_$qe|ldC~)^xXYBSIXb&t#{$2%@h`I|C#_;vnSH+j2Fiz_IFjr0jc$lmSBT8wvRXc7Y)<ON$o<FqzsUQX%xVC8AucHv3!^~H;dh^AdEO9^lntX%uq2d-ObPZervXWHTPdN*Je-)+bc?(oH&CG^M0~>)OaX5hmWW4lalu{^yoCb+KM+ee-Am7*YDaexZ~x*P8tW6F*da_@Ma0JVM4K7mme8ezY-)`>__tv|2V9;v6Yw1lF?=^zPjJIEeUp>>(nt?2odG^HlOT{GZVZ(P#*_Ir9T*~S)sx~?XixFP$PBmuU6s3>u!Z&{N+=+H&>3s}hJhm7q^?W8HBgnI?g6sA0=#b3XE0m<x%R5?L<Cl;v%v%+BvC_vvX&IHEN<AgB_Ao#mS)HlY+DoxvWyd4_%t6)I%9Th6#NXj&J}zUeH&TC-_T{(Ho8mcD9}kk2N=g>7*ZyjFOP%3yhJj*bik$lsFcnt&jmK=Op<yxza*%jZq5ixLd(_|`XwVqRx=Lnw=+$xbvGXnn5D4ybB~FJSK$1VhMKW}U4emW2V7Q=&MCe0E>qxny9Gc^f6L<l=5AIqHca3(26~iRE?Lt>5rJrGDD;BpFO7r*=G%L19?}z)RaFtxeMc&!o?m^sI<-emVmbtrB!(a^^6ytg8dK4W>zB_DU(oJn4*TQ+#QTSNs2tOZUt*5O;<%qF<`n~Ch!ipLQ=_{A{F{lp+*Aej8E-Um8I|+4Ts(qLJhB(I#zDFKL3Iyt_r+)veuK-D3IZEUx%0{y%@Eb6pyLM-FpC3VKx&p7`vm*vEUN2D&sxc9psaQ^G|N{#81*blPOM&_-T)X3`b3eJwhWu3=|q*3NOR+EPYkLovnosI(ZhlDl;QJU=j$EvVpS17L(w_1hJbrTmW(uDNf)A*|5xx+q|tzpfTIrVZFXNB#?llwW^lh6A-I$&*Rrx0lUPl<gxnBbAc?Xr@wLz|d&o$^%Yl@LC9TcSA>CAQCV7q7Ho(oPb~%8KSni@5#InQ?sRgvl!zt;2UVJ@a3ubAkQ>nunME)8ZX`S-6<YF&;qNi_mKm71?myT{jH%n#mLQQzkX-Pf~W|6+IQDPxINWI()yTiXOpNqa8S0Y)6*tnIZV0_6QOUFU;uvUXEYG<tb#1cZya-!@T;t~X#SJMzGL$wL{)BP{g8mqO-tqdEZSoI7eVA#+qB#2HY2JRNzz_ETkaUH>Z(u~_I&a|{ReY(GlD(M7MWMY_LP}JTa{0useqzNT-?(1h*o`fvWQ~Xjc4qJ}vWI<TgvFu{KQ;ZgkV#V-KW!Egr9Aga$UHS!-lv>2@=qxlCR{HiSDFq3rZr=;o0SsU23R`3bXjd&2CCf~_+09b!ZOH$+B2Vv>|5y48txwfn!!%@&tH4z{b*(ndU+?j4lO=C57-YsI2{C)1Q^6M4`R8e6t{Fz<fGvO+6ahOw4myUB5)k|FPbH*rvuQrgLl5w|tO~R4+5<kKMt+?J>~cViM!SlXHBJVRx7+eOUVfh%y@x}!#7^8g8HT~<yp>wh*Pw-x*2yF)kUOUdVk_)l2nNigq#WV(Pe1N<A6$Q&iKm=L`^TS6GjfECP5^)t3@HmF+<{LKo&*ssoD0n)NX6-HbYqm$Vp?Et%_6j*$PLQ5{~iOs`=Q!sLLQ)TnxM(?8Cj+N<rHvchTkSSBC7Pd%OXaY_D)7z8{cUzQ8b=h$zPGw<toT|pvXz4G}_eEg8XzrS_i8l``e6(4acZG+Dcq}Ga5|ZeL42k(;7C!1U?gJ378Jt)iMUcs|bJV_);*tasECv{`GNrprHw-8Dm4o-H&E2LmYZHKC7lW9P2dN0~<R{wv%~YuM#pZz}<|Co91v_{$^YS7+%C6bhT2*VnnqdTyEN6{%M8qZi;fac1b#E+=_xZaFpj+LS*_9ZzZ)vJaa8m_w3ylm&=(|QMM~`{|M;Xjr_<xN+Vc&F4@~d)rh2#w%wJM;@K=ahYCn(2=8p{XfUPwmO>v5q={@{&;AuVqew$pqIVc$V23pz{}@GsF7H8xxD?qpK}&RI=haFKK)&jp1PJ6@9|>TOBxf3QU??%QSvAJeA1oa!*CVTJq`9B+>$7r$I)un74)R0_JO!X&i*8zr=92Y8K{vel@9hT4h4B2F;?(#!n*0*>0I&CKpv0OA!-mvDM5Y2&+mYj`QWmzgdz_<Nz`de?wl9d<!VT>Hy8xa;FRoq^M=HC1PmVUz#t#xC^@G*Ns0pUv*dpSEck0TjrVyHfeKM^SpRLhs7VHZd`-;re1GA`mJ+)&SA)r8_2}H106ux@IS)whNUM%$Wj9w@^!-X?z5iAW(H;%5P)_v?3EIf-nA^P1?u_{G4(OoQ>1uGIVBm#(vXA&%`R$c<dNKW6ipdO1UZ+qQl3;-a3tgVoGeWI7`!%WM&P_;;C%8g|69{N%_jF05#4JQ}8sg^NRj$u=E1%$x>O+XLQP|FggxEtUw+2(`Na*2Lk*!5gMdKSQfh4obR2rp$C*WqD^idiYZ%GML-*6v1Jxr$xvx317Dn@=!oB=UwZ*h|EEv&%ug7r5*-gtEO9>S3}){4Xh1&__J33uEH+kLYDXc7ZtM?D7jn721~MTSz4j_|W9=P+_Td<JHmn9#4?X*FTL{Z&ME!CI_Yai@-B*N77d1PqwnGOxSd?q`p3a!=tRICp7xfzy;*@2~U3v*Qw>|wWXd)EK3K8DxGG>HXvfId7;4=NfnG+aGZFhpcF&u66T~DvFAPKXy~|eSUJ!=EpqK#C{ikdL5_r30W;UpRAXWk3AQLGx7VOInt}*f?BQ-m842F?m0lNzFecGh1)jNz+4(Qm9B9Edk+dJ^t7ahEoB~kKk?CcB3e^ol6HptZ@ROa+xXfT*M{Sc{>5p{;6ZN#5Jvj?GqJXn6&bSUTuGwDb^CrLv5f#lC`GF~lS!ipqHFYF4m`N1?$q|Z(^l`SJWu4V|iqtw~f$Q;~g6M*kmW|5wUR0I$+H1WGLvf$c5jZEza7mxObNAK<F=*93t7od9&G~3Ylw)#s+@oeQtaFmM)Tz-3lxrc5UJYxY8s*aW<Jc3(_N$jrhzR9z6Y<4yS}*nyj8Finb}HOTp$84kROYba3n=j;yQ()Tj)WevyWd57fs_e4TDFzkFN78Vb9NF;Yv>*cgO=X3&I~C7(Gf%)wW&muz~kxF$q-xy@fNTp@C+?D(R~NdhG@z@pv<H3VwYC0h*CkFn*Rb`&J;rnAUV$LW?CLp1r(lYh&a-`D(ca=uACS)2*21Pdj;A;#xM_CYf6x)^|XlsU%vhX{|at6mEf$<A@WAIMi&Cd&#+s?%j&u__j?JjjB=2qeCr7G-RKZBAkgE1EKZXkPH>oTE#y1LYR6|*vcWS&?y;MZ;x4b-Uirdq@gNxzLyK+52aZbSSi+Oy*XwY8-Apa9x!ycujg9ERI#yv*f|{>iU81apu)Apvzz<)WjiWi)Bsxi$>JZQXaSWA#jheHe6M`dUA<dO&FibeROppRneuPJiujorMUz(H(@dBZ&`equj1ad-r*;CohNY!?Y7U6&-WjtN@9HUQ#t=A~02a$cO8+US#UIps8Gg6GG7*j;U#x!0`Ifh>B;-o)G!H7HyM1vjbMK<b;PR+FmAj8oOCw7?7>ckd_*EBT&&C=*l8i*lNULsXx;GN56tg<@_<SHdpk)Lb~$0KZ-Qa4cM<4b;;QWWXXzUa*W_ZV`ii+Wgvz9$9Y;=~BVcC*BcGHXy`m$#F;xOl~7gs8%S%Vswnij;Vw7mS9Pc4K=E@LZ=&)INY$rO_UxDs+Pmxp@f;^MbMZ4O56@)fM{uAPHcJ1(A%xAFBagebdq-MPS5Nm>g6dnIbWg6k;Kw%I5Ou$ntU9bfj98WGh5TWNsH0iuk&%#gKD~atXV43#{0kRXjCC!9=b?b}bmxfmGaN1Y)t(P71xfNzrZtYRRZbg0f}YvkGp}+-G7WJ~vFKOhAIL@bh&hhT2=Kf10url>t}EJ!L5rfHae=uo?SFJEqA_(%Z`JkkTP!)RI)b-jc7@VYB{CV2j6rn_{jo9_$qrf6(YdSFiN+Q(O=w!NCt|!De1sAKI)<jYCji4Z&c;Wo-Smu1&32(94F)D3G6wOqurrDkBs6ib3#)vTAyeLE1w^)r^2)#9iQrvyWt$4JgET`K2I@wfAmHFly1%32(Xy{mH9<LvjMK<)fNBUZv$cj0(IJJ3Y+`cX6eA5Pgqwg{}#5)bbWlc$M@2rgn$0`XcjO;!_U(gVDMruvp(EV9?#Az#zYv34{v}iFBJck5ON|HlxcIJi<Xr%|ZR0l6&s&AO7e1bwL3KM$G_=Iuo3&XvlXoa_l~qj|0B_(ko2DZj47+0=2R%BSYT)Mqk6~87h>|Vgo-kpS4g|-FS$gEv$KGIn8ILH+*yj9s(*JP26hc{#GIi39ATf3N)!jnC%cntB1T9)?I*~kLyLreaN?{fSyDQh|e#NsMYLO#Z?$Ji%B|)?jX$3t~4$qMhqIoEV@;#{7ITyhMRdd>mxRgVwjt7jPk2|+vAs=Weo8lUJcDyr=ay)Z?tHx)Kq}gE6fp+lX8b@O^mi|wpe#U0x7hq1UyO~c;|iC;9bYrK~6U(YMX_I+Gej~2H5aGzb3FHuLD9qK{D>D{1xwoNJjLIg5xGeh|;Dly-Qoq1Bbn8U4~zvaQwNoSK`>VPj#A4%n!WkUWb>s3?DpLq})=ka9iDl%gSk?Y!^Y8VCZqPfn7It215ayoG9p3b5%DBSqo6b_4Q!br0ue2vYT#Zw<tICc{H2)=KmAV$?il>h}I?p3evy=C#_rcL{hV72KchVTqB~ye#%*)JHv2ULB3$07hh2oo^~7c7URjWHJkC|Rt$AWI5>hbsutYB0EPVVD7+v>F{B8p?o-z6rJ9_IP;O0uhA~0*JF{Mgi)~JmeIoU?5gk1w0}FkDeNJW9&<SmUoUJIOT<P>`$;lQ>#a42U30ZdZa*>sirQqN}-BAr<3s=kzCO&!)63qnKRgk`>X8cUs4m0&g6yVEC3t1Nxukp^(r$2<kH)EATT<-p`n^<X<wo|6UQ)2;eYLRzP(FQk%0gpE_W>lX_Qy{m$4dush^E!m>Z82|-hGu9*_PxN>$kmk7v+nw|gFPu0_BfOLSeRgHjB;6)y;|tPlDiZxWffa-mD0!^WOt@Zz1&6(w7XR-)~>ER2AHy^gO&FAs-3#=q|G*RthYl-(5js{t95)tyKccn_&UPnxAU<s0BC&o4=UvA^%M80CnM4Jl)Ao1=8&kC-^;qIpJG<$@sho!m~^E<Qn$GlE7pr4FH$<PW|-yNn?+V$H2a)W+XkoHDy)J`4l6IB%>7P3Hb~uJUAM~o>5i$eQZ+yb(pp$PO|#c?+=jYcxQ6lM)Bmo~XUi?jGnIlR;X<gM>?VmnPy)lQ@PTvW+v;Pi-7jF;mHWX|{d=U-7fd>tl=J_02t{D%QmK~M=+pP{S=9e6D9bx4F}je9GDU#rdzWT^ha(q^a$Bq^T|w!^(P}Gi3qs4hW)I_hem?OWm!1kD?XBlh92{i{4Mb%Q<SGz>eapS)7+H$o<iOG9r8%5%Y8c%y%woxS8lKZudv(K*Zr;!b;;n!{+c42vzO!{T*eDW<N2qI;`os!4%{Iqq_My^|1N~cx*gI6*bD^A;Vv|1nD+SW)2auYWWs9^Y{Al~7RmpdD;a-;YblorH>$9P@sxw)#8K#%|k*HC&R~HoobLy<NdF!z{v5V9UPV32jIN*l6msKZ9L9km@ImlQd#Bt^lp6eg&^-v<fSQprnpxFpV>Zy9w+?S-@hnS`C+jxqTGsMSb#VQ=GPMqA9NFx<$40K4xgPj5v^U$Kg-u95TN;PE7-YLT{51~5JM$T@%pw1u9&@Xo7wM<!;Lc^A>WU7*X61+b;!6T$IG%*Q5!FH`18mjaFFX-npO%?u0^xp6Vat=Fh3$nIb_cF4(mI(ndv~7j10uXs=RWCg()5rVIt`wPDYYC`>j9sj{fmy(+v0zbVn{#%JFwl`Kvyh#d9~4JY>uJwVTB__MS`V!D(xyEiUVRS^sx08j;FrUa$<p5oyuJ}E&{4D4qD$FI*qGB4AI&;WDV;KaU}f4b@FvYgg<zFF@x2&r$S|d-CLX23!79c7Ogj&GXSTD;aZPDzmi2AF9dK(ik?54;ScSq67BdHl@Zr%qj3-uUT|Dh<z-E!Y$ufr{dgYuEB|`8{6Rf73`wU$XQY;sp7e*$KxMfuDXtrEu$lKutd~#rum+moR92Ik83)N++&6cc@4n42B3`ws$>yd;8J0A?4VdSKgP%y76s+m2|Y@ch*DXCW;5&<Wjn6J?%nn(7wp%Z0%J|ItSInl}o)n)@>u-he6kj79jNQDO1x!);r(P|s{eKZR#0u^z^1FYIj%66hWK*|6n6|@aWdt<9z4H>J7;Pen;aUG&@F78~)<#C8&H!+@YlKHB?oc-FYpa>qUefSA9hs;X*1ZP%^PO-)~AT?ls7BPkb8?2x$&8U+acX<VF!!Fzm?n26(q28QEunt27i%zYaOva;B{OtssP6MZh*UxKs@!PX2WERdvtMtRJ<P*<Z<>t*?YBg}KOT=&G7~kt|P!)FbjlaPPOjD04>me0;(ly0V#k+CwFOQTKQ9hcptClrZV%j!fcd<r-X4~SyFQaLUF<Z>R_0+WD%jUfVee5Rm1vI6!ZsuUEj>eXXMp!!j^72~h?V@A}=b7v({F(xntkf%e&)Kp*KWUWm7)j0vT0sCAySJcw(Kfm~G)*dRHOQ_=1u9WW%WzGynr@abpfxy5zrvx5`Gh8vQjXBA-H0Z4RHoa!(paTc7yU*zRk?Y!6cBuC2wDlmK<MRL+t=)E1T<mA%h@EqCJ%tduU1W6p>1y{qSP{6W?;X;5-DQmSRJ-Z!XgL^X{N`O*FAHx*EN<7jVqU!!`~}x-pSLgDPhwvCsIzv9g}RdwAboI=)O$+U4-!*F0xhPC{g9>=Gjh1s{tF&5q(g3vvqK=_c~QB(Xbo0M<u~v*=w_ZPTA81RT5xRpveh)OE<+qfXjklhk0FsSC3SzBo-p<)XKyXR&4TM#>6rwel3+iNzFHF;q{wprYK7p?NTNh5*0ww@?MeTa}mpKzd@a>jX@t9!KG~W*c4SP#b_t3*D82GfU7P?3!{#D3s<^oiYZ-EGD|ce)9TmL6|*KnO8o*qMwpVC^Lajxl}TXKX5l*w*Yyb<tX)ahG4DgtB2+oHLM&So)OoQ(-5$DT2<)8iL8r^S9V-vuF#9?+wo~o}viw?@x|y$!2O|ynjW!F6@091hYyLe5$SI=BO0qoNYC8o#QgkMBRy@pCHJ$V%aOLLQl0gDiIN*yZj;uQJxgy+WUUHNFgBAz$-wc6#sEk_f4!p-w2YdAkWqgJ;3(HPn@Y+xX#4W=WSWQ#Y#1popTzeu<#5)AbP4y}uxZA#b3lT-6mHsB1J!%?~I<`m3)kx<AQY2RIF=*AUuJKWJ_r7xV$%4oXg+ADOitV<~LrmFM1?Yw)o)C2<Ihw`pTX0s8o+_e4?KRJfoX62}y;P1_;Yg-Bpz<eOS#Ur$UVe4B*P=ksBWR^gPVY2@XqZ{7S;~5)PKb?`J#We7Om0^RM3b!2wvv30(d9!5wXY$$>pF`QXSPF>C=C^M{1(YtS~{?c^ub@APT-<Goqee-f9~z>xJ6!dD?V*X7I&5@U1&ztYLA=c^*7Y=nM0&LpMB-dv2M6GP&J8>FQK=X%1Wf~t$OPziWpZo1jtMd11XkaGRct|B~xoXG7yX7OI<C5Dw5ZAsZ$uaZI<jf31m;Lg;Pr=SGGv{j=xa6umutxtwQ8&yPp++oaiZ}m9A-t*50c)MgW=$GHA;Z&_#g~earn!RMw!k6v&f}Cp%@53GkxKciawv(N3NVMf#*U8Ui-GHfb`(J)mYSOXJXm$$^ABOa-*4unO~7Jd;CUYl7Ehml30E>0}LsUfJy+@@(cMl`-X+gYeyY?l)hWeP3)=HdrR@;4P@cD`9O?l=ZreEEl_WKyToH@MOF(L)<N?`=bfbJ3Q!cEnOvbT_eXMYscsos%A21rp!KfH^wPt$9v@ZAE3nlEz-@NMU;$`L&}<o2DWA(WKE9QM$|ZpWRAkE`gL4oeKD)BG1IRtbVE!Xy$aK#sv2)+oJwkA?GX_iN*9c-svEP^nP5`55#=C)=~O!6{Iu!N8WIdfDXB-1)U9GI-SA->VTC);#R_^g8U3NEAHMxE5y1o+{t>hyp1ca2FH}nkESsX1vhJXLtk?yl;XF5vJwdWSYnH^?HF{iL(JD?rms?<J*sQdtF5|v}h||^l);S5KD&-Ncv=G><Bo=u!1mUpeB~+w`QQ73>snDs4(~_-*B&AVWimE&A-akyn$5E~4o;|pE<>nrfFWOG14rJm5f$zjBPlSOj0i3&D*(n3TVM|5R8zV<Yts5gs-t4RfBUFL&unM-4V5f8tKweC29sx_HhMHLw@Mz+%G=`iQJpi}FZL>4u74#q1`hy>C8pMj*cA(}c&;?5#V>Lkp!B8EgBiu!+INBK2_08omte2DMUz-}JWdSN4kk#ON(eN-_00y3rOMT6ybdib}<1Gt<AeUlzNvMp_bqbs{M}=@Ymy2E=g`yc6<S9v_Q2<Vb_j{A*W3I(`GejZz4NiR?E9AbgR*2PY=nL?Wv7s3nR}qBGarx3FK`^(FW~XkGDxhM5SdM~M8Dq~M=hqtRxZbJHta?_jn_Md@u||V)rN`HVk7)N_NDF2`9;Hv%1#4aIN>V^qq9(gtQ5{9AEC;*ZnUw-O6Z;hlMo9+^EQH#XN2&9Ro-ClXbm?jE8HV+AJkAb)WoHFp9?o0ZIW#|~hpi0JZZ&e71lE+?Zguw6>hg<9;;$h{sY26^nrY3~N-sX-`x%>)AhnzdZ5^IFGe?vc*#N2%wRr6I>GI3#n~FxB#ab+>_^@l5ynRMiBtm8d$$F}U09M8)Oi0+ck>M~Z5Sj8;+D9sHAPI<Nm9~&~Smj?-C_bGToP`Fu<t)%<M;;7pXbyj&hrPU%R9LL4mDH^S?3pGJX33)!gP3@hyFD<q@CDfB<9b=TeV-OO(lQ>cD#4N$RM1b^&#Y*i=5(sx_jQMq+helmDzSZIJ#xb$ab(fHS^`5RONgaz(X7h`+`?az8S)HsQvQo4FC*LHR77$p^~d(NydDv<8@<6Z;S39ICc96CVmMa<{BU)BXE0(MRtq)j+(7cJ(k&AK6X)5dj@fJ2m=Nj8s_$5iLQS~c*)6eB<(p98iYt^twA-ZroNcyH>~vQvxUtJ)tace?s~{{>rWNI+LDO4=2Ei{uSaG9sw$v07+m3IVg8+qw62w42_?Y+~Q7K9r4bpN(OdsIM7h3hDgF77IXG@sU28a}vbdDmsoR71>-e0Q>Y4LlLp_I2jp=XkWPr0F_eDspEDLZ;h1od?Q8eX|DKn%2%-KuyYLM4!zXrigN8uVGDGI9zLeN&c{GH@Po2%QoiSBc)Z^4$$y5>mT=CJlE};SH^TcU~xQ_Q6*)TVv*R_T4_*1@U)_Bh`?U*|$owSU0cEYq8+3QB%Knl6_TYUU#>XqO^9c6FqGV<pSH7R8wrU4?2`yLmI!(xTh)x))uXxOk~=rn_S$db-a=&4hVi#8KTJ2+m0^1bM8thO##d(>6u>a1s5G0VWO=PO_H<NtE0Y4O^P*XF1!c{4McyEQZ%ZRe($vNAAg-DH$dP80)66k9*p~S6)B0YpjQY^qp<Mk`rU#E@wRua!~ikQKaBazJd-!~*W2O|=)n3@^+NZxSeM1^w|WoM-YupR!KQ#0gssqhW9U^AheMXk<|D9K%3bon@kz0S<@l$p;vf$^>3^ZiS6;>zgHg=t`ZWkQ&l2`u*X|WKEr2%iW&;0W?gt_mPh#pX{|Dix_>}')))
_PROXY=make_agent({0:_DEMO})
def recent_style_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
recent_style_proxy.telemetry=_PROXY.chassis.diagnostics
agent=recent_style_proxy
