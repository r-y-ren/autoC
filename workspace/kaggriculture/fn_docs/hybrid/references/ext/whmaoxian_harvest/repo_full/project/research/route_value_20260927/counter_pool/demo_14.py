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

_DEMO=[{'farmer': ['PASS'], 'hands': [], 'market': [['BUY_ANIMAL', 'COW', 1], ['BUY_PRODUCT', 'WHEAT', 5], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1], ['BUY_ANIMAL', 'SHEEP', 1]]}, {'farmer': ['PICKUP', 'COW', 1], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_ANIMAL', 'COW', 1], ['HIRE']]}, {'farmer': ['BUILD_PASTURE'], 'hands': [['PICKUP', 'SHEEP', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'COW', 1], ['PICKUP', 'SHEEP', 1], ['PICKUP', 'COW', 1]], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'COW', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WHEAT', 1], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['BUILD_PASTURE'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['BUILD_PASTURE'], ['PLACE', 'SHEEP', 1], ['NORTH'], ['PLACE', 'SHEEP', 1], ['NORTH']], 'market': [['BUY_SEED', 'MELON', 2], ['BUY_PRODUCT', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['PLACE', 'SHEEP', 1], ['CARE'], ['WEST'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['WEST'], ['BUILD_PASTURE'], ['BUILD_PASTURE'], ['PLANT', 'MELON']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['NORTH'], ['PLACE', 'COW', 1], ['PLACE', 'SHEEP', 1], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PLANT', 'MELON'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['PLANT', 'MELON'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'MELON', 2]]}, {'farmer': ['SOUTH'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WATER'], ['WEST'], ['PLANT', 'MELON'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'MELON'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PLANT', 'WHEAT'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['WEST']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['WATER'], ['PASS'], ['PASS'], ['PLANT', 'WHEAT']], 'market': [[]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['SOUTH'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['DROP'], ['COLLECT_FERTILIZER']], 'market': [[]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['EAST']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['DROP']], 'market': [['BUY_SEED', 'MELON', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['SOUTH'], ['CARE']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['CARE'], ['FEED']], 'market': []}, {'farmer': ['PLANT', 'MELON'], 'hands': [['PASS'], ['FEED'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [['PASS'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['PLANT', 'MELON'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['DROP'], ['NORTH']], 'market': [['SELL', 'WHEAT', 1]]}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['DROP'], ['DROP'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WATER'], 'hands': [['PICKUP', 'COW', 1], ['CARE'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['SOUTH'], ['NORTH'], ['HARVEST']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['PASS'], ['SOUTH'], ['WATER'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['BUILD_PASTURE'], ['PASS'], ['SOUTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PLACE', 'COW', 1], ['PASS'], ['CARE'], ['NORTH'], ['EAST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['PASS'], ['FEED'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['SOUTH'], ['PASS'], ['EAST'], ['HARVEST'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['PASS'], ['FEED'], ['PASS'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['FEED'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['PASS'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 7], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['WEST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['DROP'], ['DROP'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['NORTH'], ['SOUTH'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'COW', 1], ['CARE'], ['SOUTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['EAST'], ['WATER'], ['FEED']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['SOUTH'], ['HARVEST'], ['CARE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['DROP'], ['SOUTH'], ['SOUTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['PASS'], ['FEED'], ['FEED']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['BUILD_PASTURE'], ['WEST'], ['PASS'], ['CARE'], ['SOUTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['HARVEST'], 'hands': [['PLACE', 'COW', 1], ['WATER'], ['PASS'], ['SOUTH'], ['FEED']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WEST'], ['NORTH'], ['PASS'], ['SOUTH'], ['PASS']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['PLANT', 'STRAWBERRY'], ['WATER'], ['PASS'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['HARVEST'], ['PASS'], ['CARE'], ['PASS']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PLANT', 'STRAWBERRY'], ['PASS'], ['FEED'], ['PASS']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WATER'], ['WATER'], ['PASS'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['FEED'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WEST'], ['PASS'], ['PASS'], ['CARE'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 7], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['DROP'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WEST'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['EAST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['DROP'], ['WEST'], ['WEST'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'COW', 1]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'COW', 1], ['CARE'], ['SOUTH'], ['WEST'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['EAST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PASS'], ['EAST'], ['HARVEST'], ['DROP'], ['WATER']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['EAST'], ['PICKUP', 'WHEAT', 2], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WEST'], ['DROP'], ['EAST'], ['PASS'], ['WATER']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['BUILD_PASTURE'], ['FEED'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['PASS'], ['HARVEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['PLACE', 'COW', 1], ['WEST'], ['FEED'], ['NORTH'], ['PASS'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['FEED'], ['NORTH'], ['FEED'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['HARVEST'], ['CARE'], ['CARE'], ['CARE'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['PASS'], ['FEED'], ['SOUTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['FEED'], ['PASS'], ['PASS'], ['FEED'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WATER'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['CARE'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['EAST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['WEST'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['NORTH']], 'market': []}, {'farmer': ['DROP'], 'hands': [['SOUTH'], ['EAST'], ['FEED'], ['CARE'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['SOUTH'], ['EAST'], ['CARE'], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 1], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['PASS'], ['FEED'], ['FEED'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 2], ['PASS'], ['CARE'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PASS'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['DROP']], 'market': []}, {'farmer': ['CARE'], 'hands': [['WEST'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['WEST'], ['CARE'], ['NORTH'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WATER'], ['WEST'], ['WEST'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['WATER'], ['EAST'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['EAST'], ['NORTH'], ['EAST'], ['WEST'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['WATER'], ['FEED'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['CARE'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WEST'], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['PLACE', 'FERTILIZER', 1], ['WEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WOOL', 6], ['BUY_LAND']]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['NORTH'], ['FEED'], ['EAST'], ['EAST'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 6], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'GOOSE', 1], ['NORTH'], ['CARE'], ['EAST'], ['EAST'], ['WATER'], ['WATER'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLANT', 'STRAWBERRY'], ['DROP'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WOOL', 6], ['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['BUILD_COOP'], ['SOUTH'], ['WEST'], ['WATER'], ['PICKUP', 'GOOSE', 1], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': [['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['PICKUP', 'GOOSE', 1], 'hands': [['PLACE', 'GOOSE', 1], ['SOUTH'], ['FEED'], ['NORTH'], ['EAST'], ['SOUTH'], ['EAST'], ['WATER'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'MELON', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['PLACE', 'FERTILIZER', 1], ['CARE'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['SOUTH'], ['WATER'], ['EAST'], ['EAST']], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'MELON'], ['PICKUP', 'GOOSE', 1], ['COLLECT_FERTILIZER'], ['WATER'], ['BUILD_COOP'], ['SOUTH'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'MELON', 2], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLACE', 'GOOSE', 1], 'hands': [['WATER'], ['EAST'], ['EAST'], ['EAST'], ['PLACE', 'GOOSE', 1], ['SOUTH'], ['WATER'], ['WATER'], ['CARE']], 'market': [['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['NORTH'], ['EAST'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['PLACE', 'FERTILIZER', 1], ['EAST'], ['SOUTH'], ['PICKUP', 'GOOSE', 1]], 'market': [['BUY_ANIMAL', 'GOOSE', 1], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PICKUP', 'GOOSE', 1], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['DROP'], ['WATER'], ['BUILD_COOP'], ['PICKUP', 'GOOSE', 1], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['PLACE', 'GOOSE', 1], ['PICKUP', 'WHEAT', 3], ['EAST'], ['PLACE', 'GOOSE', 1], ['PICKUP', 'WHEAT', 3], ['PLACE', 'FERTILIZER', 1], ['WATER'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['NORTH'], ['FEED'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['NORTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['EAST'], 'hands': [['PLANT', 'MELON'], ['NORTH'], ['NORTH'], ['WATER'], ['BUILD_COOP'], ['NORTH'], ['PASS'], ['PLANT', 'STRAWBERRY'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['BUILD_COOP'], 'hands': [['WATER'], ['PLANT', 'STRAWBERRY'], ['FEED'], ['NORTH'], ['PLACE', 'GOOSE', 1], ['NORTH'], ['PASS'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['PLACE', 'GOOSE', 1], 'hands': [['NORTH'], ['WATER'], ['CARE'], ['PLANT', 'STRAWBERRY'], ['EAST'], ['FEED'], ['PASS'], ['NORTH'], ['BUILD_COOP']], 'market': [[]]}, {'farmer': ['NORTH'], 'hands': [['PLANT', 'STRAWBERRY'], ['EAST'], ['NORTH'], ['WATER'], ['NORTH'], ['CARE'], ['PASS'], ['WEST'], ['PLACE', 'GOOSE', 1]], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'STRAWBERRY'], 'hands': [['WATER'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['WEST'], ['EAST'], ['WEST'], ['PASS'], ['WEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['NORTH'], ['PASS'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['FEED'], ['WATER'], ['WATER'], ['WEST'], ['PASS'], ['PLANT', 'STRAWBERRY'], ['PASS']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['PASS'], ['CARE'], ['PASS'], ['PASS'], ['WATER'], ['PASS'], ['WATER'], ['PASS']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], [], []]}, {'farmer': ['DROP'], 'hands': [['CARE'], ['NORTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [[], [], []]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['DROP'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3], []]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['SOUTH'], ['PICKUP', 'WHEAT', 4], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['DROP'], ['FEED'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 2], []]}, {'farmer': ['DROP'], 'hands': [['DROP'], ['EAST'], ['SOUTH'], ['CARE'], ['NORTH'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['PICKUP', 'WHEAT', 3], ['FEED'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_PRODUCT', 'WHEAT', 3]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['PLACE', 'FERTILIZER', 1], ['DROP'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER']], 'market': [[]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['WEST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FEED'], ['PICKUP', 'WHEAT', 3], ['FEED'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['NORTH'], ['EAST'], ['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['FEED'], ['NORTH'], ['WEST'], ['FEED'], ['EAST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['CARE'], ['FEED'], ['WATER'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['CARE'], ['WEST'], ['SOUTH'], ['DROP']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FEED'], ['NORTH'], ['NORTH'], ['DROP'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 2]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['CARE'], ['FEED'], ['WATER'], ['PASS'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['CARE'], ['NORTH'], ['PASS'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['PASS'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WATER'], ['PLACE', 'FERTILIZER', 2], ['PASS'], ['NORTH'], ['PASS'], ['FEED']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['WEST'], ['EAST'], ['WATER'], ['PASS'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['PASS'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['PASS'], ['NORTH'], ['WATER'], ['PASS'], ['EAST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['WATER'], ['PASS'], ['WATER'], ['EAST'], ['PASS'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['DROP'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['EAST']], 'market': [['SELL', 'MILK', 6], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLACE', 'FERTILIZER', 1], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['NORTH'], ['EAST'], ['NORTH']], 'market': [['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['PLACE', 'FERTILIZER', 1], 'hands': [['PICKUP', 'WHEAT', 4], ['WEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['FEED'], ['FEED'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['WATER'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], []]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['FEED'], ['SOUTH'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WEST']], 'market': [[]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['DROP'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST']], 'market': [['SELL', 'MILK', 6], ['BUY_LAND'], []]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': [[]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['EAST'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['DROP'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'FERTILIZER', 1], []]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['EAST'], ['FEED'], ['SOUTH'], ['WEST'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['CARE'], ['SOUTH'], ['DROP'], ['EAST'], ['PICKUP', 'GOOSE', 1], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['DROP'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['DROP'], ['WATER'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], []]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['WATER'], ['EAST'], ['WATER'], ['WEST'], ['WEST'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['EAST'], ['SOUTH'], ['BUILD_COOP'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['NORTH'], ['DROP'], ['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'WHEAT'], ['PLACE', 'GOOSE', 1], ['WATER'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['WEST'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['WEST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['FEED'], ['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 3]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WEST'], ['EAST'], ['NORTH'], ['WATER'], ['EAST'], ['NORTH'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WATER'], ['CARE'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS'], ['WATER'], ['CARE'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['BUY_PRODUCT', 'WHEAT', 6], ['BUY_PRODUCT', 'WHEAT', 6]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['PLACE', 'FERTILIZER', 1], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['NORTH'], ['WEST'], ['PICKUP', 'WHEAT', 4]], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 3], ['EAST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST']], 'market': [['SELL', 'WOOL', 4], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['DROP'], ['FEED'], ['PLACE', 'FERTILIZER', 1], ['FEED'], ['EAST'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH'], ['FEED']], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['PICKUP', 'GOOSE', 1], ['CARE'], ['EAST'], ['FEED'], ['WATER'], ['NORTH'], ['WATER'], ['CARE']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['FEED'], 'hands': [['PLACE', 'FERTILIZER', 1], ['NORTH'], ['WEST'], ['EAST'], ['DROP'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'WOOL', 4], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'GOOSE', 1], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PICKUP', 'GOOSE', 1], ['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1], ['BUY_ANIMAL', 'GOOSE', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['SOUTH'], ['FEED'], ['BUILD_COOP'], ['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['BUILD_COOP'], ['CARE'], ['PLACE', 'GOOSE', 1], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['WATER'], ['SOUTH'], ['WATER'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PLACE', 'GOOSE', 1], ['NORTH'], ['WEST'], ['EAST'], ['BUILD_COOP'], ['CARE'], ['EAST'], ['DROP'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'GOOSE', 1], ['FEED'], ['PLANT', 'WHEAT'], ['WATER'], ['PLACE', 'GOOSE', 1], ['WEST'], ['WATER'], ['PICKUP', 'GOOSE', 1], ['NORTH'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 2], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['CARE'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['BUILD_COOP'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['FEED'], ['WATER'], ['FEED'], ['NORTH'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['PLACE', 'GOOSE', 1], ['NORTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['PLANT', 'WHEAT'], ['CARE'], ['WEST'], ['NORTH'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLACE', 'FERTILIZER', 2], 'hands': [['EAST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WEST'], ['DROP']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['EAST'], ['NORTH'], ['WATER'], ['NORTH'], ['WEST'], ['SOUTH'], ['WEST'], ['WATER'], ['PICKUP', 'WHEAT', 2]], 'market': [['SELL', 'FERTILIZER', 4]]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 2], ['EAST'], ['EAST'], ['EAST'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WATER'], ['NORTH'], ['EAST'], ['PLANT', 'MELON'], ['SOUTH'], ['EAST'], ['FEED'], ['EAST'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['CARE'], ['HARVEST'], ['CARE'], ['WATER'], ['WATER'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['CARE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['PASS'], ['PLANT', 'WHEAT'], ['PASS'], ['SOUTH'], ['SOUTH'], ['WEST'], ['CARE'], ['WEST'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['WATER'], ['PASS'], ['WATER'], ['SOUTH'], ['WATER'], ['PASS'], ['WATER'], ['SOUTH'], ['FEED']], 'market': []}, {'farmer': ['PASS'], 'hands': [['PASS'], ['SOUTH'], ['PASS'], ['SOUTH'], ['WATER'], ['SOUTH'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['NORTH']], 'market': [['HIRE'], ['HIRE'], ['BUY_PRODUCT', 'WHEAT', 12], ['BUY_PRODUCT', 'WHEAT', 5]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['DROP'], ['FEED'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['EAST'], ['WEST'], ['HARVEST'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['PICKUP', 'WHEAT', 4], ['CARE'], ['WEST'], ['NORTH'], ['WEST'], ['WEST'], ['WATER'], ['WEST'], ['DROP'], ['WEST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['HARVEST'], ['WEST'], ['EAST'], ['WATER'], ['PICKUP', 'WHEAT', 4], ['NORTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['CARE'], ['SOUTH'], ['CARE'], ['HARVEST'], ['WEST'], ['WEST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['DROP'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['EAST'], ['EAST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MELON', 6], ['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [['EAST'], ['NORTH'], ['SOUTH'], ['WEST'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['FEED'], ['HARVEST']], 'market': [['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['FEED'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['EAST'], ['EAST'], ['EAST'], ['CARE'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['DROP'], ['CARE'], ['WATER'], ['WEST'], ['DROP'], ['EAST'], ['EAST'], ['WATER'], ['DROP'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [['SELL', 'MELON', 12], ['SELL', 'MELON', 6]]}, {'farmer': ['CARE'], 'hands': [['PICKUP', 'WHEAT', 4], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['WEST'], ['DROP'], ['EAST'], ['NORTH'], ['WEST'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'MELON', 6], ['BUY_PRODUCT', 'WHEAT', 12]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WEST'], ['SOUTH'], ['EAST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['EAST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['DROP'], ['NORTH'], ['WEST'], ['NORTH'], ['DROP']], 'market': [['SELL', 'MELON', 6], ['SELL', 'MILK', 6]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['FEED'], ['WATER'], ['SOUTH'], ['WEST'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['PICKUP', 'WHEAT', 2]], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WEST'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['NORTH'], ['SOUTH'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['CARE'], ['EAST'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['WATER'], ['FEED'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['WEST'], ['FEED'], ['WATER'], ['SOUTH'], ['CARE'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['EAST'], ['WEST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WEST'], ['FEED'], ['WATER'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['CARE'], ['WEST'], ['WATER'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['WEST'], ['EAST'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['HARVEST'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WEST'], ['PASS'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['FEED'], ['FEED']], 'market': [['SELL', 'WHEAT', 7]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['CARE'], ['PASS'], ['PASS'], ['NORTH'], ['PASS'], ['WATER'], ['WATER'], ['WATER'], ['CARE'], ['CARE']], 'market': []}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 12], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['WEST'], ['PICKUP', 'WHEAT', 4], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['FEED'], ['FEED'], ['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['PICKUP', 'WHEAT', 4], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['CARE'], ['CARE'], ['WEST'], ['NORTH'], ['FEED'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['CARE'], ['WATER'], ['SOUTH'], ['NORTH'], ['FEED'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['NORTH'], ['SOUTH'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['HARVEST'], ['CARE'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FEED'], ['NORTH'], ['FEED'], ['WEST'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['CARE'], ['FEED'], ['CARE'], ['FEED'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['NORTH'], ['FERTILIZE']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['WEST'], ['CARE'], ['EAST'], ['FEED'], ['WEST'], ['WEST'], ['SOUTH'], ['FEED'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['EAST'], ['CARE'], ['WATER'], ['WATER'], ['SOUTH'], ['CARE'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['DROP'], 'hands': [['FEED'], ['EAST'], ['CARE'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FERTILIZE']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['EAST'], ['WATER'], ['WATER'], ['DROP'], ['NORTH'], ['WATER']], 'market': [['SELL', 'MILK', 5]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['SOUTH'], ['FEED'], ['EAST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['EAST'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['HARVEST'], ['SOUTH'], ['CARE'], ['DROP'], ['NORTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WEST'], ['SOUTH']], 'market': [['SELL', 'MELON', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['WATER'], ['WATER'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['NORTH'], ['NORTH'], ['EAST'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['EAST'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['HARVEST'], ['FERTILIZE'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['NORTH'], ['WEST'], ['WEST'], ['FEED'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['CARE'], ['WATER'], ['EAST'], ['WEST'], ['NORTH'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['PLANT', 'WHEAT']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['EAST'], ['SOUTH'], ['PASS'], ['PASS'], ['FEED'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'WHEAT', 7]]}, {'farmer': ['NORTH'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['EAST'], ['EAST'], ['SOUTH'], ['PASS'], ['PASS'], ['CARE'], ['SOUTH'], ['PASS']], 'market': []}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'FERTILIZER', 9], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE']]}, {'farmer': ['SOUTH'], 'hands': [['DROP'], ['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3]], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['DROP'], 'hands': [['WEST'], ['CARE'], ['CARE'], ['WEST'], ['HARVEST'], ['EAST'], ['WEST'], ['WEST'], ['NORTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['SOUTH'], ['CARE'], ['SOUTH'], ['EAST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['DROP'], ['WATER'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['EAST'], ['CARE'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['EAST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['EAST'], ['FERTILIZE'], ['FEED']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['FEED'], ['WEST'], ['WEST'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WEST'], ['CARE']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['CARE'], ['CARE'], ['NORTH'], ['WATER'], ['SOUTH'], ['WATER'], ['EAST'], ['FERTILIZE'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['DROP'], ['WATER'], ['FEED']], 'market': [['SELL', 'MILK', 3]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['FEED'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['PLANT', 'STRAWBERRY'], ['WEST'], ['SOUTH'], ['CARE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['CARE'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['FERTILIZE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['NORTH'], ['WEST'], ['WATER'], ['DROP'], ['PLANT', 'WHEAT'], ['NORTH']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['NORTH'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['FERTILIZE'], ['EAST'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'MILK', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['WATER'], ['SOUTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['EAST'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WATER'], ['EAST'], ['SOUTH'], ['EAST'], ['EAST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['EAST'], ['PASS'], ['DROP']], 'market': [['SELL', 'EGG', 8], ['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['PASS'], ['SOUTH'], ['CARE'], ['PASS'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['PASS']], 'market': [['SELL', 'FERTILIZER', 3], ['SELL', 'EGG', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 4], 'hands': [], 'market': [['SELL', 'FERTILIZER', 7], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['SOUTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 1], ['HIRE'], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['DROP'], ['DROP'], ['WEST'], ['FEED'], ['WATER'], ['HARVEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 4]], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['FEED'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['WEST'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['NORTH'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['FEED'], ['EAST'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['FEED']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['CARE']], 'market': []}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WEST'], ['HARVEST'], ['PLANT', 'STRAWBERRY'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['FEED'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['FEED']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['FERTILIZE'], 'hands': [['FEED'], ['CARE'], ['FEED'], ['CARE'], ['WEST'], ['FERTILIZE'], ['WATER'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['FEED'], ['CARE'], ['WATER'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['HARVEST'], ['WEST'], ['CARE']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['CARE'], ['HARVEST'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['HARVEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['WEST'], ['WATER'], ['WEST'], ['FEED']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['SOUTH'], ['HARVEST'], ['FEED'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['CARE']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WEST'], ['NORTH'], ['CARE'], ['WATER'], ['EAST'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WEST'], ['HARVEST'], ['WATER'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['WEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['FERTILIZE'], ['WEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['NORTH'], ['WATER'], ['EAST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['WATER'], ['PLANT', 'CARROT'], ['SOUTH'], ['HARVEST'], ['WEST'], ['EAST']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WATER'], ['NORTH'], ['WEST'], ['EAST'], ['WATER'], ['SOUTH'], ['NORTH'], ['FERTILIZE'], ['EAST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['SOUTH'], ['HARVEST'], ['WATER'], ['EAST'], ['EAST'], ['WATER'], ['EAST'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['EAST'], ['HARVEST'], ['EAST'], ['SOUTH'], ['WATER'], ['EAST'], ['HARVEST'], ['EAST'], ['EAST'], ['WATER']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['PLANT', 'CARROT'], ['EAST'], ['EAST'], ['SOUTH'], ['WATER'], ['PASS'], ['EAST'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 4]]}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['WATER'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['WATER'], ['PASS'], ['EAST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'FERTILIZER', 9], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'FERTILIZER', 1], ['HIRE']]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['NORTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['FEED'], ['EAST'], ['WEST'], ['WEST'], ['WEST'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['NORTH'], ['EAST'], ['SOUTH'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WATER'], ['FERTILIZE'], ['WEST'], ['WEST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['NORTH'], ['EAST'], ['WATER'], ['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WEST'], ['FEED'], ['NORTH'], ['WATER'], ['WEST'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['FEED'], ['FEED'], ['CARE'], ['FEED'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 5], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['WEST'], ['EAST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WEST'], ['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['WEST'], ['FERTILIZE'], ['WEST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'CARROT'], ['PLANT', 'WHEAT'], ['WEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['HARVEST'], ['WEST'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['WEST'], ['EAST'], ['SOUTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['EAST'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['FEED'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['EAST'], ['SOUTH'], ['EAST'], ['PLANT', 'CARROT'], ['PLANT', 'CARROT'], ['PLANT', 'CARROT'], ['CARE'], ['SOUTH'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['DROP'], ['EAST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['DROP'], ['FERTILIZE'], ['HARVEST'], ['EAST'], ['EAST'], ['EAST'], ['NORTH'], ['FEED'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 3]]}, {'farmer': ['EAST'], 'hands': [['PASS'], ['WATER'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['WATER'], ['WATER'], ['NORTH'], ['CARE'], ['DROP'], ['HARVEST']], 'market': [['SELL', 'FERTILIZER', 3], ['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['PASS'], ['PASS'], ['WATER'], ['PASS'], ['SOUTH'], ['PASS'], ['WATER'], ['PASS'], ['PASS'], ['EAST']], 'market': [['SELL', 'EGG', 8], ['SELL', 'EGG', 8]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'MILK', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 2], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 4], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'FERTILIZER', 4], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['WEST']], 'market': [['SELL', 'WOOL', 1], ['HIRE'], ['HIRE'], ['BUY_SEED', 'STRAWBERRY', 1], ['BUY_SEED', 'STRAWBERRY', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['DROP'], ['WEST'], ['FEED'], ['EAST'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['CARE'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['WEST'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['EAST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['SOUTH'], ['SOUTH'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['FERTILIZE'], ['EAST'], ['WEST'], ['NORTH'], ['WEST']], 'market': [['SELL', 'WHEAT', 13]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['EAST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 3]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WEST'], ['CARE'], ['WEST'], ['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['NORTH'], ['PLANT', 'STRAWBERRY']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['CARE'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['EAST'], ['SOUTH'], ['FERTILIZE'], ['FEED'], ['FERTILIZE'], ['WATER'], ['WATER'], ['NORTH'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['CARE'], ['WATER'], ['HARVEST'], ['NORTH'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['PLANT', 'STRAWBERRY'], ['FERTILIZE'], ['WATER'], ['EAST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FERTILIZE'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['NORTH'], ['FERTILIZE'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['PLANT', 'STRAWBERRY'], ['HARVEST'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['PLANT', 'STRAWBERRY']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WEST'], ['PLANT', 'STRAWBERRY'], ['PLANT', 'STRAWBERRY'], ['WATER'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['EAST'], ['EAST'], ['PLANT', 'STRAWBERRY']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['PLANT', 'STRAWBERRY'], ['PLANT', 'WHEAT'], ['WEST'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['FERTILIZE'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['SOUTH'], ['WEST'], ['SOUTH'], ['NORTH'], ['WEST'], ['EAST'], ['HARVEST'], ['EAST'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['FERTILIZE'], ['WEST'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER'], ['SOUTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['HARVEST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['WATER'], ['SOUTH'], ['HARVEST'], ['EAST'], ['EAST']], 'market': [['SELL', 'WHEAT', 6]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS'], ['FERTILIZE'], ['FERTILIZE']], 'market': []}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'FERTILIZER', 5], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['WATER'], ['FEED'], ['WEST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['EAST'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['CARE'], ['WEST'], ['FEED'], ['WATER'], ['SOUTH'], ['NORTH'], ['NORTH'], ['EAST'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['HARVEST'], ['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['EAST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['WEST'], ['SOUTH'], ['HARVEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'WHEAT', 3], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['WATER'], ['EAST'], ['HARVEST'], ['WEST'], ['HARVEST'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['CARE'], ['WEST'], ['FEED'], ['DROP'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['WEST'], ['NORTH'], ['WATER'], ['EAST']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WEST'], ['FEED'], ['CARE'], ['EAST'], ['PLANT', 'CARROT'], ['EAST'], ['HARVEST'], ['WEST'], ['HARVEST'], ['WEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['WEST'], ['DROP'], ['WEST'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'MELON', 6]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WEST'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['DROP'], ['SOUTH'], ['FERTILIZE'], ['SOUTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['EAST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WEST'], ['SOUTH'], ['PICKUP', 'WHEAT', 2], ['SOUTH'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['WEST'], ['WEST'], ['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['EAST'], ['NORTH'], ['SOUTH'], ['WEST'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 3], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['WEST'], ['EAST'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['DROP']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['SOUTH'], ['NORTH'], ['PLANT', 'WHEAT'], ['WEST'], ['WEST'], ['SOUTH'], ['FEED'], ['DROP'], ['WATER'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['HARVEST'], ['FERTILIZE'], ['DIG'], ['WATER'], ['SOUTH'], ['DROP'], ['EAST'], ['CARE'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 8]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['PLANT', 'CARROT'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['WATER'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['NORTH'], ['DROP'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['WEST'], ['HARVEST'], ['WEST'], ['EAST'], ['WEST'], ['EAST'], ['EAST'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['WEST'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['WEST'], ['HARVEST'], ['WEST'], ['FEED'], ['EAST'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['FERTILIZE'], ['CARE'], ['WATER'], ['CARE'], ['EAST'], ['WATER'], ['EAST']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['HARVEST'], 'hands': [['EAST'], ['PASS'], ['PASS'], ['HARVEST'], ['HARVEST'], ['WATER'], ['PASS'], ['PASS'], ['PASS'], ['HARVEST'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 4], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 8], ['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['WEST'], ['FEED'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['CARE'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['WEST'], ['CARE'], ['WEST'], ['WATER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['CARE'], ['CARE'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['SOUTH'], ['WEST'], ['WEST'], ['CARE'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['FEED'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['CARE'], ['FEED'], ['WEST'], ['WATER'], ['NORTH'], ['EAST'], ['WATER'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WEST'], ['HARVEST'], ['HARVEST'], ['CARE'], ['FERTILIZE'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WATER'], ['FEED'], ['SOUTH'], ['NORTH'], ['EAST'], ['WATER'], ['PLANT', 'CARROT'], ['WEST'], ['EAST'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['EAST'], ['CARE'], ['WATER'], ['EAST'], ['WATER'], ['WEST'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['FERTILIZE'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['EAST'], ['WATER'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['EAST'], ['WEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['WEST'], ['WEST'], ['SOUTH'], ['PLANT', 'CARROT'], ['HARVEST'], ['WATER'], ['DIG'], ['HARVEST'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'CARROT'], ['WEST'], ['PLANT', 'CARROT'], ['WEST'], ['PLANT', 'CARROT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['EAST'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['EAST'], ['NORTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['WATER'], ['EAST'], ['PLANT', 'CARROT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['PLANT', 'CARROT'], ['HARVEST'], ['WATER'], ['HARVEST'], ['EAST'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['EAST'], ['WATER'], ['PLANT', 'CARROT'], ['SOUTH'], ['SOUTH'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['EAST'], ['WATER'], ['EAST'], ['SOUTH'], ['EAST'], ['WATER']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['PASS'], ['PASS'], ['PASS'], ['SOUTH'], ['WATER'], ['PASS'], ['PASS'], ['SOUTH'], ['PASS'], ['PASS']], 'market': [['SELL', 'CARROT', 6]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['FEED'], ['WEST'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['EAST'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['SOUTH'], ['CARE'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['EAST'], ['HARVEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['EAST'], ['EAST'], ['WEST']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['CARE'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['WEST'], ['FEED'], ['PLANT', 'WHEAT'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['FEED'], ['CARE'], ['WATER'], ['SOUTH'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['CARE'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['WEST'], ['WEST'], ['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['WATER'], ['WEST'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['HARVEST'], ['WEST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['WEST'], ['WEST'], ['EAST'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['WEST'], ['WEST'], ['EAST'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['DROP'], ['EAST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['WEST'], 'hands': [['DROP'], ['SOUTH'], ['WATER'], ['EAST'], ['DROP'], ['WATER'], ['DROP'], ['SOUTH'], ['EAST'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 12], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['WATER'], ['HARVEST'], ['FEED'], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['FERTILIZE'], ['HARVEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['DIG'], 'hands': [['FEED'], ['HARVEST'], ['PLANT', 'WHEAT'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['EAST'], ['WATER'], ['DIG']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['CARE'], ['PLANT', 'WHEAT'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['EAST'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'CARROT', 13]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['WEST'], ['WATER'], ['SOUTH'], ['DROP'], ['EAST'], ['EAST'], ['EAST'], ['NORTH'], ['EAST'], ['NORTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['SOUTH'], 'hands': [['FEED'], ['NORTH'], ['EAST'], ['FEED'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['FEED'], ['NORTH'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['CARE'], ['FERTILIZE'], ['WATER'], ['CARE'], ['DROP'], ['NORTH'], ['NORTH'], ['CARE'], ['NORTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WEST'], ['SOUTH'], ['SOUTH'], ['PASS'], ['DROP'], ['EAST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'WHEAT', 8], ['SELL', 'EGG', 4]]}, {'farmer': ['FERTILIZE'], 'hands': [['FEED'], ['WATER'], ['WATER'], ['FEED'], ['PASS'], ['PASS'], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['EAST']], 'market': [['SELL', 'CARROT', 2], ['SELL', 'EGG', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 3], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 4], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 4], ['PICKUP', 'FERTILIZER', 4], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['PICKUP', 'FERTILIZER', 4]], 'market': [['SELL', 'STRAWBERRY', 4], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['WEST'], ['FEED'], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['CARE'], ['FERTILIZE'], ['WATER'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['HARVEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['WEST'], ['WATER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['FEED'], ['EAST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER'], ['EAST'], ['NORTH'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['CARE'], ['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['SOUTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['SOUTH'], ['WEST'], ['WEST'], ['NORTH'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['FERTILIZE']], 'market': []}, {'farmer': ['EAST'], 'hands': [['CARE'], ['FEED'], ['FEED'], ['FEED'], ['NORTH'], ['WATER'], ['EAST'], ['EAST'], ['NORTH'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['EAST'], ['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['HARVEST'], ['FERTILIZE'], ['FERTILIZE'], ['NORTH'], ['FERTILIZE'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['CARE'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['FEED'], ['WEST'], ['NORTH'], ['NORTH'], ['EAST'], ['WATER'], ['NORTH'], ['WEST'], ['WATER'], ['NORTH'], ['SOUTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['NORTH'], ['NORTH'], ['FERTILIZE'], ['SOUTH'], ['FERTILIZE'], ['WEST'], ['NORTH'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['CARE'], ['NORTH'], ['FEED'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['WATER'], ['DIG'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['CARE'], ['NORTH'], ['NORTH'], ['WEST'], ['NORTH'], ['DIG'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['FERTILIZE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['HARVEST'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FERTILIZE'], ['SOUTH'], ['EAST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['WEST'], ['EAST'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['DIG'], ['SOUTH'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['DIG'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['NORTH'], ['WEST'], ['EAST'], ['PLANT', 'WHEAT'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['NORTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['FERTILIZE'], ['WEST'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 8]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['PASS'], ['PASS'], ['WATER'], ['SOUTH'], ['FERTILIZE'], ['WEST'], ['WATER'], ['PASS']], 'market': [['SELL', 'EGG', 3]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'STRAWBERRY', 6], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['EAST'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MELON', 6], ['SELL', 'FERTILIZER', 8], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['FEED'], ['WEST'], ['WEST'], ['EAST'], ['HARVEST'], ['EAST'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['SOUTH'], ['CARE'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['HARVEST'], ['EAST'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['FEED'], ['COLLECT_FERTILIZER'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['FEED'], 'hands': [['HARVEST'], ['CARE'], ['WEST'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['WEST'], ['FEED'], ['WATER'], ['EAST'], ['SOUTH'], ['WEST'], ['DIG'], ['SOUTH'], ['EAST'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['FEED'], ['CARE'], ['WEST'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['HARVEST'], ['FERTILIZE']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['SOUTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['SOUTH'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WEST'], ['CARE'], ['HARVEST'], ['WATER'], ['HARVEST'], ['SOUTH'], ['PLANT', 'WHEAT'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['FEED'], 'hands': [['WEST'], ['WEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['DIG'], ['DROP'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['CARE'], 'hands': [['DROP'], ['WATER'], ['FERTILIZE'], ['WATER'], ['SOUTH'], ['WATER'], ['FEED'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 6], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'WHEAT', 2], ['SOUTH'], ['WATER'], ['NORTH'], ['WEST'], ['HARVEST'], ['CARE'], ['WATER'], ['NORTH'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['FEED'], ['WATER'], ['NORTH'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['NORTH'], ['WEST'], ['NORTH'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['EAST'], 'hands': [['CARE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['DIG'], ['WEST'], ['WATER'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['EAST'], 'hands': [['HARVEST'], ['PLANT', 'WHEAT'], ['EAST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['CARE'], ['EAST'], ['HARVEST'], ['SOUTH'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['DROP'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['SOUTH'], ['WATER'], ['SOUTH'], ['DROP'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['WATER'], ['SOUTH'], ['EAST'], ['NORTH'], ['PLANT', 'CARROT'], ['WEST'], ['EAST'], ['DROP'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['SOUTH'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['WATER'], ['FEED'], ['EAST'], ['WEST'], ['NORTH'], ['WATER']], 'market': [['SELL', 'CARROT', 5], ['SELL', 'EGG', 4]]}, {'farmer': ['WATER'], 'hands': [['DROP'], ['PASS'], ['PASS'], ['PASS'], ['CARE'], ['WEST'], ['CARE'], ['EAST'], ['PASS'], ['PASS'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 8], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'CARROT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['WEST'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'FERTILIZER', 3], ['HIRE'], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['FEED'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['CARE'], ['FEED'], ['EAST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['NORTH'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WEST'], ['WEST'], ['WEST'], ['EAST'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['WATER'], ['FEED'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['SOUTH'], ['CARE'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['WATER'], ['NORTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['CARE'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['FEED'], ['FERTILIZE'], ['HARVEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['HARVEST'], ['SOUTH'], ['FEED'], ['WEST'], ['CARE'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['CARE'], ['WATER'], ['EAST'], ['EAST'], ['WATER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['WEST'], ['HARVEST'], ['EAST'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['NORTH'], ['NORTH'], ['EAST'], ['WEST'], ['EAST'], ['WATER'], ['FERTILIZE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['WATER'], ['WATER'], ['FEED'], ['WEST'], ['FEED'], ['HARVEST'], ['WATER'], ['SOUTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['WEST'], ['CARE'], ['FERTILIZE'], ['CARE'], ['SOUTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['WEST'], ['HARVEST'], ['WATER'], ['WATER'], ['NORTH'], ['FEED'], ['NORTH'], ['FEED'], ['HARVEST'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['EAST'], ['WATER'], ['CARE'], ['EAST'], ['CARE'], ['SOUTH'], ['PLANT', 'WHEAT'], ['FERTILIZE']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['SOUTH'], 'hands': [['CARE'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST'], ['HARVEST'], ['DROP'], ['PLANT', 'WHEAT'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['SOUTH'], ['WEST'], ['WATER'], ['EAST'], ['NORTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['EAST']], 'market': [['SELL', 'CARROT', 7], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['EAST'], 'hands': [['PASS'], ['WATER'], ['SOUTH'], ['PASS'], ['FERTILIZE'], ['HARVEST'], ['SOUTH'], ['DROP'], ['WEST'], ['FERTILIZE'], ['EAST']], 'market': [['SELL', 'WHEAT', 8], ['SELL', 'EGG', 8], ['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'WHEAT', 16], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'FERTILIZER', 6], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['DROP'], ['FEED'], ['NORTH'], ['WEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['EAST'], ['NORTH'], ['NORTH'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['CARE'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['WEST'], ['EAST'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['NORTH'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['HARVEST'], ['WATER'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST'], ['FERTILIZE'], ['DIG'], ['PLANT', 'WHEAT'], ['EAST'], ['WATER'], ['EAST'], ['WEST'], ['DIG']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['CARE'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['SOUTH'], ['WATER'], ['SOUTH'], ['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['FERTILIZE'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['FEED'], ['SOUTH'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['EAST'], ['WATER'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['FEED'], ['FEED'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['DIG'], ['NORTH'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['CARE'], ['WEST'], ['DIG'], ['PLANT', 'WHEAT'], ['WATER'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['NORTH'], ['DIG']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['EAST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['FERTILIZE'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['NORTH'], ['WATER'], ['WATER'], ['SOUTH'], ['HARVEST'], ['SOUTH'], ['SOUTH'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['SOUTH'], ['DIG'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['DIG'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['NORTH']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['COLLECT_FERTILIZER'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['SOUTH'], ['SOUTH'], ['WATER'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WATER'], ['WATER'], ['SOUTH'], ['DIG'], ['WEST'], ['WATER'], ['SOUTH'], ['WEST'], ['NORTH'], ['DIG']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['HARVEST'], ['EAST'], ['WATER'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['NORTH'], ['SOUTH'], ['DROP'], ['NORTH'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'STRAWBERRY', 6]]}, {'farmer': ['SOUTH'], 'hands': [['COLLECT_FERTILIZER'], ['PLANT', 'WHEAT'], ['DIG'], ['SOUTH'], ['WATER'], ['WATER'], ['HARVEST'], ['FEED'], ['PICKUP', 'WHEAT', 2], ['WATER'], ['WATER']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['NORTH'], ['WEST'], ['DIG'], ['CARE'], ['NORTH'], ['EAST'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['EAST'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['SOUTH'], ['WEST'], ['EAST'], ['PLANT', 'CARROT'], ['DIG'], ['NORTH'], ['WATER'], ['EAST'], ['FEED'], ['WEST'], ['DIG']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['WATER'], 'hands': [['DROP'], ['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['NORTH'], ['NORTH'], ['EAST'], ['CARE'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 2], ['SELL', 'EGG', 8]]}, {'farmer': ['SOUTH'], 'hands': [['PASS'], ['FERTILIZE'], ['EAST'], ['EAST'], ['HARVEST'], ['WATER'], ['NORTH'], ['DROP'], ['PASS'], ['PASS'], ['WATER']], 'market': [['SELL', 'FERTILIZER', 2], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'WHEAT', 16], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['PICKUP', 'WHEAT', 3], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['EAST'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 3], ['NORTH'], ['NORTH']], 'market': [['SELL', 'WOOL', 1], ['SELL', 'FERTILIZER', 3], ['HIRE']]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['DROP'], ['WEST'], ['FEED'], ['WATER'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['CARE'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['CARE'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['FEED'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['CARE'], ['CARE'], ['FEED'], ['WATER'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['WATER'], ['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['CARE'], ['HARVEST'], ['WEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['FERTILIZE']], 'market': []}, {'farmer': ['WATER'], 'hands': [['FEED'], ['CARE'], ['HARVEST'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['WEST'], ['FEED'], ['WATER'], ['WATER'], ['WEST'], ['FERTILIZE'], ['WEST'], ['EAST'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['FEED'], ['CARE'], ['SOUTH'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['NORTH'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['CARE'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['HARVEST'], ['PLANT', 'CARROT'], ['WATER'], ['HARVEST'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['HARVEST'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['NORTH']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['PLANT', 'CARROT'], ['WATER'], ['WATER'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WEST'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER'], ['WATER'], ['WEST'], ['EAST'], ['HARVEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['FERTILIZE'], ['HARVEST'], ['HARVEST'], ['WEST'], ['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['PLANT', 'CARROT']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['EAST'], 'hands': [['PLANT', 'CARROT'], ['WATER'], ['SOUTH'], ['PLANT', 'CARROT'], ['WEST'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['DROP'], ['WATER'], ['WATER'], ['WEST'], ['PLANT', 'CARROT'], ['NORTH']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'EGG', 4]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['FERTILIZE'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['WEST'], ['WEST'], ['WATER'], ['WATER'], ['EAST']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'CARROT'], ['WATER'], ['PLANT', 'CARROT'], ['FEED'], ['DROP'], ['FERTILIZE'], ['FERTILIZE'], ['HARVEST'], ['EAST'], ['EAST']], 'market': [['SELL', 'MILK', 4]]}, {'farmer': ['EAST'], 'hands': [['WATER'], ['EAST'], ['WATER'], ['CARE'], ['PASS'], ['WATER'], ['WATER'], ['PLANT', 'CARROT'], ['DIG'], ['EAST']], 'market': [['SELL', 'WHEAT', 2], ['SELL', 'EGG', 4]]}, {'farmer': ['CARE'], 'hands': [['SOUTH'], ['EAST'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['WATER'], ['SOUTH'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 3], ['SELL', 'WOOL', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 16], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['WEST'], ['PICKUP', 'FERTILIZER', 4], ['WEST'], ['PICKUP', 'FERTILIZER', 4], ['WEST'], ['NORTH']], 'market': [['SELL', 'WOOL', 1], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['CARE'], ['CARE'], ['SOUTH'], ['NORTH'], ['EAST'], ['WEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['FEED'], ['FERTILIZE'], ['EAST'], ['COLLECT_FERTILIZER'], ['WEST'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['NORTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WEST'], ['CARE'], ['WATER'], ['EAST'], ['WEST'], ['FERTILIZE'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['FEED'], ['FEED'], ['COLLECT_FERTILIZER'], ['WEST'], ['FERTILIZE'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['EAST'], ['FERTILIZE'], ['HARVEST']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['CARE'], ['CARE'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['SOUTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['WEST'], ['FEED'], ['HARVEST'], ['NORTH'], ['WEST'], ['FERTILIZE'], ['WATER'], ['EAST'], ['WEST'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['FEED'], ['FEED'], ['CARE'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['COLLECT_FERTILIZER'], ['WATER'], ['WATER'], ['HARVEST'], ['WEST'], ['NORTH'], ['WATER'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['CARE'], 'hands': [['HARVEST'], ['HARVEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WATER'], ['FERTILIZE']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['CARE'], ['SOUTH'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['HARVEST'], ['WATER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['EAST'], ['WATER'], ['FERTILIZE'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FEED'], 'hands': [['FERTILIZE'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['WEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WATER'], ['FERTILIZE'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['FERTILIZE'], ['NORTH'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WATER'], ['SOUTH'], ['EAST'], ['WATER'], ['SOUTH'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['WATER'], ['FERTILIZE'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['FEED'], 'hands': [['FERTILIZE'], ['WEST'], ['FERTILIZE'], ['EAST'], ['NORTH'], ['WATER'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['PLANT', 'CARROT']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['CARE'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['EAST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['EAST'], ['WATER'], ['EAST'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['HARVEST'], ['EAST'], ['SOUTH'], ['EAST'], ['PLANT', 'CARROT'], ['WATER'], ['EAST'], ['WEST'], ['EAST'], ['EAST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['NORTH'], 'hands': [['WEST'], ['PLANT', 'CARROT'], ['HARVEST'], ['DROP'], ['PLANT', 'CARROT'], ['WATER'], ['HARVEST'], ['EAST'], ['WATER'], ['WATER'], ['EAST']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['FERTILIZE'], 'hands': [['WEST'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['PLANT', 'CARROT'], ['EAST'], ['HARVEST'], ['HARVEST'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 4]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['SOUTH'], ['WEST'], ['DROP'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['PLANT', 'CARROT'], ['PLANT', 'WHEAT'], ['FEED']], 'market': [['SELL', 'WHEAT', 8], ['SELL', 'CARROT', 4], ['SELL', 'EGG', 4]]}, {'farmer': ['FERTILIZE'], 'hands': [['DROP'], ['FERTILIZE'], ['WATER'], ['PASS'], ['WATER'], ['EAST'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['CARE']], 'market': [['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'WHEAT', 16], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['PICKUP', 'WHEAT', 3], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 3], ['NORTH'], ['NORTH']], 'market': [['SELL', 'MILK', 4], ['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE']]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['DROP'], ['DROP'], ['WEST'], ['FEED'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['EAST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['WEST'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['EAST'], ['FEED'], ['FEED'], ['WEST'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FERTILIZE'], ['CARE'], ['CARE'], ['FEED'], ['EAST'], ['WATER'], ['SOUTH'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['CARE'], ['WATER'], ['HARVEST'], ['WATER'], ['HARVEST'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['HARVEST'], ['PLANT', 'CARROT'], ['SOUTH'], ['PLANT', 'WHEAT'], ['WATER'], ['WEST'], ['EAST']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['FEED'], ['WEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['WATER'], ['FERTILIZE'], ['WATER'], ['HARVEST'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['COLLECT_FERTILIZER'], ['CARE'], ['FEED'], ['NORTH'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['PLANT', 'WHEAT'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'MILK', 4], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['EAST'], ['WEST'], ['CARE'], ['COLLECT_FERTILIZER'], ['EAST'], ['HARVEST'], ['WEST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['PLANT', 'CARROT']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['SOUTH'], ['HARVEST'], ['EAST'], ['NORTH'], ['NORTH'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['CARE'], ['WEST'], ['CARE'], ['HARVEST'], ['WATER'], ['WEST'], ['EAST'], ['WATER'], ['NORTH'], ['NORTH']], 'market': []}, {'farmer': ['PLANT', 'WHEAT'], 'hands': [['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['PLANT', 'WHEAT'], ['HARVEST'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['WATER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['WEST'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['DROP'], ['WATER'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['WEST'], ['SOUTH'], ['WATER'], ['WEST'], ['WATER'], ['WEST'], ['PICKUP', 'WHEAT', 2], ['EAST'], ['PLANT', 'CARROT'], ['PLANT', 'CARROT']], 'market': [['SELL', 'WHEAT', 8], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['FEED'], ['WEST'], ['WATER'], ['WEST'], ['WEST'], ['NORTH'], ['WATER'], ['EAST'], ['FERTILIZE'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['HARVEST'], ['SOUTH'], ['WATER'], ['FEED'], ['NORTH'], ['WEST'], ['FEED'], ['WATER'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['WEST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['CARE'], ['EAST'], ['WATER'], ['CARE'], ['SOUTH'], ['FERTILIZE'], ['WATER']], 'market': []}, {'farmer': ['WEST'], 'hands': [['FEED'], ['FERTILIZE'], ['HARVEST'], ['PLANT', 'CARROT'], ['WEST'], ['NORTH'], ['HARVEST'], ['NORTH'], ['FERTILIZE'], ['WATER'], ['NORTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['FEED'], ['DROP'], ['PLANT', 'CARROT'], ['FEED'], ['WATER'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['WATER'], ['CARE'], ['SOUTH'], ['PLANT', 'CARROT'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'WHEAT', 8]]}, {'farmer': ['EAST'], 'hands': [['FEED'], ['PLANT', 'CARROT'], ['EAST'], ['SOUTH'], ['DROP'], ['NORTH'], ['NORTH'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'FERTILIZER', 2], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['FERTILIZE'], 'hands': [['CARE'], ['WATER'], ['FERTILIZE'], ['EAST'], ['PASS'], ['PASS'], ['WATER'], ['HARVEST'], ['PASS'], ['SOUTH'], ['NORTH']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [], 'market': [['SELL', 'WHEAT', 16], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 3], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['NORTH'], ['SOUTH'], ['PICKUP', 'FERTILIZER', 4], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['FEED'], ['WEST'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['WATER'], ['CARE'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['EAST'], ['EAST'], ['SOUTH'], ['WEST'], ['NORTH'], ['NORTH'], ['WEST'], ['DIG']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['FERTILIZE'], ['SOUTH'], ['CARE'], ['EAST'], ['COLLECT_FERTILIZER'], ['WATER'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['FEED'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['WATER'], ['EAST'], ['HARVEST'], ['FERTILIZE'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['EAST'], ['CARE'], ['WEST'], ['HARVEST'], ['EAST'], ['PLANT', 'CARROT'], ['WEST'], ['FERTILIZE'], ['EAST'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['WEST'], ['FEED'], ['EAST'], ['NORTH'], ['WATER'], ['FERTILIZE'], ['WATER'], ['EAST'], ['NORTH'], ['WEST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['FEED'], ['CARE'], ['EAST'], ['EAST'], ['SOUTH'], ['WATER'], ['EAST'], ['WATER'], ['WATER'], ['FERTILIZE']], 'market': [['SELL', 'MILK', 2], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WEST'], 'hands': [['PLANT', 'WHEAT'], ['CARE'], ['HARVEST'], ['WATER'], ['EAST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['HARVEST'], ['EAST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['PLANT', 'CARROT'], ['WATER'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['PLANT', 'CARROT'], ['HARVEST'], ['WATER'], ['WATER'], ['PLANT', 'WHEAT'], ['WATER'], ['EAST'], ['NORTH']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'CARROT', 6]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['WEST'], ['SOUTH'], ['FERTILIZE'], ['WATER'], ['PLANT', 'CARROT'], ['WEST'], ['NORTH'], ['WATER'], ['NORTH'], ['WATER'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['WATER'], 'hands': [['WEST'], ['WATER'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['NORTH'], ['SOUTH'], ['WATER'], ['EAST'], ['WEST']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [['FEED'], ['WEST'], ['WEST'], ['WATER'], ['NORTH'], ['HARVEST'], ['FERTILIZE'], ['WEST'], ['HARVEST'], ['DIG'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['FERTILIZE'], ['FERTILIZE'], ['HARVEST'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['WATER'], ['FEED'], ['PLANT', 'CARROT'], ['PLANT', 'CARROT'], ['HARVEST']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['WATER'], ['WATER'], ['PLANT', 'CARROT'], ['WATER'], ['WATER'], ['NORTH'], ['CARE'], ['WATER'], ['WATER'], ['PLANT', 'CARROT']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['PLANT', 'CARROT'], 'hands': [['FEED'], ['SOUTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['WEST'], ['FERTILIZE'], ['SOUTH'], ['EAST'], ['EAST'], ['WATER']], 'market': [['SELL', 'CARROT', 10]]}, {'farmer': ['WATER'], 'hands': [['CARE'], ['WATER'], ['WATER'], ['SOUTH'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['WATER'], ['FEED'], ['WATER'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'EGG', 6]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['WEST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['CARE'], ['HARVEST'], ['HARVEST'], ['SOUTH']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['WEST'], ['PLANT', 'CARROT'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['EAST'], ['SOUTH'], ['EAST'], ['SOUTH'], ['NORTH']], 'market': [['SELL', 'WHEAT', 5]]}, {'farmer': ['FEED'], 'hands': [['FEED'], ['FERTILIZE'], ['WATER'], ['EAST'], ['FERTILIZE'], ['PLANT', 'CARROT'], ['NORTH'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['CARE'], 'hands': [['CARE'], ['WATER'], ['SOUTH'], ['WATER'], ['WATER'], ['WATER'], ['HARVEST'], ['FEED'], ['WATER'], ['DROP'], ['WATER']], 'market': [['SELL', 'WHEAT', 6], ['SELL', 'EGG', 4]]}, {'farmer': ['PICKUP', 'WHEAT', 2], 'hands': [], 'market': [['SELL', 'CARROT', 13], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['HARVEST'], ['HARVEST'], ['PICKUP', 'WHEAT', 2], ['COLLECT_FERTILIZER'], ['EAST'], ['SOUTH'], ['WEST'], ['WEST'], ['NORTH']], 'market': [['SELL', 'MILK', 2], ['SELL', 'WHEAT', 13], ['HIRE'], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['DROP'], ['DROP'], ['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['PICKUP', 'WHEAT', 3], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WEST'], ['NORTH'], ['WEST'], ['EAST']], 'market': []}, {'farmer': ['FEED'], 'hands': [['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['FEED'], ['NORTH'], ['PLANT', 'WHEAT'], ['SOUTH'], ['WEST'], ['PLANT', 'WHEAT'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER']], 'market': []}, {'farmer': ['CARE'], 'hands': [['FEED'], ['FEED'], ['CARE'], ['WATER'], ['WATER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['WATER'], ['NORTH'], ['HARVEST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['CARE'], ['CARE'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['NORTH'], ['WATER'], ['WEST'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['PLANT', 'WHEAT']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['SOUTH'], ['SOUTH'], ['PLANT', 'WHEAT'], ['FEED'], ['SOUTH'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['HARVEST'], ['WATER']], 'market': [['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['FERTILIZE'], 'hands': [['FEED'], ['FEED'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WATER'], ['SOUTH'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['CARE'], ['CARE'], ['CARE'], ['NORTH'], ['CARE'], ['WATER'], ['WATER'], ['WEST'], ['HARVEST'], ['WATER'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 1]]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['HARVEST'], ['WATER'], ['PLANT', 'WHEAT'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'CARROT', 13]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['FEED'], ['WEST'], ['SOUTH'], ['WEST'], ['FERTILIZE'], ['HARVEST'], ['PLANT', 'WHEAT'], ['WEST'], ['WATER'], ['PLANT', 'WHEAT'], ['EAST']], 'market': [['BUY_SEED', 'WHEAT', 1], ['BUY_SEED', 'WHEAT', 1]]}, {'farmer': ['WEST'], 'hands': [['CARE'], ['WATER'], ['HARVEST'], ['FERTILIZE'], ['WATER'], ['NORTH'], ['WATER'], ['WATER'], ['EAST'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['EAST'], ['SOUTH'], ['WEST'], ['WATER'], ['NORTH'], ['WATER'], ['WEST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['NORTH'], 'hands': [['COLLECT_FERTILIZER'], ['WATER'], ['SOUTH'], ['SOUTH'], ['WATER'], ['WEST'], ['HARVEST'], ['PLANT', 'WHEAT'], ['FERTILIZE'], ['EAST'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['FERTILIZE'], 'hands': [['HARVEST'], ['HARVEST'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['SOUTH'], ['WATER'], ['WATER'], ['FEED'], ['NORTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['PLANT', 'WHEAT'], ['HARVEST'], ['HARVEST'], ['FEED'], ['WATER'], ['FERTILIZE'], ['NORTH'], ['EAST'], ['CARE'], ['NORTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['WATER'], ['PLANT', 'WHEAT'], ['PLANT', 'WHEAT'], ['CARE'], ['WEST'], ['WATER'], ['WATER'], ['EAST'], ['EAST'], ['NORTH']], 'market': [['SELL', 'WOOL', 1]]}, {'farmer': ['WATER'], 'hands': [['EAST'], ['EAST'], ['WATER'], ['WATER'], ['WEST'], ['WATER'], ['NORTH'], ['NORTH'], ['NORTH'], ['EAST'], ['NORTH']], 'market': [['SELL', 'FERTILIZER', 1]]}, {'farmer': ['HARVEST'], 'hands': [['FERTILIZE'], ['NORTH'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['HARVEST'], ['EAST'], ['WATER'], ['SOUTH'], ['DROP'], ['WATER']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['PASS'], 'hands': [['EAST'], ['HARVEST'], ['WEST'], ['SOUTH'], ['FEED'], ['SOUTH'], ['EAST'], ['HARVEST'], ['FERTILIZE'], ['NORTH'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 8]]}, {'farmer': ['PASS'], 'hands': [['SOUTH'], ['EAST'], ['FERTILIZE'], ['EAST'], ['CARE'], ['WATER'], ['EAST'], ['PASS'], ['WEST'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['EAST'], 'hands': [['NORTH'], ['NORTH'], ['EAST'], ['SOUTH'], ['HARVEST'], ['EAST'], ['EAST'], ['PASS'], ['FERTILIZE'], ['DROP'], ['SOUTH']], 'market': [['SELL', 'CARROT', 3]]}, {'farmer': ['WATER'], 'hands': [['WATER'], ['DROP'], ['FERTILIZE'], ['DROP'], ['PASS'], ['WATER'], ['NORTH'], ['PASS'], ['EAST'], ['PASS'], ['WATER']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'CARROT', 4], ['SELL', 'FERTILIZER', 1]]}, {'farmer': ['NORTH'], 'hands': [], 'market': [['SELL', 'CARROT', 20], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['NORTH']], 'market': [['SELL', 'STRAWBERRY', 4], ['SELL', 'WHEAT', 13], ['HIRE']]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['EAST'], ['WEST'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['COLLECT_FERTILIZER'], ['EAST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['NORTH'], ['EAST'], ['COLLECT_FERTILIZER'], ['FEED'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['NORTH'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['NORTH'], ['WATER'], ['HARVEST'], ['WATER'], ['WEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['COLLECT_FERTILIZER'], ['FERTILIZE'], ['COLLECT_FERTILIZER'], ['FEED'], ['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['COLLECT_FERTILIZER'], 'hands': [['HARVEST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['EAST'], ['WEST'], ['WEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['EAST'], ['FERTILIZE'], ['WEST'], ['WEST'], ['EAST'], ['FERTILIZE'], ['WATER'], ['WATER'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['WATER'], ['WATER'], ['WATER'], ['WEST'], ['WEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['HARVEST'], ['HARVEST'], ['SOUTH']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['HARVEST'], ['SOUTH'], ['WATER'], ['WATER'], ['HARVEST'], ['SOUTH'], ['EAST'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['HARVEST'], 'hands': [['WEST'], ['NORTH'], ['WATER'], ['HARVEST'], ['HARVEST'], ['EAST'], ['HARVEST'], ['WATER'], ['SOUTH'], ['WATER']], 'market': []}, {'farmer': ['NORTH'], 'hands': [['FERTILIZE'], ['WATER'], ['HARVEST'], ['NORTH'], ['WEST'], ['WATER'], ['WEST'], ['HARVEST'], ['SOUTH'], ['SOUTH']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['HARVEST'], ['WEST'], ['HARVEST'], ['WATER'], ['NORTH'], ['WEST'], ['NORTH'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['HARVEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['WATER'], ['WATER'], ['WATER'], ['FEED'], ['HARVEST']], 'market': [['SELL', 'MILK', 5], ['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['WATER'], ['FERTILIZE'], ['WEST'], ['SOUTH'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['HARVEST'], ['EAST']], 'market': []}, {'farmer': ['FERTILIZE'], 'hands': [['WATER'], ['HARVEST'], ['WATER'], ['FERTILIZE'], ['EAST'], ['SOUTH'], ['EAST'], ['SOUTH'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['NORTH'], ['HARVEST'], ['WATER'], ['EAST'], ['SOUTH'], ['WATER'], ['WEST'], ['DROP'], ['HARVEST']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['WATER'], ['SOUTH'], ['EAST'], ['EAST'], ['WEST'], ['NORTH'], ['WEST'], ['HARVEST'], ['SOUTH']], 'market': [['SELL', 'CARROT', 7]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['HARVEST'], ['WATER'], ['EAST'], ['EAST'], ['WEST'], ['NORTH'], ['WEST'], ['DROP'], ['WEST']], 'market': [['SELL', 'WHEAT', 10]]}, {'farmer': ['EAST'], 'hands': [['WEST'], ['WEST'], ['HARVEST'], ['EAST'], ['SOUTH'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'EGG', 8]]}, {'farmer': ['WATER'], 'hands': [['NORTH'], ['WATER'], ['NORTH'], ['DROP'], ['DROP'], ['DROP'], ['EAST'], ['DROP'], ['NORTH'], ['WATER']], 'market': [['SELL', 'CARROT', 7], ['SELL', 'EGG', 4]]}, {'farmer': ['HARVEST'], 'hands': [['WATER'], ['HARVEST'], ['EAST'], ['WEST'], ['NORTH'], ['PICKUP', 'WHEAT', 2], ['NORTH'], ['NORTH'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'WHEAT', 13], ['SELL', 'STRAWBERRY', 2], ['SELL', 'WHEAT', 13]]}, {'farmer': ['SOUTH'], 'hands': [['HARVEST'], ['SOUTH'], ['FERTILIZE'], ['SOUTH'], ['NORTH'], ['FEED'], ['DROP'], ['NORTH'], ['WATER'], ['NORTH']], 'market': [['SELL', 'CARROT', 7], ['SELL', 'FERTILIZER', 3], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['SOUTH'], 'hands': [['SOUTH'], ['SOUTH'], ['WATER'], ['HARVEST'], ['HARVEST'], ['PASS'], ['PASS'], ['PASS'], ['PASS'], ['PASS']], 'market': [['SELL', 'EGG', 8], ['SELL', 'EGG', 8]]}, {'farmer': ['WEST'], 'hands': [], 'market': [['SELL', 'CARROT', 24], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE'], ['HIRE']]}, {'farmer': ['WEST'], 'hands': [['NORTH'], ['EAST'], ['HARVEST'], ['WEST'], ['NORTH'], ['EAST'], ['SOUTH'], ['WEST'], ['NORTH']], 'market': [['SELL', 'CARROT', 13], ['SELL', 'WHEAT', 13]]}, {'farmer': ['WEST'], 'hands': [['WATER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH'], ['EAST'], ['HARVEST'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['HARVEST'], ['WEST'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['WATER'], ['COLLECT_FERTILIZER'], ['WEST'], ['NORTH']], 'market': []}, {'farmer': ['WEST'], 'hands': [['WEST'], ['NORTH'], ['WEST'], ['COLLECT_FERTILIZER'], ['NORTH'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WATER']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['SOUTH'], ['HARVEST'], ['EAST'], ['SOUTH'], ['WEST'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['SOUTH'], 'hands': [['NORTH'], ['HARVEST'], ['SOUTH'], ['COLLECT_FERTILIZER'], ['WEST'], ['WATER'], ['WATER'], ['HARVEST'], ['EAST']], 'market': []}, {'farmer': ['WATER'], 'hands': [['WEST'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['WATER'], ['HARVEST'], ['HARVEST'], ['SOUTH'], ['HARVEST']], 'market': []}, {'farmer': ['HARVEST'], 'hands': [['NORTH'], ['HARVEST'], ['WATER'], ['SOUTH'], ['HARVEST'], ['NORTH'], ['WEST'], ['WATER'], ['COLLECT_FERTILIZER']], 'market': []}, {'farmer': ['SOUTH'], 'hands': [['WATER'], ['COLLECT_FERTILIZER'], ['HARVEST'], ['HARVEST'], ['WEST'], ['NORTH'], ['SOUTH'], ['HARVEST'], ['NORTH']], 'market': [['SELL', 'MILK', 2]]}, {'farmer': ['HARVEST'], 'hands': [['HARVEST'], ['EAST'], ['SOUTH'], ['NORTH'], ['SOUTH'], ['WEST'], ['HARVEST'], ['EAST'], ['WATER']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['WATER'], ['WATER'], ['EAST'], ['SOUTH'], ['WEST'], ['NORTH'], ['EAST'], ['HARVEST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['SOUTH'], ['HARVEST'], ['HARVEST'], ['NORTH'], ['SOUTH'], ['WEST'], ['NORTH'], ['EAST'], ['EAST']], 'market': []}, {'farmer': ['EAST'], 'hands': [['EAST'], ['SOUTH'], ['NORTH'], ['DROP'], ['WATER'], ['HARVEST'], ['NORTH'], ['NORTH'], ['WATER']], 'market': [['SELL', 'STRAWBERRY', 2]]}, {'farmer': ['EAST'], 'hands': [['EAST'], ['WEST'], ['NORTH'], ['NORTH'], ['HARVEST'], ['COLLECT_FERTILIZER'], ['EAST'], ['DROP'], ['HARVEST']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['SOUTH'], ['WEST'], ['EAST'], ['EAST'], ['EAST'], ['SOUTH'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'CARROT', 10]]}, {'farmer': ['DROP'], 'hands': [['DROP'], ['SOUTH'], ['EAST'], ['HARVEST'], ['EAST'], ['SOUTH'], ['DROP'], ['EAST'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 6], ['SELL', 'CARROT', 7]]}, {'farmer': ['NORTH'], 'hands': [['NORTH'], ['DROP'], ['NORTH'], ['DROP'], ['DROP'], ['DROP'], ['NORTH'], ['NORTH'], ['SOUTH']], 'market': [['SELL', 'STRAWBERRY', 2], ['SELL', 'FERTILIZER', 2], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['NORTH'], 'hands': [['EAST'], ['COLLECT_FERTILIZER'], ['DROP'], ['NORTH'], ['NORTH'], ['NORTH'], ['NORTH'], ['COLLECT_FERTILIZER'], ['WEST']], 'market': [['SELL', 'WHEAT', 20], ['SELL', 'EGG', 4], ['SELL', 'EGG', 4]]}, {'farmer': ['WEST'], 'hands': [['HARVEST'], ['DROP'], ['NORTH'], ['HARVEST'], ['NORTH'], ['HARVEST'], ['WEST'], ['SOUTH'], ['SOUTH']], 'market': [['SELL', 'WHEAT', 10], ['SELL', 'FERTILIZER', 2], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['SOUTH'], ['PASS'], ['PASS'], ['NORTH'], ['NORTH'], ['NORTH'], ['WEST'], ['DROP'], ['DROP']], 'market': [['SELL', 'EGG', 8], ['SELL', 'EGG', 4], ['SELL', 'EGG', 4]]}, {'farmer': ['WEST'], 'hands': [['DROP'], ['PASS'], ['PASS'], ['NORTH'], ['EAST'], ['NORTH'], ['WEST'], ['PASS'], ['PASS']], 'market': [['SELL', 'MILK', 6], ['SELL', 'CARROT', 3], ['SELL', 'FERTILIZER', 2]]}, {'farmer': ['WEST'], 'hands': [['PASS'], ['PASS'], ['PASS'], ['EAST'], ['EAST'], ['EAST'], ['WEST'], ['PASS'], ['PASS']], 'market': [['SELL', 'EGG', 1000], ['SELL', 'MILK', 1000], ['SELL', 'WOOL', 1000], ['SELL', 'WHEAT', 7]]}]
_PROXY=make_agent({0:_DEMO})
def demonstrated_proxy(observation,configuration=None):
    return _PROXY(observation,configuration)
demonstrated_proxy.telemetry=_PROXY.chassis.diagnostics
agent=demonstrated_proxy
