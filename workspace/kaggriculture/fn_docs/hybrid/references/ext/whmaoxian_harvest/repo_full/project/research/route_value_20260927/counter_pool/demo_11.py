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

_DEMO=[{'farmer': ['PASS'], 'hands': [], 'market': [['BUY_PRODUCT', 'WHEAT', 5], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['PICKUP', 'COW', 1], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['BUY_ANIMAL', 'COW', 1], ['BUY_ANIMAL', 'SHEEP', 3], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['BUILD_PASTURE'], 'hands': [['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'COW', 1], ['PICKUP', 'SHEEP', 1]], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'COW'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['BUILD_PASTURE']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['BUILD_PASTURE'], ['WEST'], ['NORTH'], ['PLACE', 'SHEEP']], 'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLACE', 'SHEEP'], ['BUILD_PASTURE'], ['PASS'], ['CARE']], 'market': [['BUY_PRODUCT', 'WHEAT', 1], ['BUY_SEED', 'MELON', 2]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['PLACE', 'SHEEP'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['WEST'], ['BUILD_PASTURE'], ['WEST']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 1], ['NORTH'], ['PLACE', 'COW'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PLANT', 'MELON'], ['NORTH'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['PLANT', 'MELON'], ['NORTH']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['PLANT', 'MELON'], 'hands': [['FEED'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 2]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['PLANT', 'MELON'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 5]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['WATER'], ['PLANT', 'MELON'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WEST'], ['PASS'], ['WEST'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PASS'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['EAST'], ['EAST'], ['PLACE', 'FERTILIZER', 1]], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['EAST'], 'hands': [['PLACE', 'FERTILIZER', 1], ['EAST'], ['PASS'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['PICKUP', 'WHEAT', 2], ['PLACE', 'FERTILIZER', 1], ['PASS'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'MELON', 1]]}, {'farmer': ['PASS'], 'hands': [['FEED'], ['PASS'], ['PASS'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 2], ['BUY_SEED', 'MELON', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['WEST'], ['PASS'], ['PASS'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['PASS'], ['PASS'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['PASS'], ['PASS'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PLANT', 'MELON'], ['PASS'], ['WEST'], ['PLANT', 'MELON']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WEST'], ['PASS'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PLANT', 'MELON'], ['PASS'], ['PASS'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PLANT', 'MELON']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['EAST'], ['PASS'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['PLANT', 'WHEAT'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['PASS'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WEST'], ['PASS'], ['WEST'], ['CARE'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['CARE'], ['CARE'], ['NORTH'], ['PASS'], ['NORTH'], ['WEST']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['NORTH'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['EAST'], ['WEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 2], ['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 1], ['PASS'], ['WEST'], ['WEST'], ['WEST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 4], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['PASS'], ['WEST'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['WEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['NORTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['PASS'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WEST'], ['PASS'], ['WATER'], ['PASS'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['PASS'], ['HARVEST'], ['PASS'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WEST'], ['PASS'], ['PASS'], ['PASS'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PLANT', 'STRAWBERRY']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['HARVEST'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['PASS'], ['PASS'], ['PASS'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PASS'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['PLACE', 'FERTILIZER', 1], ['EAST'], ['WEST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['SOUTH'], ['PICKUP', 'WHEAT', 4], ['EAST'], ['WEST'], ['WEST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['PLACE', 'FERTILIZER', 1], ['PLANT', 'STRAWBERRY'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['NORTH'], ['WEST'], ['WATER'], ['WEST'], ['PLANT', 'STRAWBERRY']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 2], ['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['FEED'], ['PASS'], ['WATER'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['HARVEST'], ['PLANT', 'STRAWBERRY'], ['WATER']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['WATER'], ['WEST'], ['PLANT', 'STRAWBERRY']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['NORTH'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['WATER'], ['PASS'], ['PLANT', 'STRAWBERRY'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['PASS'], ['WEST'], ['PASS'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [[]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['NORTH'], ['PLACE', 'FERTILIZER', 1]], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['NORTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['NORTH'], ['EAST'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['PASS']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WATER'], ['EAST'], ['PASS']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['PASS']], 'market': []}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['SOUTH'], ['WEST'], ['PASS'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 2], ['WATER'], ['PASS'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['FEED'], 'hands': [['PASS'], ['WATER'], ['WEST'], ['PASS']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WATER'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['SOUTH'], ['NORTH'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PASS'], ['SOUTH'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PASS'], ['PASS'], ['NORTH'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['SOUTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['SOUTH'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['BUY_PRODUCT', 'WHEAT', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['WEST'], ['PASS'], ['NORTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['PASS'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['PASS'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['CARE'], ['PLACE', 'FERTILIZER', 1], ['EAST'], ['PASS'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['PASS'], ['EAST'], ['PASS'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PASS'], 'hands': [['FEED'], ['PASS'], ['PLACE', 'FERTILIZER', 1], ['PASS'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['PASS'], ['PASS'], ['PASS'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PASS'], 'hands': [['COLLECT_FERTILIZER'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PLACE', 'FERTILIZER', 2], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['FEED'], ['PASS'], ['PASS'], ['PASS'], ['NORTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PASS'], ['PASS'], ['PASS'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['FEED'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 1], ['PICKUP', 'WHEAT', 1], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['HARVEST'], ['NORTH'], ['FEED'], ['NORTH'], ['WEST'], ['HARVEST'], ['WEST'], ['WEST']], 'market': [['SELL', 'WOOL', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['EAST'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['DROP'], ['WATER'], ['EAST']], 'market': [['SELL', 'WOOL', 6], ['BUY_LAND']]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['CARE'], ['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['WATER'], ['NORTH'], ['NORTH'], ['PLACE', 'FERTILIZER', 1]], 'market': [['SELL', 'WOOL', 6], ['BUY_SEED', 'STRAWBERRY', 8], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'COW', 1], ['COLLECT_FERTILIZER'], ['PASS'], ['PASS'], ['EAST'], ['NORTH'], ['WATER'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['EAST'], ['PASS'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['FEED'], 'hands': [['BUILD_PASTURE'], ['SOUTH'], ['PASS'], ['PICKUP', 'GOOSE', 1], ['PLANT', 'STRAWBERRY'], ['WATER'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PLACE', 'COW'], ['PLACE', 'FERTILIZER', 1], ['PASS'], ['EAST'], ['WATER'], ['EAST'], ['NORTH'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'GOOSE', 1], ['PASS'], ['PASS'], ['EAST'], ['EAST'], ['EAST'], ['WATER'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['PICKUP', 'GOOSE', 1], ['PICKUP', 'COW', 1], ['BUILD_COOP'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['WEST'], ['PASS']], 'market': [['BUY_SEED', 'STRAWBERRY', 1], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['EAST'], ['NORTH'], ['PLACE', 'GOOSE'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['PICKUP', 'GOOSE', 1]], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['BUILD_COOP'], ['EAST'], ['BUILD_PASTURE'], ['NORTH'], ['EAST'], ['WATER'], ['NORTH'], ['EAST']], 'market': [['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLACE', 'GOOSE'], ['EAST'], ['PLACE', 'COW'], ['EAST'], ['EAST'], ['EAST'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['BUILD_COOP'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['EAST'], ['NORTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['PLACE', 'GOOSE'], ['PICKUP', 'COW', 1], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['PLANT', 'STRAWBERRY'], ['EAST'], ['NORTH'], ['EAST'], ['NORTH'], ['WATER'], ['EAST'], ['BUILD_COOP']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['EAST'], ['NORTH'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['EAST'], ['PLACE', 'GOOSE']], 'market': []}, {'farmer': ['PASS'], 'hands': [['EAST'], ['NORTH'], ['BUILD_PASTURE'], ['NORTH'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['NORTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PLANT', 'STRAWBERRY'], ['SOUTH'], ['PLACE', 'COW'], ['PASS'], ['WEST'], ['WATER'], ['EAST'], ['NORTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['NORTH'], ['CARE'], ['PASS'], ['PLANT', 'STRAWBERRY'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['PLANT', 'STRAWBERRY']], 'market': []}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['CARE'], ['NORTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['PASS'], ['EAST'], ['COLLECT_FERTILIZER'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['CARE'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['WEST'], ['EAST'], ['PICKUP', 'WHEAT', 3], ['PASS']], 'market': []}, {'farmer': ['EAST'], 'hands': [['PLACE', 'FERTILIZER', 1], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['SOUTH'], ['WEST'], ['WEST'], ['WEST'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['EAST'], ['EAST'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['SOUTH'], ['PICKUP', 'WHEAT', 3], ['WATER'], ['PLACE', 'FERTILIZER', 1], ['FEED'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['PASS'], ['WEST'], ['PLACE', 'FERTILIZER', 1], ['FEED'], ['NORTH'], ['NORTH'], ['CARE'], ['PLACE', 'FERTILIZER', 1]], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['PICKUP', 'WHEAT', 3], ['PLACE', 'FERTILIZER', 1], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['PASS'], ['PASS'], ['WEST'], ['FEED'], ['EAST'], ['WEST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['EAST'], ['PICKUP', 'WHEAT', 1], ['WATER'], ['CARE'], ['WATER'], ['NORTH'], ['NORTH'], ['CARE']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['EAST'], ['EAST'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'STRAWBERRY'], ['NORTH'], ['WEST'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WATER'], ['FEED'], ['EAST'], ['NORTH'], ['FEED'], ['PASS'], ['WATER'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['EAST'], ['WATER'], ['EAST'], ['PASS'], ['WEST'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['PLANT', 'STRAWBERRY'], ['EAST'], ['EAST'], ['PASS'], ['EAST'], ['PASS'], ['WATER'], ['WATER'], ['PLANT', 'STRAWBERRY']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['EAST'], ['NORTH'], ['PASS'], ['SOUTH'], ['PASS'], ['WEST'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['SOUTH'], ['SOUTH'], ['EAST'], ['SOUTH'], ['PASS'], ['WEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['PASS'], ['NORTH'], ['NORTH'], ['EAST'], ['NORTH'], ['PASS'], ['WATER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WEST'], ['WEST'], ['EAST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 6], 'hands': [['CARE'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 6], ['BUY_PRODUCT', 'WHEAT', 13], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['FEED'], ['SOUTH'], ['EAST'], ['WEST'], ['EAST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['CARE'], ['SOUTH'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['DROP'], ['FEED'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['WATER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['DROP'], ['CARE'], ['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['NORTH'], ['EAST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 3], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['EAST'], ['FEED'], ['PASS'], ['WATER'], ['NORTH'], ['EAST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['PASS'], ['PASS'], ['WEST'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['PASS'], ['FEED'], ['NORTH'], ['EAST'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 2], 'hands': [['WATER'], ['PASS'], ['COLLECT_FERTILIZER'], ['PASS'], ['CARE'], ['WATER'], ['WATER'], ['EAST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['PASS'], ['EAST'], ['PASS'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['PLACE', 'FERTILIZER', 1], ['PASS'], ['FEED'], ['WATER'], ['WATER'], ['EAST'], ['EAST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['EAST'], ['PASS'], ['PASS'], ['PASS'], ['CARE'], ['SOUTH'], ['SOUTH'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PASS'], 'hands': [['EAST'], ['PASS'], ['PASS'], ['PASS'], ['EAST'], ['WATER'], ['HARVEST'], ['EAST'], ['EAST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['PASS'], ['EAST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['PASS'], ['EAST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['EAST'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['EAST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['PASS'], ['WEST'], ['PASS'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['PASS'], ['WEST'], ['PASS'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['PASS'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 3], ['BUY_ANIMAL', 'COW', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PICKUP', 'COW', 1], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['NORTH'], ['PASS']], 'market': [['BUY_PRODUCT', 'WHEAT', 3], ['HIRE'], ['HIRE']]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['PLACE', 'COW', 1], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH']], 'market': []}, {'farmer': ['PLACE', 'WOOL', 4], 'hands': [['EAST'], ['PICKUP', 'COW', 1], ['WEST'], ['EAST'], ['WEST'], ['WEST'], ['WEST'], ['NORTH'], ['CARE'], ['NORTH']], 'market': [['SELL', 'WOOL', 4], ['BUY_LAND']]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['DROP'], ['SOUTH'], ['FEED'], ['FEED'], ['WATER'], ['HARVEST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['CARE'], ['NORTH'], ['EAST'], ['WATER'], ['EAST'], ['PLACE', 'FERTILIZER', 1], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 1], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WEST'], ['FEED'], ['FEED'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 1], ['BUILD_PASTURE'], ['FEED'], ['NORTH'], ['NORTH'], ['DROP'], ['WATER'], ['CARE'], ['NORTH'], ['WATER']], 'market': [['SELL', 'WOOL', 4], ['BUY_SEED', 'WHEAT', 1], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['PLACE', 'COW'], ['CARE'], ['FEED'], ['WATER'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['WEST']], 'market': [['BUY_ANIMAL', 'GOOSE', 2]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'GOOSE', 1], ['PLANT', 'WHEAT'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WATER'], ['EAST'], ['FEED'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH'], ['PLACE', 'FERTILIZER', 1], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['BUILD_COOP'], ['SOUTH'], ['PLANT', 'WHEAT'], ['FEED'], ['WATER'], ['PICKUP', 'GOOSE', 1], ['PLANT', 'WHEAT'], ['NORTH'], ['FEED'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['PLACE', 'GOOSE'], ['PLANT', 'WHEAT'], ['WATER'], ['CARE'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['CARE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['PICKUP', 'GOOSE', 1], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 2], 'hands': [['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['BUILD_COOP'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PICKUP', 'GOOSE', 1], 'hands': [['WEST'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['WATER'], ['SOUTH'], ['PLACE', 'GOOSE'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['SOUTH'], 'hands': [['BUILD_COOP'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['PLACE', 'FERTILIZER', 2], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['SOUTH'], 'hands': [['PLACE', 'GOOSE'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['NORTH'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['NORTH'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['BUILD_COOP'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'GOOSE'], 'hands': [['WATER'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['SOUTH'], ['SOUTH'], ['PLANT', 'TOMATO'], ['EAST'], ['WEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['SOUTH'], ['EAST'], ['SOUTH'], ['WATER'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 5], ['BUY_PRODUCT', 'WHEAT', 8], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['WEST'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['CARE'], ['CARE'], ['EAST'], ['WEST'], ['FEED'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['EAST'], ['WEST']], 'market': [['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['CARE'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['EAST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['FEED'], ['HARVEST'], ['WATER'], ['NORTH'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['NORTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['SOUTH'], ['WEST'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['NORTH'], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['EAST'], ['WATER'], ['DROP'], ['SOUTH'], ['DROP'], ['WATER'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'MELON', 12], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_PRODUCT', 'WHEAT', 31]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['SOUTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['SOUTH']], 'market': [['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['EAST'], ['EAST'], ['WATER'], ['NORTH'], ['DROP'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['NORTH'], ['DROP'], ['WEST'], ['FEED'], ['PICKUP', 'GOOSE', 1], ['NORTH'], ['SOUTH'], ['EAST'], ['EAST']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['PICKUP', 'WHEAT', 4], ['WATER'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['DROP']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['EAST'], ['EAST'], ['PICKUP', 'GOOSE', 1]], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['FEED'], ['NORTH'], ['NORTH'], ['EAST'], ['FERTILIZE'], ['SOUTH']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['NORTH'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['SOUTH'], ['SOUTH'], ['CARE'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['DROP'], ['WATER'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['FEED'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['BUILD_COOP'], ['WATER'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['CARE'], ['WATER'], ['PLANT', 'WHEAT'], ['PLACE', 'GOOSE'], ['WEST'], ['SOUTH'], ['WATER'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WEST'], ['WATER'], ['NORTH'], ['WEST'], ['WEST'], ['WEST'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['WEST'], ['WEST'], ['CARE'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['SOUTH'], ['PASS'], ['WATER'], ['COLLECT_FERTILIZER'], ['PASS'], ['SOUTH']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'FERTILIZER', 14], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['CARE'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['EAST'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['PICKUP', 'WHEAT', 2]], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['FEED'], ['EAST'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['WEST'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST'], ['CARE'], ['WEST'], ['EAST'], ['NORTH'], ['FEED'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['CARE'], ['WATER'], ['CARE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['SOUTH'], ['HARVEST'], ['DROP'], ['FEED'], ['WEST'], ['WATER'], ['SOUTH'], ['WEST'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'MELON', 6], ['SELL', 'WHEAT', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['FERTILIZE'], ['EAST'], ['PICKUP', 'GOOSE', 1], ['CARE'], ['WATER'], ['HARVEST'], ['SOUTH'], ['FEED'], ['EAST'], ['FEED']], 'market': [['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['CARE'], ['EAST'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['WEST'], ['FEED'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['DROP'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['FERTILIZE'], ['CARE'], ['WEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['DROP'], ['WEST'], ['PICKUP', 'GOOSE', 1], ['SOUTH']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['BUILD_COOP'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['WEST'], ['NORTH'], ['PLACE', 'GOOSE'], ['WEST'], ['WATER'], ['EAST'], ['FEED'], ['FERTILIZE'], ['WEST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['CARE'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['NORTH'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['EAST'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['EAST'], ['SOUTH'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['PLANT', 'STRAWBERRY'], ['HARVEST'], ['WEST'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['FEED'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['WATER'], ['EAST'], ['WEST'], ['SOUTH'], ['CARE'], ['PLANT', 'WHEAT'], ['EAST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['EAST'], ['WATER'], ['EAST'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'MELON', 6], ['SELL', 'FERTILIZER', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PASS'], ['WEST'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['CARE'], ['CARE'], ['NORTH'], ['PASS'], ['WEST'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'GOOSE', 1], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['DROP'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['EAST'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['EAST'], ['FEED'], ['SOUTH'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['CARE'], ['NORTH'], ['DROP'], ['WATER'], ['FEED'], ['CARE'], ['WEST'], ['CARE']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['CARE'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['CARE'], ['HARVEST'], ['HARVEST'], ['PLACE', 'MILK', 3], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['FEED']], 'market': [['SELL', 'WHEAT', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['HARVEST'], ['FEED'], ['BUILD_COOP'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['CARE'], ['WEST'], ['HARVEST'], ['WATER'], ['WEST'], ['WEST'], ['EAST'], ['CARE'], ['PLACE', 'GOOSE'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['WEST'], ['WEST'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['EAST'], ['CARE'], ['FEED'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['EAST'], ['SOUTH'], ['HARVEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['FERTILIZE'], ['NORTH'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['CARE'], ['WATER'], ['NORTH'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['WATER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['EAST'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['EAST'], ['NORTH'], ['WATER'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['NORTH'], ['FERTILIZE'], ['EAST'], ['WATER'], ['NORTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['DROP'], ['SOUTH'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['SOUTH']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['PASS'], ['PASS'], ['WATER'], ['WATER'], ['WATER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['PASS'], ['PASS'], ['SOUTH'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'FERTILIZER', 10], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 5], ['PICKUP', 'WHEAT', 4], ['SOUTH'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['NORTH'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['EAST'], ['CARE'], ['FEED'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['HARVEST'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['FERTILIZE'], ['WEST'], ['CARE'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WEST'], ['HARVEST'], ['CARE'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FEED'], ['EAST'], ['NORTH'], ['FEED'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['WATER'], ['FEED'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['FEED'], ['FEED'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['SOUTH'], ['WEST'], ['HARVEST'], ['CARE'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['FEED'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['PLANT', 'STRAWBERRY']], 'market': [['SELL', 'WHEAT', 5], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WATER'], ['WEST'], ['WEST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WATER'], ['FERTILIZE']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['FERTILIZE'], ['WATER'], ['WEST'], ['WATER'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['SOUTH'], ['EAST'], ['WEST'], ['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['FEED'], ['WATER'], ['EAST'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['EAST'], ['EAST'], ['NORTH'], ['WATER'], ['WATER'], ['CARE'], ['NORTH'], ['EAST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['PASS'], ['SOUTH'], ['WATER'], ['DROP'], ['NORTH'], ['FERTILIZE']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['EAST'], ['SOUTH'], ['WATER'], ['PASS'], ['EAST'], ['SOUTH'], ['EAST'], ['PASS'], ['EAST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1], ['SELL', 'WHEAT', 8], ['SELL', 'EGG', 10]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['EAST'], ['SOUTH'], ['PASS'], ['PASS'], ['SOUTH']], 'market': [['SELL', 'EGG', 2]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 10], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['PLACE', 'MILK', 6], ['FEED'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WEST'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['NORTH']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['EAST'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER'], ['PLACE', 'MILK', 6], ['HARVEST'], ['EAST'], ['HARVEST'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'MILK', 6]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WEST'], ['CARE'], ['NORTH'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['CARE'], ['NORTH'], ['WEST'], ['FEED'], ['WATER'], ['EAST'], ['WEST'], ['WEST'], ['HARVEST'], ['HARVEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['PASS'], ['SOUTH'], ['EAST'], ['FEED'], ['HARVEST'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WEST'], ['SOUTH'], ['CARE'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['CARE'], ['FERTILIZE'], ['FEED'], ['SOUTH']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['FEED'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['DROP']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['CARE'], ['HARVEST'], ['NORTH'], ['CARE'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['NORTH'], ['CARE'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 2], ['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['FEED'], ['WATER'], ['HARVEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['WEST'], ['FEED'], ['WEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['FERTILIZE'], ['FERTILIZE'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['CARE'], ['FERTILIZE'], ['WATER'], ['CARE']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['WATER'], ['EAST'], ['WATER'], ['CARE'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['EAST'], ['WATER'], ['WEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['HARVEST'], ['WEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST'], ['EAST'], ['WEST'], ['CARE']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FERTILIZE'], ['WEST'], ['WATER'], ['EAST'], ['EAST'], ['SOUTH'], ['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['WEST'], ['NORTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['NORTH'], ['EAST'], ['FERTILIZE'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 5], ['SELL', 'EGG', 12]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['WEST'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'EGG', 7]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'FERTILIZER', 3], ['WEST'], ['PICKUP', 'FERTILIZER', 4], ['WEST']], 'market': [['BUY_SEED', 'TOMATO', 1], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['DROP'], ['NORTH'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['WEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['FEED'], ['PASS']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['CARE'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['CARE'], ['WEST'], ['EAST'], ['FEED'], ['FERTILIZE'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['FEED'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['CARE'], ['CARE'], ['CARE'], ['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['WATER'], ['FEED'], ['FERTILIZE']], 'market': [['SELL', 'WHEAT', 5], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['FEED'], ['HARVEST'], ['FEED'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['CARE'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PASS'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['FEED'], ['EAST'], ['HARVEST'], ['WEST'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['CARE'], ['FERTILIZE'], ['PLANT', 'STRAWBERRY'], ['HARVEST'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 3], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['WEST'], ['EAST'], ['CARE'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['PASS'], ['NORTH'], ['SOUTH'], ['EAST'], ['FERTILIZE'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['PASS'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['WATER'], ['SOUTH'], ['PASS'], ['WEST'], ['WATER']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['SOUTH'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['EAST'], ['EAST'], ['PLANT', 'TOMATO'], ['SOUTH'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['WEST'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['WATER'], ['EAST']], 'market': [['SELL', 'WHEAT', 3], ['SELL', 'EGG', 12]]}, {'farmer': ['EAST'], 'hands': [['FERTILIZE'], ['PASS'], ['SOUTH'], ['PASS'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['EAST'], ['PASS']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'EGG', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 11], ['SELL', 'FERTILIZER', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['SOUTH'], ['EAST'], ['WEST']], 'market': [['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['FEED'], ['NORTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['PICKUP', 'WHEAT', 3]], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['EAST'], ['FEED'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['EAST'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['FEED'], ['EAST'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH'], ['HARVEST'], ['FEED']], 'market': [['SELL', 'WHEAT', 5], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['WEST'], ['CARE'], ['WATER'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['HARVEST'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'MILK', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['FEED'], ['HARVEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['SELL', 'EGG', 8]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['EAST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['CARE'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['WEST'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['HARVEST'], ['FEED'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 12]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['DROP'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WEST'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['WATER'], ['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'EGG', 8]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WATER'], ['SOUTH'], ['DROP'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['PASS'], ['EAST'], ['SOUTH'], ['PICKUP', 'WHEAT', 2], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['PASS'], ['EAST'], ['FEED'], ['EAST'], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['EAST'], ['HARVEST'], ['EAST'], ['DROP'], ['NORTH'], ['SOUTH'], ['EAST'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['FERTILIZE'], ['WATER'], ['EAST'], ['PASS'], ['WATER'], ['WEST'], ['WATER'], ['EAST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'WHEAT', 3]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['SOUTH'], ['SOUTH'], ['EAST'], ['PASS'], ['EAST'], ['WATER'], ['EAST'], ['PASS'], ['FEED'], ['WATER']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'FERTILIZER', 12], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['WEST'], ['EAST'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 13], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['NORTH'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['SELL', 'EGG', 8]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['EAST'], ['CARE'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['CARE'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['CARE'], ['NORTH'], ['WEST'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WEST'], ['FEED'], ['HARVEST'], ['FEED'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['HARVEST'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['SOUTH'], ['CARE'], ['NORTH'], ['CARE'], ['SOUTH'], ['EAST'], ['FEED'], ['NORTH'], ['SOUTH'], ['FERTILIZE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['FEED'], ['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['FEED'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['HARVEST'], ['EAST'], ['CARE'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['CARE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['WEST'], ['WATER'], ['HARVEST'], ['WEST'], ['EAST'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WEST'], ['SOUTH'], ['WATER'], ['FEED'], ['WATER'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['NORTH'], ['NORTH'], ['WEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['CARE'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['FEED'], ['EAST'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['CARE'], ['NORTH'], ['NORTH'], ['WEST'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['NORTH'], ['EAST'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['SOUTH'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['SOUTH'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['WEST'], ['WEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['SOUTH'], ['EAST'], ['PASS'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['SELL', 'WHEAT', 12], ['SELL', 'EGG', 12]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['NORTH'], ['SOUTH'], ['WATER'], ['EAST'], ['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['WEST']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 11], ['SELL', 'TOMATO', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['PICKUP', 'FERTILIZER', 3], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'WOOL', 1], ['SELL', 'FERTILIZER', 6], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['FEED'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['WEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['CARE']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['FEED'], ['EAST'], ['NORTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['FERTILIZE'], ['CARE'], ['FEED'], ['WATER'], ['EAST'], ['WEST'], ['FERTILIZE'], ['WEST'], ['WATER'], ['HARVEST'], ['HARVEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['DIG'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['FEED'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['PLANT', 'TOMATO'], ['WATER'], ['NORTH'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['FERTILIZE'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['FERTILIZE'], ['CARE'], ['WEST'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['SOUTH'], ['FEED'], ['FERTILIZE'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['DIG'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'TOMATO', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['CARE'], ['WATER'], ['WEST'], ['EAST'], ['WEST'], ['NORTH'], ['PLANT', 'TOMATO'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['WEST'], ['DROP'], ['EAST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['NORTH'], ['HARVEST'], ['WEST'], ['HARVEST'], ['PASS'], ['EAST'], ['WEST']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['WEST'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['DIG'], ['PASS'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'WHEAT', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['WATER'], ['DROP'], ['DIG'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['EAST'], ['SOUTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['EAST'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'FERTILIZER', 1], ['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['WATER'], ['DROP'], ['WATER'], ['FEED'], ['FEED'], ['HARVEST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['FERTILIZE']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['EAST'], ['EAST'], ['SOUTH'], ['CARE'], ['CARE'], ['PASS'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 3], ['SELL', 'EGG', 6]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['NORTH'], ['EAST'], ['SOUTH'], ['HARVEST'], ['PASS'], ['PASS'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['PASS']], 'market': [['SELL', 'EGG', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 11], ['BUY_PRODUCT', 'WHEAT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['EAST'], ['WEST'], ['PICKUP', 'FERTILIZER', 3], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'WOOL', 1], ['BUY_PRODUCT', 'WHEAT', 13], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['CARE'], ['EAST'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['FEED'], ['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['CARE'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['CARE'], ['WATER'], ['WEST'], ['SOUTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WEST'], ['FEED'], ['NORTH'], ['EAST'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['FEED'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WEST'], ['CARE'], ['FEED'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST'], ['CARE'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['WATER'], ['CARE'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'WHEAT', 5], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['FEED'], ['NORTH'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WATER'], ['CARE'], ['WATER'], ['FERTILIZE'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['SOUTH'], ['EAST'], ['HARVEST'], ['FERTILIZE'], ['FERTILIZE'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['EAST'], ['NORTH']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['HARVEST'], ['NORTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['DIG'], 'hands': [['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['DIG'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FERTILIZE'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['EAST'], ['CARE']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['FERTILIZE'], ['SOUTH'], ['WATER'], ['DIG'], ['WEST'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['EAST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['EAST'], ['WATER'], ['DIG'], ['DIG'], ['EAST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['HARVEST'], ['WATER'], ['WATER'], ['EAST'], ['HARVEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WEST'], ['SOUTH'], ['DROP']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['SOUTH'], ['WATER'], ['WEST'], ['WEST'], ['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 3], ['SELL', 'EGG', 12]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WEST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['EAST'], ['NORTH'], ['DIG'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'TOMATO', 2], ['SELL', 'EGG', 8]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 11], ['SELL', 'FERTILIZER', 8], ['SELL', 'TOMATO', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['PICKUP', 'FERTILIZER', 1]], 'market': [['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['FEED'], ['NORTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['EAST'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['CARE'], ['EAST'], ['WEST'], ['NORTH'], ['WEST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['FERTILIZE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WEST'], ['CARE'], ['WATER'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['EAST'], ['EAST'], ['HARVEST'], ['WEST'], ['SOUTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WATER'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['EAST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['FEED'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['CARE'], ['NORTH'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['WEST'], ['HARVEST'], ['CARE']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WATER'], ['SOUTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['EAST'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['FERTILIZE'], ['EAST'], ['NORTH'], ['SOUTH'], ['EAST'], ['WATER'], ['WEST'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['EAST'], ['HARVEST'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['EAST'], ['DROP'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['HARVEST'], ['WATER'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['CARE'], ['NORTH'], ['EAST'], ['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['EAST'], ['EAST'], ['WEST'], ['SOUTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['FEED'], ['FEED'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['NORTH'], ['NORTH'], ['WATER'], ['CARE'], ['SOUTH'], ['DIG'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['FERTILIZE'], ['NORTH'], ['HARVEST'], ['EAST'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FERTILIZE'], ['WATER'], ['EAST'], ['FEED'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'EGG', 4]]}, {'farmer': ['EAST'], 'hands': [['PASS'], ['PASS'], ['SOUTH'], ['SOUTH'], ['CARE'], ['FERTILIZE'], ['NORTH'], ['SOUTH'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 6], ['SELL', 'EGG', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['BUY_PRODUCT', 'WHEAT', 11], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['EAST'], ['WEST'], ['PICKUP', 'FERTILIZER', 3], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['CARE'], ['EAST'], ['WEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['FEED'], ['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['NORTH'], ['CARE'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WEST'], ['EAST'], ['FEED'], ['EAST'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['NORTH'], ['FEED'], ['HARVEST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['FEED'], ['SOUTH'], ['FEED'], ['CARE'], ['HARVEST'], ['WATER'], ['SOUTH'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['CARE'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['CARE'], ['HARVEST'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['CARE'], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['EAST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['FEED'], ['WATER'], ['EAST'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['CARE'], ['WEST'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 4], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['WEST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['WATER'], ['HARVEST'], ['EAST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['SOUTH'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['NORTH'], ['WATER'], ['WEST'], ['WEST'], ['EAST'], ['FERTILIZE'], ['FERTILIZE'], ['WEST'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['FEED'], ['EAST'], ['WEST'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['CARE'], ['NORTH'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['EAST'], ['FERTILIZE'], ['EAST'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['FERTILIZE'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH'], ['EAST'], ['WEST'], ['PASS'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['WEST'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WEST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'WHEAT', 5], ['SELL', 'TOMATO', 2], ['SELL', 'EGG', 16]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['PASS'], ['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['PASS'], ['NORTH'], ['PASS'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 3], ['SELL', 'EGG', 8]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 11], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 3], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['PICKUP', 'FERTILIZER', 3], ['NORTH'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['EAST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'FERTILIZER', 4]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['CARE'], ['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['WEST'], ['HARVEST'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['WEST'], ['FEED'], ['WATER'], ['NORTH'], ['WEST'], ['SOUTH'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['FEED'], ['CARE'], ['HARVEST'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['EAST'], ['HARVEST'], ['WATER'], ['EAST'], ['WATER'], ['NORTH'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH'], ['EAST'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WEST'], ['FEED'], ['WEST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WEST'], ['NORTH']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['EAST'], ['WATER'], ['SOUTH'], ['NORTH'], ['FERTILIZE'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['DIG'], ['WEST'], ['CARE'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WEST'], ['DROP'], ['WATER'], ['WATER'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['NORTH'], ['WATER'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['SOUTH'], ['WEST'], ['WATER'], ['SOUTH'], ['FEED'], ['WEST'], ['EAST'], ['WATER'], ['FERTILIZE'], ['NORTH']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['SOUTH'], ['WEST'], ['CARE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WATER'], ['FERTILIZE'], ['FEED'], ['DROP'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WATER'], ['WEST'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['HARVEST'], 'hands': [['DIG'], ['SOUTH'], ['WATER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['FEED'], ['NORTH'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'EGG', 8]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['CARE'], ['NORTH'], ['EAST'], ['HARVEST'], ['CARE'], ['HARVEST'], ['SOUTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['WATER'], ['NORTH'], ['DIG'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WATER'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['DROP'], ['WEST'], ['FEED'], ['PLANT', 'WHEAT'], ['WEST'], ['DIG']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['SOUTH'], ['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FERTILIZE'], ['CARE'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['FERTILIZE'], ['FERTILIZE'], ['WEST'], ['CARE'], ['HARVEST'], ['WEST'], ['WATER'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['NORTH'], ['FEED'], ['DIG'], ['WATER'], ['WEST']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['NORTH'], ['PASS'], ['HARVEST'], ['DIG'], ['WEST'], ['NORTH'], ['CARE'], ['SOUTH'], ['SOUTH'], ['DIG']], 'market': [['SELL', 'FERTILIZER', 1], ['SELL', 'WHEAT', 5], ['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 11], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['EAST'], ['WEST'], ['PICKUP', 'FERTILIZER', 3], ['WEST']], 'market': [['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 8]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['CARE'], ['EAST'], ['CARE'], ['EAST'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['WEST'], ['HARVEST'], ['FEED'], ['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['CARE'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['CARE'], ['NORTH'], ['HARVEST'], ['WEST'], ['SOUTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['FEED'], ['EAST'], ['FEED'], ['EAST'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['CARE'], ['FEED'], ['CARE'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['DIG'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['WATER'], ['CARE'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['FERTILIZE'], ['CARE'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['FEED'], ['WEST'], ['NORTH'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['WATER'], ['EAST'], ['NORTH'], ['WATER'], ['WEST'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['CARE'], ['WATER'], ['WATER'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 4]]}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['HARVEST'], ['WATER'], ['EAST'], ['NORTH'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['NORTH'], ['DIG'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['DIG'], ['SOUTH'], ['WEST'], ['NORTH'], ['HARVEST'], ['DIG'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['EAST'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['FERTILIZE'], ['WATER'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['FEED'], ['DIG'], ['EAST'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['DIG'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['CARE'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['EAST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['SELL', 'MILK', 2], ['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['EAST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'MILK', 1], ['SELL', 'WHEAT', 4], ['SELL', 'EGG', 10]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['PASS'], ['DIG'], ['WATER'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['SOUTH'], ['EAST'], ['FERTILIZE']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'WHEAT', 16], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['HARVEST'], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 3], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'WOOL', 1], ['SELL', 'TOMATO', 2], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['DROP'], ['NORTH'], ['PLACE', 'MILK', 6], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 2], ['EAST'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['DIG'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['WATER'], ['WEST'], ['EAST'], ['FEED']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['HARVEST'], ['CARE'], ['CARE'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['FERTILIZE'], ['WEST'], ['NORTH'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['FEED'], ['FEED'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['FEED'], ['FERTILIZE'], ['EAST'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['FERTILIZE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['CARE'], ['WATER'], ['DIG'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER'], ['FEED'], ['WATER'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['WEST'], ['CARE'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 4]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['SOUTH'], ['EAST'], ['WEST'], ['WEST'], ['FERTILIZE'], ['FERTILIZE'], ['CARE'], ['FERTILIZE'], ['NORTH'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['WEST'], ['HARVEST'], ['SOUTH'], ['WEST'], ['NORTH'], ['HARVEST'], ['DROP']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['EAST'], ['HARVEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 3], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['NORTH'], ['EAST'], ['EAST'], ['SOUTH'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 5], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['FEED'], ['SOUTH'], ['FERTILIZE'], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['WATER'], ['WEST'], ['EAST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['EAST'], ['HARVEST'], ['CARE']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['HARVEST'], ['WEST'], ['SOUTH'], ['WATER'], ['EAST'], ['FERTILIZE'], ['FERTILIZE'], ['PASS'], ['PLANT', 'WHEAT'], ['PASS']], 'market': [['SELL', 'EGG', 16]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['SOUTH'], ['WATER'], ['EAST'], ['NORTH'], ['HARVEST'], ['WATER'], ['PASS'], ['NORTH'], ['WATER'], ['PASS']], 'market': [['SELL', 'WHEAT', 1], ['SELL', 'EGG', 10]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'WHEAT', 16], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['EAST'], ['WEST'], ['PICKUP', 'FERTILIZER', 3], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WEST'], ['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'FERTILIZER', 3]], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['CARE'], ['EAST'], ['WEST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['FEED'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['CARE'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['FEED'], ['HARVEST'], ['WEST'], ['SOUTH'], ['PLANT', 'CARROT'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['FERTILIZE'], ['NORTH'], ['CARE'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['WATER'], ['WATER'], ['FEED'], ['SOUTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['DIG'], ['WEST'], ['WEST'], ['CARE'], ['FERTILIZE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FEED'], ['WEST'], ['HARVEST'], ['NORTH'], ['EAST'], ['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['FEED'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['HARVEST'], ['CARE'], ['HARVEST'], ['WATER'], ['HARVEST'], ['WEST'], ['PLANT', 'CARROT'], ['HARVEST'], ['FERTILIZE'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['PLANT', 'CARROT'], ['EAST'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['DIG']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['FERTILIZE'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH'], ['DIG'], ['SOUTH'], ['WATER'], ['NORTH'], ['PLANT', 'CARROT']], 'market': [['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['NORTH'], ['HARVEST'], ['WEST'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['FEED'], ['WEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'MILK', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['EAST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['HARVEST'], ['DIG'], ['WATER'], ['HARVEST'], ['WEST'], ['HARVEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['FERTILIZE'], ['FEED'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'CARROT'], ['WEST'], ['CARE'], ['WATER'], ['PLANT', 'CARROT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['CARE'], ['EAST'], ['WEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WEST']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['EAST'], ['FERTILIZE'], ['SOUTH'], ['WEST'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER'], ['EAST'], ['WATER']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['FEED'], ['WATER'], ['WATER'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['CARE'], ['WEST'], ['WEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['FEED'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER']], 'market': [['SELL', 'WHEAT', 2], ['BUY_SEED', 'WHEAT', 1], ['SELL', 'EGG', 8]]}, {'farmer': ['FERTILIZE'], 'hands': [['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['FERTILIZE'], ['CARE'], ['WATER'], ['WATER'], ['HARVEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['FEED'], ['FEED'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['EAST'], ['SOUTH'], ['EAST'], ['PLANT', 'CARROT']], 'market': [['SELL', 'TOMATO', 2], ['SELL', 'EGG', 10]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['CARE'], ['CARE'], ['PASS'], ['PASS'], ['WATER'], ['PASS'], ['EAST'], ['FERTILIZE'], ['WATER'], ['WATER']], 'market': [['SELL', 'EGG', 2]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'WOOL', 1], ['SELL', 'WHEAT', 13], ['SELL', 'TOMATO', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 2], 'hands': [['HARVEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'MILK', 4], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PLACE', 'MILK', 4], ['DROP'], ['NORTH'], ['WEST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WEST'], ['PICKUP', 'FERTILIZER', 3]], 'market': [['SELL', 'FERTILIZER', 5]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['FEED'], ['FEED'], ['WEST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['CARE'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 3]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['DIG'], 'hands': [['EAST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WEST'], ['EAST'], ['HARVEST'], ['SOUTH']], 'market': []}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['HARVEST'], ['PLANT', 'CARROT'], ['WATER'], ['EAST'], ['WATER'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['SOUTH'], ['EAST'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'WHEAT', 5], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['HARVEST'], ['WATER'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['HARVEST'], ['FEED'], ['SOUTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['DROP'], ['HARVEST'], ['NORTH'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 1], ['SELL', 'MILK', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['FERTILIZE'], ['HARVEST'], ['WATER'], ['CARE'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['PLANT', 'CARROT'], ['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['SELL', 'WHEAT', 5], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DIG'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['NORTH'], ['CARE'], ['HARVEST'], ['WEST'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['WATER'], ['SOUTH'], ['FEED'], ['WATER'], ['WEST'], ['EAST'], ['WATER'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WATER'], ['CARE'], ['NORTH'], ['FEED'], ['EAST'], ['HARVEST'], ['HARVEST'], ['DIG']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'WHEAT'], ['EAST'], ['SOUTH'], ['FERTILIZE'], ['CARE'], ['EAST'], ['PLANT', 'WHEAT'], ['PLANT', 'CARROT'], ['PLANT', 'CARROT']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FERTILIZE'], ['WEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['SOUTH'], ['FEED'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'WHEAT', 1], ['SELL', 'EGG', 4]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['DIG'], ['CARE'], ['WATER'], ['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['FERTILIZE']], 'market': [['SELL', 'EGG', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'WHEAT', 16], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['EAST'], ['WEST'], ['PICKUP', 'FERTILIZER', 3], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'TOMATO', 2], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['FEED'], ['NORTH'], ['FEED'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['CARE'], ['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['NORTH'], ['HARVEST'], ['WEST'], ['WATER'], ['DIG'], ['NORTH'], ['FEED']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['PLANT', 'CARROT'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['FEED'], ['EAST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WHEAT', 5], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['CARE'], ['FEED'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['FEED'], ['WEST'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['FERTILIZE'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['SOUTH'], ['CARE'], ['FEED'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['CARE'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['CARE'], ['WATER'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['SOUTH'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['CARE']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['FEED'], ['NORTH'], ['HARVEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['SOUTH'], ['EAST'], ['HARVEST'], ['WATER'], ['WEST'], ['FERTILIZE'], ['CARE'], ['HARVEST'], ['PLANT', 'WHEAT'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['FERTILIZE'], ['EAST'], ['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['NORTH'], ['EAST'], ['PLANT', 'CARROT']], 'market': [['SELL', 'STRAWBERRY', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['DIG'], ['WEST'], ['WATER'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['HARVEST'], ['WATER'], ['WATER'], ['DIG'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['FERTILIZE']], 'market': [['SELL', 'MILK', 1]]}, {'farmer': ['HARVEST'], 'hands': [['PLANT', 'WHEAT'], ['CARE'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['WATER'], ['SOUTH'], ['FEED'], ['WATER'], ['NORTH'], ['SOUTH'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 4]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['HARVEST'], ['WATER'], ['WATER'], ['EAST'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['FERTILIZE'], ['DIG'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['SOUTH'], ['EAST'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['SELL', 'TOMATO', 2], ['SELL', 'EGG', 14]]}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['NORTH'], ['SOUTH'], ['WATER'], ['DROP'], ['DROP'], ['FERTILIZE'], ['FERTILIZE'], ['NORTH'], ['WEST'], ['FERTILIZE']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'WHEAT', 16], ['SELL', 'TOMATO', 5], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'MILK', 3], 'hands': [['HARVEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 3], ['NORTH']], 'market': [['SELL', 'MILK', 3], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PLACE', 'MILK', 3], ['DROP'], ['NORTH'], ['WEST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['WEST'], ['EAST'], ['PICKUP', 'FERTILIZER', 3]], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['EAST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['FEED'], ['FEED'], ['WEST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['HARVEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['WATER'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['FERTILIZE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['FEED'], ['EAST'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['EAST'], ['WATER'], ['NORTH'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['SOUTH'], ['FEED'], ['WEST'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['FERTILIZE'], ['WATER']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['EAST'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WATER'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WEST'], ['EAST'], ['WATER'], ['SOUTH'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['WEST'], 'hands': [['FERTILIZE'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['DROP'], ['NORTH'], ['HARVEST'], ['EAST'], ['FERTILIZE'], ['SOUTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['EAST'], ['WEST'], ['EAST'], ['NORTH'], ['DROP'], ['WATER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 6], ['SELL', 'CARROT', 13]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['FERTILIZE'], ['WEST'], ['EAST'], ['NORTH'], ['WATER'], ['NORTH'], ['NORTH'], ['EAST'], ['WEST']], 'market': [['SELL', 'CARROT', 3]]}, {'farmer': ['SOUTH'], 'hands': [['FERTILIZE'], ['NORTH'], ['FEED'], ['EAST'], ['NORTH'], ['HARVEST'], ['WATER'], ['NORTH'], ['PASS'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['PASS'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 7]]}, {'farmer': ['HARVEST'], 'hands': [['FERTILIZE'], ['EAST'], ['SOUTH'], ['DROP'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'CARROT', 7]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['EAST'], ['DROP'], ['NORTH'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'FERTILIZER', 1], ['SELL', 'TOMATO', 2], ['SELL', 'EGG', 9]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['DROP'], ['PASS'], ['NORTH'], ['DROP'], ['EAST'], ['SOUTH'], ['NORTH'], ['PASS'], ['EAST']], 'market': [['SELL', 'CARROT', 4], ['SELL', 'EGG', 4]]}, {'farmer': ['WEST'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['SELL', 'WHEAT', 24], ['SELL', 'FERTILIZER', 6]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['HIRE'], ['HIRE'], ['SELL', 'WHEAT', 13]]}, {'farmer': ['WEST'], 'hands': [['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['EAST'], ['NORTH'], ['NORTH'], ['WEST'], ['EAST'], ['WEST'], ['WEST']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST'], ['EAST'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['EAST'], ['WEST'], ['EAST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['WEST'], ['EAST'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['EAST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['HARVEST'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['EAST'], ['WATER'], ['HARVEST'], ['WEST'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'MILK', 1]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['WEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['HARVEST'], ['EAST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WATER'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['EAST'], ['NORTH'], ['WATER'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'MILK', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['WEST'], ['EAST'], ['WEST'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'CARROT', 13]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['HARVEST'], ['NORTH'], ['WEST'], ['SOUTH'], ['WEST'], ['EAST'], ['SOUTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['WEST'], ['DROP'], ['WEST'], ['SOUTH'], ['WEST'], ['EAST'], ['SOUTH'], ['EAST'], ['EAST']], 'market': [['SELL', 'TOMATO', 2], ['SELL', 'MILK', 2]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['DROP'], ['PASS'], ['WEST'], ['EAST'], ['SOUTH'], ['EAST'], ['WEST'], ['EAST'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'WHEAT', 3], ['SELL', 'MILK', 1]]}, {'farmer': ['DROP'], 'hands': [['DROP'], ['NORTH'], ['NORTH'], ['DROP'], ['EAST'], ['SOUTH'], ['DROP'], ['WEST'], ['NORTH'], ['DROP']], 'market': [['SELL', 'CARROT', 7], ['SELL', 'FERTILIZER', 7], ['SELL', 'TOMATO', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['EAST'], ['SOUTH'], ['NORTH'], ['WEST'], ['DROP'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'WHEAT', 13], ['SELL', 'FERTILIZER', 3]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['DROP'], ['SOUTH'], ['NORTH'], ['DROP'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'STRAWBERRY', 2], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['DROP'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'CARROT', 12], ['SELL', 'WHEAT', 10], ['SELL', 'TOMATO', 2], ['SELL', 'MILK', 1], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'EGG', 21], ['SELL', 'WHEAT', 4], ['SELL', 'CARROT', 2]]}]
_PROXY=make_agent({0:_DEMO})
def demonstrated_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
demonstrated_proxy.telemetry=_PROXY.chassis.diagnostics
agent=demonstrated_proxy
