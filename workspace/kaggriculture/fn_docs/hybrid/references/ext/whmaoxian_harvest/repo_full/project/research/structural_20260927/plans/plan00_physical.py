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

# Standalone observation-guarded reconstruction of a public production plan.
import base64,json,zlib
_SCHEDULE=json.loads(zlib.decompress(base64.b85decode('c-rlK%Z?;Tj^w}OIS*+Mf5hH$s$#kelik^<#{^~@jYb1Iiv<?5hu*y{_TRTUBi!BGC=?2*YVMv{bE+uIc(_riR4OSH`SbsM_uv2a_y73!zrXu0e}4C;k3aqN?l14({g1!>umASHe|_-lm;dp%zyHsF|3ANe{pWZ8^vl2f^-n*3{{ENmet!4<-OKNvKmPjP=`Zj9{O<QZ{P_G%{o)_L=BMZ9?^nO$kDovP$@%yB^!Vc+fB3`4Prv@dPrrYD{?ohn!(aaL|K4A{zz^U3%P)Uge#7Nu{`~Ic`KO=Xz5cBqfByZKufPxd<4^tY>HEL_YK)(MdHc-v+pbMRKKz&8_|x;JPnSpI)%#xm+pzjAe|Y}%`HzdoW&uX>XRm+YpPzsH`G-$G{MY9n7ylfa^wY=ho;`~~^TCG~lRtmFUIpu9saJQ*cYd$$KEK3|oxd2GbiD@P*S~$fYvZqNyxMn5bDf>`Y}U)~29Kao9UBqXxN>N`>78$ZUZyPF9R049(M~2>SPg94SIaKUxcUMb%DjX3{A>dh0G8gg-tC%|205fC*0DQzu^Fv>UQNf2fbvogQ2-1bR*j^Am3}qJAAdeCm9qoEF0+p2xn8&tqobo@^6HsG*N$$+mybXH`W&CO7ms>#z>6K}W^4*kNzWMbyBz#UX%AjG+`<Istq5G{`lph?UC1mVzr?>R8PvR}>Y0yh&Xc<#pZf0Oo7I#^-yUJKcTAZk-dmU81j5vHQsVj2>vzRgX>^UM_f)ph#TNhk4;Obr&Z{-!{2lC%tb+?yNFIz@;E{F?xD6$COpkz>_7u8Ii4$qH2UZTV`lrN(nMlUG{&=sSg&z&)wYtQ#)$)Z)w1vZ<d$ew(#K)pp#qtQ?OQv0mGM~#`Jo6W?*UbCOotN?SDeyAd1?5+AmPjgJl-C-ba>8O)jH_PtGbhvK6G7{rzxwI(FVda8-RkDkzpXrUl(SdZFVreS>JvA=%$psrmg02(Km8kg^!i?pVgK{TTN``%Nb;D~pZf0er%%t{{ruO(Y3-JJGY9x<VR!Y%zW?#d&zZojm0RE+n=>hq|H;69wI#OmpJW!E(;qeI9DK#d=N{rL#Yr;9Ojg^zJ>eTFxy>%V=HgXpEW}A?@Ru9M@)tin;dK+^PI!ALSB2)%8|SXCYv-J<J>cWI#d67*Go{(3U#Lm>oV~)SjR_@5a9p2M4bvM@_<?Iv9o;wD6*4+@9HSi`eY%7Asw1!XnQw(}vu}MHHHq)C!<AjZ$_kPLg{jLqJ&8--b3^G&-QK&Z&0R}{*T8c$L%Un__HvOa3=`$5^?6}m->+{{l<m27DYz~}ieK1r+eW5en{fRx`O>4~^WiqoOfZoUSpJpkMD}%CEbR4mKTtwvF;tAzxS)ldRGMWB@>Xs{4)pp@p+WpdO1u<P_`L`PXzSX81X1>ja9_;Ly*|-abL{lzyuY-@o4j0Ok2Q4b#8oGF<uJnwWAwSkAAgofGQW)P0lDL<rj|5}+?PMyM&EvJbrA*sdJ4@A)=6fKm+}^<YQ@nb^W&uw7=bdT3WBLR8Edy_m&0`N3su__^_gC!-m8#v#?$@o^XH$Qn=aPYoR|8qT$_x07MD~x_!vqCWMbaEZF~OE1UL4u@58!@(Xy?3<kbRA{q=%&H{01@)z)38+b>tXeGi~6=cUH|l2pLF<;y+$T{r8J`NbL@X|b#ue%%WcxFKDwjNN|!@yCBn<pQf;e))O$8n4K(?>=9hLhmiWqE^+MYDn9+d~|6~grgAJ&pUGcubc}AEfpIm@hQL^0kq;TkCyIn{(8I5V$n(G>(ug-*l&vqVtZbx(YrYri=HdBt9`J*3Fx5P)EmtDI@tU4<>Os_P_t_mxozyFTYY?60l9pvv-h08Na10&@)?51xYYJPu7^uH`*^0?Y^ofq5B1*ErtkWB!=@3z9o^&et`mW<ERr6DOd-zaMEOw#k7RMcX?U{KdY)T+==^!Z+Z(^fC1+sD!0vh-Hs~t|;1kD0=j6O}0Zw+7h6sU_!JmcK1*wwr?3X3of|1nc^-Ys%T0M#J!u6Empk2~xq4#(ms;2kLpGzSEpCVUFAu8rVKXoiY3NB8!D9e647ob_CwjsEU5;PEW(No<=hT#bf1MWoro=w)bRNz}XvT&?GAXZM4s!RJ9S)OQl-qC0HM-Af9n7=*+Z3EC%!3Ey4Me}%_S_y$wsD25C03HFxn!y40l6?13&V4vG<E=pV)6YMCeEFy6AAkHeX^ZY?Vv#7BBTJlJf^<lQlDPmkdY^%8yD-&j+a-!#=PNlbM#AG+DZEN<!Rb(z?<6$?PbZ~~e+f|Au9UQkgMi9HnA%9oG8Evo?zgPRrlcD5^OfOO-gSBBN<}kqK`Y#2otpN-DX(7C9v$zUA2L(x@~Uc|6gU|nIa*o*)u46AUPv|Yl)-dYu)L`YdVS2yjG3R^cs*t2xBxTf6DeuJxY#z<BkZX1v?Q?IYQtaoTmrH+j0*h@{FFxp<`@>CEbj!EIYgD$C@?>@O=Yx~nT7;>)dqJnb+5Yp@S%L2$Yh&+W*^R;YBP?Y7gMi{P6ZOJa?P?l^AiKww2tm9UcdE3d(^AxcjyC5LcO=8$S*;f>^N<55#nXpu)5Dk21}KgN>6FdUmik`Xt9W|f%TeL+?2_cbhn_bSYLv(R?pk~IN#WzO|p)ZVI$tL#QE^@v0BXtPZc;`8(DM<gdV>sC>qd``vOAJ=uMtOOme?8N!Nu7hMr-PMP!4+mzoj<q-mviDvd^l7J=0amigMdv)bC)ZHA8aUJhh#LJ&|%NzA(yNrmKIarnOW4g-0MU0kGyPYL=0L+!<<1{ge>z@e=)zjKm#|6Db=8~C4$rs2NNf~(6%n<s(GU7UU>%pyu$$*lX6Z37JrHRue}#zD^-!G;Hf$egKbg=McWl+5yO?u2DWv^%KqP8L1J3+^@o=+l1Bi{DxR^GS9QMHpna#Y#8nSVIdGm{H!k?K>uM5@QD7Y+<&Se_MgJE%hyX;loWAHNzU>A$1*)cU-sG-}hBXE$2eGYF?GL!XE1V$Wpqs|K%4k55T@5ZRqfVG3gPR`N;JQw?c3;Ivdbm2UYvt;|PflpBY%+2#j7BShqBaRoxAhNNDcG8d;i`hwm#_hpHug|L+g#)=Mx1>9b_n#pz8R*#bdM6gD?;%}#zi$GaAg$`T%)YAtVi3`<o!aMrN^Itc~4VymUWluc6`b-QmK+F7E`Zn`4QX!g<htMJkCL?bKX!-LD>am1R>{20F0?QBYnW`H44900yyQ%+5oSN~A9`+a?OX&r}e#+-^A1=`qrxAPOL;Z%BD6Sr|hSb&?Y<A`PA`5QOhvpZDJ`iTWb@bTL)WR`Tyf)Bm9hqlqKB%SImgEq|Dtn81JMbHvcluY=W3WWf|T_)KZe`~SOc682PtN|GR>3aUG6rg88f{0?t{oA#nWsIS^Zr2x^|Fj!r+VPrN-<sLxzGmB;Q0d{XbS1NSU;Ku>jnGTkFIHX38VLUDG-wQL?b}-nzv$Iv1Z|C~&h6*VpBBse>Ej>2e-}$-gtP?_9f~*4*`r^~Z2_m1fjxPDt=DMdJ~!Yx70^gS>+rX%^G3&0oPls#4@rZ_M{Zs0=y*D|q69aIgaZ6`D>yk23Oe+OFNJ49&K&YtDZxdN-pR3jw6X4}cDL|75HA3mNH~$@?1^Arl=pGh3^^r6rs^bhH{qmZl#YhDtZK4rPYC=M*~Z%h7Q-1Pp+)bV5$WO6KAn6<9#!<>(5dDGX-h1d`24%y>HH~G_`MKA89*-=I@WA)$qB47Gf6t}nM#@9Qye*LU*!@A^^gHr_vm**JAZMnNtZEWv|fAYwjMV~`|<FU!3EGU1a~?xw61SdWr+P^{pu;@d*~#G<hAl_7%tA~n4MgrDMrM+l#UGZ+Lm*US|SxME{o+@brvs5Z+jyQ6CgTRb|Wz2>R8v1pVR}!=-MaCVwxFbapHEwx9HCaTik$4G1w&}%(`*rZoGYCouCuonir1epsJZV%atSNBY=v@8?&>Ediq+Pbg-ckF&aGc02%PYtxvm<M}{5b0(p;egQ$<(5op@QkJtdoVw+l!3mBDod-D3}w@^Y#70QxHJwWBJhxC@tr}0O41+hjMtm3?Rd+Bh_OjQwQ1D*v=4yuQ#ZlbZvXjy2PDRFCIylSgW6tuEQm#n*4q}pa;V%>%mpJq-8?KiZEec@5QVz@wJi!2OY6clw?H1A-bLD?R45=YN@fc!K|lCA<9yT3{v6^h2mJ0<Lk1OL~xOf2$Xz4T!=vq5XAF!kxk|F-cDR@FYlLC}&6_sGPR^Q3H3q1ay~WAw|MZfCkoyOze|#yV(dIuLyDT(_;y#AU8imbu3Yr0Dw?ybujpP=2lE`P~%rX)318H5nuA(`N?+ZGs3DDii+M(D~Yzs!Oko$JqKGdJnQg!oFa9El?jwjb1(BZFwl)$K1V)OP_3{$JR!KW))XqP0agL)YN*UA+#Gy)tP{MSrEG&sDNimoix&?`7u>u^PoZ}8G|+Uvi=-Fwqq*=J5`#IJbldBZ8%Ukq1PoA8OJBBaCN<LDhycwbd``6oifB2$5QES$C~=8H@>-aNt)eWj}_$w+7z3-<4rGW8aFF)KN6leF!u%N9@o51e!E3VD|fuaZTi>=R9{9@4+I@6kj)Bj86~VB@_L&oPyJk$1)79HEpQk&P>;OUGL_}pv+!@X>D~{xHT9X|y3B-xEIzAJXe+^y*C+T;kYrUNkgd_urU;o^OWXnrY_ntPN-`y4uT8R7w2pZStJu?k0=;F1vLuTwAA+nss6^TsvP=P>-m@v~Thw!~!|2KoAvK|-8b$Q(t4n9A%`A6X_V8Bis7&`j<oqDCJ`qIHZ6xL`)L5z>H=iVGFIrEy4#0*xQb&@Y0+a@kCPwC<r~!f>5wsGUy4tGnyGym7SBKif5A~?<-?5Co7pAcoNy=t@g0;{6;fGKEf>6<6OBWWtu77H$ObW%KNEXDbkFN#b{k#{y+UqGOfB5zE*Pm|_4ktNmIh~(#!&jiEPN~s^rE&-2QWF&i?Az*?S|Dh`(&iyei*xlc=N34Pf3;Yozi+Pl<X}mVB&^*uwN3E>2MDjxbPy&Gum1EDV{DMplSe7CZ}nHX*lo%tuFv{fN;a|plOBb;!s{?}T#98hU%;I(s+_o_ig2T?fQ2Dl1BrKNCx$|Eg=hhbNC7ivsENlaPM{hdT5qoxp94^@lP^?fgb(^5Wg{WDK$>eC0)$zpA&Zb%c<&zCG}ScF1<!OG+I3J(r~w05bXeJ=B2<BxZXh=%Gu>%RFjwvfA3SVh7qwm1^aAmff=2U!cHhO;#7PO<XXFe9DbmHU!1h39q5v+LL>*8RbfM1W71`-tK9%v^(VC?1k2zcm6O<QqzVbr{$`$~w-d?Yr6SS)+0H9O?{i`oL)!8;GKqiUX+&3R@$WqP8gYZi?_q_~6KWdDv`?d*qI!GTtZ3pbuWyPjO%;Mb|a-fSSx2Mw^;Fd_+EU@cb*^!rN(b_o2KI=k9ftwP|)z!AzRXNY+J80c&gSBXaFaWtXR%;}0imu&_r&s(|u#aGSV`uMP?bX#Qz_D@jJG$Rs=MoR2`SgS&1FRCD58cWacQGM=T9yFs2pX?;@gmZq?w%UIvr2zx%49d@K=c@IP*F1IGoh(LO_7Myw4-js7t%9rHsJMpC9<<gE2m$6;nElOS^p>MLpVI6WV$?qkRhtcN-*n_)1jlTo$nYjGr;O)#3)i}`%Ks&^OvnMYmV@dhN#E3$2Fhx7k2diln%fC0W)?6+_iO3=JhYlyaJHs(@SFWgPz{Xvv-N^(4{A2CiY?M)rYcqCqEMcjv^XR8&OH#vv(P~C)TO7$Q)qm%cDGzM3(zWASp>bVjbaG06c$asu<gGIZ)w2HY24YZE{ZC{0O|WGHN~^zgjI_D!NoQLk|u!T^|T*?*_bo!hqz*EW_O{6K5-nI@TE#y>s#ON-$F6bpU6i4JIgR+uOD3^>kjAf&3(zE)lh+upnuGTYK;sUYbNO&S<5D&R4IihtouBzkz2KfODg<B0{^%A*q6yoDLS)Da(tCMQ@XQo1#IJXK9C}tH1zkT_)~NGXQMF<}O0uM=4TtG?l>Z%|=#MlN-UEcwNO#lJRcw{!>Q!T^t?Zy|wIM$*yAqF**5RtDr=25b#^FzN)w(b}>>Qk-qIRbHq+Su<0^*PqgqEpWk-9v#oWI`c$H&4>~F0qx#z-IY>)7I(9qIquwpdc82L~89MFMgH4C5Stu0ge%4Tla}IIPyu1X=xWH_y?Win&QYRca-0bX7s6qVJJbX<cvu-%OLGMkRxjU3Q;LX{n^^l0UE<%_i<~|U1MbqqsR@%myN8^0q_FXz%F(lKyV*_<Q3fvzY*e7`ZcrTB@|7vhzDepiwVh1ZyRIuNLKt)Zn)+#+ySo=wRLxRwPabCfu9XOoe^m<6NsildIdR%IHv9Eqp!f_!22G!EZAQi`ap#qGP1n2}0Qxda16$mk=jI7gBiiRb+rr`?2)l<g1Q5e<os+Dho0N~N6H$lATi<zYim+<PR6J=o5Edu!ncW0>_a1vA?GqE2W+lJ-_#rC&v4moH=j;mb^n*hV}wg}6w(XqD^KChF3r_|8$un)SI4kUE-M}e71UvuV-)$>;CL>H&!W5Df$aoDB7nKEpUoS$Y}v-!bMZ7#1?{Me8M+bJ19$qpXz9Uyr1&icpE*l?fo@12<bg-8n%L=ps>B^GWrkxM<AwCNTm%ni#YsD)>>q0cjB+Z?+pBha8sr-{&+#_!^0b(j}Vx;D-+bMHvt1kZ<PhD{KZ^e9~iAoB;0UgFUDp-Q#uo$moKYA?m@+{Ig|sZkjaCL)Grk?`C&|K~Vy8+EdVAYhDh>C&7){!EDofxH}y%h9qwtL`*kJTfqeV10CE_!18-Xd+T4X05lE=QMF`-heWbwl{+;7m+fIlF_Vvm@$x<WUy*$7cY<GYYfR6=V^riR)cG%2u;;M0KS4Xinge*6Jl&imLZQkJ~~Y8WPm)*$LU2I*5xD+51dCME9<p6yRXYGs)~ja`ic^0yQJ-yIYycE4WHHrq}9Rgvw*?yp1)-`yMViEr3U)8K)-&VA3vv2;rrhF%Zp;(+e?Ot3T#9x${{wabzcUpl)79JeZGVgy4F!GffAu4PZm~7h($oRTy*w*<#6yff&Xa4r7M%JUq<%CoQM$=(}S1~V86ti0$GaVeJ!wnN5P7WF)8Zn5+qRf7T*K-VlDeKD1(Fz!f0%`27z%o0;^seWT~}BomBxpe0^AmDdt>+9VV~xxo36DNt5xpD*dibl7MHWm|$ly?$HE4DhJ!KW<-M-QRlK_U6oOvgngRAYG%a$P^+q>SP!L|=)qGV%vNnW7qnGWs_{cwvq`38w;j3gywIH$9n|^a<P?iM=YHX+4LlAR72SQj0wA7hZX3>vqvTVlHqMFGx>Ax)5{QoJ_S0M|6j>_+h%~+P@)g*o{@JBeltlr8nUi3TbBA5sb+;)O&)a5+Q%2!&PE=!9f0#O^S3wXjp;`NmnJ%ZgagT)t5i0^OHu=&xRuGd8%ZOLYmJQwNj${9H76bw~Jy9YUUbHZ75DSKFEv*v?r%Hk^eh)$+Ozpe%jkKhZO6(G3D=iNt&jo?g#0Xj@$<7haaJr>a*G$2v&KczIB(P1P94dqSr7dH>li$yK=NrdcQBTY`D{F^&#sBNbY(pxf;oK%C2()N}RiI%d%fqYzqhuz6(>K2Ljy%V8oA~`)c_$cpx9uZ^x`bEvnTQSNK-$`n0+3%I@Ttrd)EX-cB`wIAY?^P~$zS!!XfV-(^#V*YFfWPm^&3)3SV0O4lrMdz&fkC?X|$Av_2J02st2~MF~|EG)9)Bx@n4fYZD^(!$G*J?m!TB#k(5vj*(J2~21hh1Q7a_$G?qXi)>H|yC^Bl2l^rs6y-m(EhqUKW57Ay$bB$h<RJnxW9e4_MTVBG{N^OyKd@)t?7<}Vm^L`8&$Ayml#JGj88bYr(w%HpN$W2^m;O|h;8QMA9pPynSKRe&4G(e*=DFh10ZRn>=6M3jrOlz`t3PVGp8qKKmMSx%2*4B{~S>&E2#<x#;_WuC==nxa2>xw#dgyf8EK~3&dhyxfxcI9#f4^&3!R2YH+=E**Qj^MKGY8);Yl@~+MJNJeZU|_293?FrDf`!<zf}tAX;@d9Z3J4YoiE;uu#<-TARi_y%1S1h`$w8$w=@R3SMltDz<Et=;QR@W=dAu!Tw~^N{h%`rmV#JIx7$(_EBY^VGQzDk|`n&8l_+W2l;X}+;ff7dqVP`vjO3P?|XeiXu-A?5&X`jJ$W{HZP#8u!?%Fv9@7OYMUqUfzC8EO)wf%=@*QonKU%<tEFKM^6Rk7>1sowr%EAfq+LXam@m;G-*60q+n(&}SV^N}A~t)ntL8es$s`P*3<2j2a#ekPKyw?TlRB<cm1<wNJbAaOB(?hR8<;mt5P6jc^mW%oS}tUYU#kuhw##5wnzmF*U@(pOY1U0hF>EiBIT!D>`)LEIl=UuYw`11=3q+ub&{nm2Ui?K!p5hZ?Fl#Zs58{C_7zjzVam6ZcEr;Wn@Otu*;^SUY?%JiJ;{@^l_IJ*}6+$%W#0!?rr-?1P3^4jK*d_b<&*)2d$g7dG6r`_U^}1kdwo4tPD%{6%AZ}P_?^Nodj~CCEhqRa2X=e#;mKG2Y6%$ty37o<qyVeYYj+FHq!;XdASbI$9)CBR{f69q^j;@E-ByF=<Uu%#1=ys4p%#FxfJVZdeRm?)OZ98JjP!5f^pm-!v+)B{~#S`mQa9?cY#bA{lGcsHmS;cHl7n0nW<JBp+#`5;%#Ax!dT}rDG1w^Fd2amD5ad3SOpK;eR}{%Z$gLtH_qoE>d_M+*ofE!UM6=mDqhqyG*b6e<lMJHMfR;!4jt9MIRzF=fp8t>$f?<-x|=ElzR&Q6!@jqzF7U%DC1tPF@hg4jfnhO0PmFM4x1Iki*8;uM!sWK?-s;@iL2&61O;*%}C}hA>s;k8y;^I9`aPxrAB*kaws+>G+LT50uj-@6aCvio9`y6G6sFla&CR9P517*m>YIkMl2&j-0@R3<3@cfS35vXl}T^2-eBzJ{<RlI5t#3>4l+JFzi<TA8T;>(Xi&{C4sbSiMlN5^dxzh+6ZCiH?Sb=1}n#NuG}mP3Euow(Zgpmg$M6SR!zCTrC3HAT>hckeUO2Q0675}D=^4k!<m#Fb625f!2MY*{&rhs-v?^K~IK1|fkJVs%Hd7IThx8>B2)SDnHBngpb&+V-U9m>yZcP^(sZZEbR3GA&HUToLpGwg0*_Qa$VH^fjVBnY%2raN`gAQ_JW9!F^PbCGEGn^3nAn!^s3Lv8y!hgE~NZXc4o}X`LcTWQoH()d(~bg#i%npyP+(cr9Zt4I;3IiuBWJ&OTIDS=kHbG6V3-2J)Cb1fSwU?i2{M6hMyw^f!plfOw<}Iet79+mj<}Yy)J032lsRT;v3K4vhVs%+`ng!Wa~SCxCJJVYCee#>1M?I1(jqOfs~s2CsUGB9&#W1u*4K6KBA@0YTOTxkBhXtP46W@9+8R+}{jL0wfZdKi0AydTNVgA+&-b&a6&#LcnD6`ea^e)eaD-hj75n;R;XpfGY^lS4dl-ViatlI)-dbDT<1#7`;r0O&oh-SKr_yIP$x8iO1p`l{j~WollN#bPC-k5r*}2o)0lid^i_6>Lx#Ah*9UJ5;H_7Ams^*6X7&}oWU<_mD~M*=9(G3f!_A$Lfa|#0=cmwPd@J)rm3rFZEFN*l`-0~Fk}Li$Wfq-?vFK~(9&d4O@}7%t0w<<kh>`w#<WsZ4*Gv93@EuCfk&AUwv={IMQA82#(O`Xo-)q~Ba39!9A?{bU{-Fxc0z{lGYc~3PE=hJC)t^0#MzC5n<Z_BCOw8Jou;HXc!mt@Db{=<{Q7i=a4X{6sR7uRgiv<g4m$Rm=|em#g|Yw?*ja=ppC7e}^OVg^A$_8!b5)-1cHZ6Go>gfMUZ?aW4WzLDa!VTI&H44;7w~Z@AP8vZaK(uTq66~IEJo+SWWE~v8x%3Zs49&8;4od&40DU6PuHjE-pt>uR)D4FNNi_Vvyx7g(ji8sq<E)s>)G>?dO9QOL!)KB`MWqSvZ`h*W8+SeZ5lx2L|gw_WqKv7$5dvi5&>y6XN$H~KTZ!uFP27E876g|9AcFc14S}5Fm=fzC92_ry72wOhe~Zgh6xsH;UX}*nioAAYO!VRW?CS7u^4|0XgSf`7*6lnKzm=MWwkR8kSNK76o}XN<kb<UwTIH{tnG4I4Ro$*QDhY8Jw(|sNcn-j5!kw4<ej@ZaA2_%Bq1c0uw?8}c@Ol>!a3gc&ve13qBAa+;B9E>3_2qi;dvBJ32(sOXOTERv`c&0j_&tZ5t8dYN8;fW!?^)}!Be1d??qPNI#)Zsul~p!V>sB%L)7eU)*F%dx?r>J>J(9C^^vi?2KfwsAW`-u4Q}sNb+)xGD3WD7h=QXFI@;B`*IF0Ezb@=$cx+}=Gmu)~7YcnxtS@a1UGXx3f>8rV7K0Nb;s;%*#Hm}L{0k<<6v7Q5B5duoT9F8FozsjfM{UM!)HuR>bY#t?%_H;n?}y%eUF%rP)LZgvEC^3&%ITRNVN%;6=nSgTB+Be(*Pb~h%yV{%tgj)kRmdVHs?Y<CKoy6dvxI^Z=lV|I6()^KYLrkW*T1;P!kN@~aJ1?}v|3WON7e_;P5Va*V&%ySAAJehhhBC{064Y=(04Y4&i&v~aaoaJr>9V--w~TvJx;YzG=E_IBHE_Z{HPhnk~)kxr{G`7JSHs=<e|4@x-O{7D)FFteXr*b5nD985BY*6(u)?eKqTu)G)7_?v&gH3^A6sYL0{ogY?hP07p9EHnT39aAW7PWq+}HKyhVt+2T@PK%xF6u<V{zCME1(iiCb@Y+XBh)SEX$jj=Eoe12_NxC~8w+t6CRF5y_)rnBfvu3GkV~yE08i!w(2KVAF&vFm<}Gj@oVrD4o1X!>e^wI2A=jLe@$PI5V96kj`wT4M4@LcNuLLuljEe|F;KmLo=8Y3CqjQybocD>F)KDI+3o;he+XREXuKg(=?=343MoL!sG|gk80$orkpfj^qY8y9UjzQ2z|7SaYeEJwac$f!52V-%(Qa>EP+pk#J~cuw!@crf<I6S8t1-*b51dj9MHvbh%AFnLrl{!<+zf<;c;W*H(y;QG8Rh$p*$Ls3R6f@1Nc?L`fNM(3><FEg^_H97numCxDQ1kUpN!AaB@uKAeI~PDZZ+D3CS+lMMP8i(3x0d814aD2|Mgf+9x?)k>$c1(aP`D6Mx|4IwQ!fjFq;bQ7*yCM~Aovb@Tqs7LlgS=4d;8^OTuV%!xt}ybAMhRPQ_gqjP<}vC;Ah6n-Bqz8(W$r1>H^>xG)eO7`pq_H{~bS_@4041Rt^S0G@GLNi+;*C+Mt*OQ(MyNs0^a80$BvfihdPwMOob{`;-nb@x*T(+P@XAW+>O0ST!eM8~Y6xmW2;4VMWiIoSStt2)8yj{TAz-GhvLS*~IL(@J2WK|iESE8w=C=??c7N|<8D`cT9TP=vGeQrxqGPjeIP_aE>PegI+b>UJMLQR^G-}6R2T!BNw>mVzCK{=?;*JX^pie^JVBZ3nTs1$>C18^(Pg3WxQmtB=`$us@bbZ$qtD{JD5m#>wNg~F@aYvU{66;clAY-_%CEFy!g5EXjWUWQ{GYzX$n=S3+OzlW|H#d7@{-^L)Xgld+92CWEUVNbt^xU$6v`5||X6%I*vAM{8Oq(t2+B&jL-0G4G$<rd;jh#nXebEAW&44)pOX+v{c%roTOh(|91q8q%r-{$uz&%+Ao@S(x^gB94IeAHtFcvb_4W}?ce&2r&R0e@#ZVig+l@}X+nk{*bY{P^P0P=3zmYEikGT@&`6;-A>^=y6D$jnc{&s61qgu1v7bn`46T$jx@ZSHV06D-S|t4}dw&y>Eo8e(r<+9ShK{d#Q$y%NT0^Bjf-uE^AA+;!7!CkP2qGk0OiHay+M!My4fcT6OO0P=)`@59zVe!Dx+ZzW|4)Lad)o6;&A4ZEPMAuq0+%a*u`5TUe2ces#CaFyDVOOucb1;{%bmu!dSnVaL^U7ul)4Ebcy$pdRs!q9VOIrTeG-2wN@%BqEPd-H#&VX|9kt7E=5&E3~pa!6h-F^uXr#>-;(|3~un!HhYqgcqp4ZUmPzNM!c$Rz-HlqkP+u>k8@Nkrng8w+#3>=M;(acx|WUs>=>?T71q?JEYCvF#S4fO5`!!oNQYUTPE>B<Wa1*#2r>D*K|$)#s<w=8ii0(%i=#$UV}$8`DvWnM6<F0Igj9+oJ07u-sAb#Y=Noi`x&#}C6yU;3;TN?Ttq#L7$$h!@sN+VLo@cSFEZ2uMAk<~26g%D)xFt`6Z{403`!*dKJ<uS!L2YEcG3-n?Xg2F6ZH3Et9Rq~~z(0$(JYyduvZo=Epw+L0bPTds9i%r?Hp~y1mmjsZHSHKpg3~N?`E_LPV(wd*wO=riD0Tu;ewM>fP;htmj_3d9tpk4v)D<YBFcvi2w7-RH+fXs~rtJrNGR8M|F2N)mnPCfVYM8It!ilvMJ6VCGuuz+yC{l%R?Ye*<?&7UbnJ_Vx;h72GBZwR!f0QRr=*s5N!cWmf^apT$gbgO0W@}yL$`dBGSbL|CSM(G92?R4OqQu9;a<U+PQ}Lkp%?Dfyoz3N!1%hi1?W)<iPW{QH>Jz!+L03W)qv`Fa8wcwIUwnA^V8|%@1#eV$v$LufHr>?D1-QtfU3EXc6kT72V?-R4o-})kRq(myO~L%EdqLL1^MR)X9HoPx52NS^u9^j=6cGesCW0$v@~P<udoUZ6ap;^<2(ZGoQmMQ&@Tg2Rwv*!x;3NA+UcnrLZzNR)Ydv0>p^bg$K{#+iu^YQfW>xTn7d1na8fOxZNv>DJPUQ){{N#HHP9m{MX#4C?9OtluOK?MQUKUuj?mALA3o}T{LX}Aq)~7~>42PTz&X}uGE=q$#4i$czgbk++=pw?1!8&^qS%g#A$Ya+PnuapEU|$2i=48t*H}Y%^lu&Q^vhg811o7)D%`}|ue~8opCO$u^R8pQI`5ySYO0fexT5zdAOb04#h=f2_BQ+B_b+T?bX^f-CYNDg*R0;#wmZ&DIgn%kjjJru6m&>K`*{YDh;3$knEr0tyAyVkef%Zh&M3-B+Uu$PA@D^c}YddzP?vW>L6HG~bRFWrdY}p=AHr-ZWV=x(K>i|Xas5vH0140h$scB$kOK5$w4z6c?iV}&W4fxWj9kpXnmfdPnV*eO;Wx4{kEE?&}`Cu$@KB5PyfqZ4=c~aLh5$?~02Q|O=GKeR-+HJH368XVHj7*TK1fSF5ESLy;PIG7$oOC|3CfTjl(6bHiR)*^1`yYPi(q=}v@+tufPxAdX+n^2Gzby$D#kT;PtCUd=cgX56AGXw@8y=K0#3^({gqGmswu?bDT<Eo>EA>#+D}NkP5h4c-%grF6VyCmpa%LLB)tKMk@&T5n1Ot<gUeNiZ2QI1Q)$$*T+)&EWL+W6jR2{XD&4s%$FkMvi$URmFb@UZ+VPX-eDXRo{JH*YkBG#=zH+86ukH7I@H;dYh`#mizE=NWv--(|ke~)j&=GcxYfqWF@jAXVJ32D$S)UwSt6TrdLpao;09d>5TyW~?~4jqK(<jot)Q6=CY9Y9e57bLDPR*$>Y)l*%a;ej?pLrp&mk)q@v77GF(JZOgi+@eD9Kc<fZ@2bCSu<+(L);TO5OR{tor%<S{4pHoghhuY^k*hn`ri1<R^UBsuvVL_NA(hzh^0RpBi|ox7=Kjo7Yj|9lje#io1X#l0+Is^Mj6^WJBUxA?GeejPKuCqd7^n=vM1u9b0#dJA2C!5YxHplWy~8-*Q167HbAKGOciSz~NdI<gaWWi}c<ETXyqvo>&s?$f-V1Usp*WD9T{94<a4<3XlE|}H4WOH?l*oC&FYrFzh|ytrP-_p2O0@f;D<{QZ@QY=Dcxa()ol_J1(mv8!26LYgn}TL29yw4C^{<-TV^`4xVz8f6oc99H>EBQPz42i^egy{iiP)TT+2ONcF`hJvxAOG|G(F(~vDI~pJK=L<NJvFFP+LfC`q<vGS}vYQTna<30u@1iBqdOYA+l5e>Uqiya?i!6<KGaIh0~ls9&K{?(*t~fo@%^TqbpBA@d8X9DVoqbjpSxyG~#N>a`_A>ym62_IR;J(V@eob7UWc}e(HVFJ__TLaLA$oF-)Tk!aX}#7u#huMNp7m-8Qrs9j%qTZJ(Uo!#Kl|4{z^)8&f*2@4B0m#-1ApHH8<Us5T86(XhZHs(xxT9<oV+ZRGD6?+NKK8~Iy6^@LT{oD9=jgXJg?gM3*~HhPOC0`nc*@+?*xu!qd+<NWI7xf7hnf)-S^n(5|Xg*>^;HXS5iaVfVNsu+_rN}nuwDwDG*wxfgOD5+MjR))nox+bT<`>3j7hM=r`<h2v)%Jc}!l*j-H+l$36hG~nB`(a1S^c4cG=8fTq(RL8nVZIT(TX!@f(TaG{B;tIA=SYc0J0cetxP(D^!lkC(^MvG>4pJ$QRILi_*J#CCNsx7-1=w!{?+9>(U@Vitac!Z|UPn`HQ0w9wF384%noMpfxQTI5xED0m?Dd8^qRt*ml%^~BqXe!{br29}w(D@_bRY4iCLWkTc!}#F^2%aIJtkz~b}@qv$AaFVpdE<t;zTFNJr`HlG`9f0jP>d8Z8SjO>6+1EVnCy3Mb2U~v8+2z-;Z6+T)(&JiIACMga^oD5V4yYKd6=7d^G>W_|F=jRA886T6-z-RmSj<QpnxVUS=?hH96%r0Ejqe3|KT1J_{^Qi{9l1i{<W>4oa$FO%t}D5&3Drv9?8oZ}D)iCwQj-qp06tN5(g-me}3Ptkc~C3aQ0_26O;#Bun(0h}VEcg;iM`T-Ny@1!tsYS0(@6!rph`sZnUr&o(`SeyH~fvXfn~p)K~MTq)y*c$Q`k8sOke5=uqD?NI<gmfb%f0<M9QX8iE2fL9PDV+yYVnkI&V#xS*qHRJ1vrfeH!tRW?Ov(OaLC|w?lQc|yLHS{4y*-8{=>c+p(Q8|k9Z^(F++Z#9!7n%Z&pfLk@0B97Dui-Q;w*?+p`AJm^VVfaX16(RK?O@P;w2gZ1>oL+~U#-xOx8}8&($I%pg_Yz2MF|*X@Q#S){z>)d9{yd7_#LouED(WX+5i{*5&ck&uKTdyeJNndU3v*S>S?lQ#LK9qyitd^3(Dud3*yvPMK-qppcqA__^dcq#@u}9?sn_bkBgtFQouTDK$*a1L$kt+8?o#&zKN?!V#?+l%$vuPL^gr)x(;jplI8#1?g%jxpcy6Z*NGFZki>RTMvvuL)UphF{iHjw8K`CZxzDKyEu=(^fR~M_4iZ>yFwVR!UkF;N6=6$b>$0Tz#G!JFq=$u&b!m4~x(ZfCFYSZ5TLkf}0veYp-h5RnFI#pjIcwU+Z6*x_ny@fU#OECJgB$HSY~q>JuFi~EU|UfP8t#0~O{;+$&~C^;`KbXbEjRVq5Ye5Xj^^7p>KZ3p*T*>qL8BP)$*N8HsWJLip0y3_C$f#GeTfN15yeM@W^2Vj3>%u8hofFj{X*y{k@W)ZEDjYcAOz!hyTy8VL48t^jptZH1~fXfdKQHg=5gPMUEQmvoP+G7wC?v|;20XvCXAQ~onE$R%js!QxYn<OI~DM-OGVdK07(hlcX|Jd6j7w7?URW4Ez+7%cgjAFeRF&;1j*eQP<)}mxi9UBbsBag!*zGWjG$)pz_sg@Qt~KcM5<tsu-zvP=SH?qE^-Svq^uUQ<xp-*v5bwb6Xt+`y%pqOnlo(1dBV7U!i()8Lll%!{K)hXu>mRHiOsSQxFOtDs}^QTf$Bk!CS!y&>7`_Bu_hkJqsOfgql9C`!=VX-(i(asR8^M5NuwUP>M{kmlNTc5YH6$^!s=&*nj@`0<t!@*SxM(EQ%w|#eY8!59NbPFqkAG`wRWa5Lm}86%d<}-OPzDuKau){EPICspa;u&9ky{!*n62BtCgFf6i*Hv;S&4akfC6bhe)r3q?zF((6Fc6n}7YGJ-3H)6KPN!%nDh;GEH_IQzj`7n-_|}5l#(6l-KmzfZfG?QO4#hQJvdx*^ww@E2Xtv`kS}XuTV(kURc2$cez(AciZT*bP7%T8?Zz<u`6JJvR+T|0gbTWpoV{_)UkTf6lM5ti|tl6ewLHlVFXj5$bx2+-OV2jeZXEWAA;=NREZ}>_qITe?q+<!#I*SoNCR@o5V6XUMG)N0x!ZD>f+neqt&7fBK8IEb?8>!ZgDzIRISWfnQFyS2sVcXu;yDt*WgByLNgG+`o1U1U^~#Vllrg8$6t6I8-EAE*F$S0zkyQq?6;J`{%lp5T7xIaE%F2o=$Z%td7IeY1T{e7#+LZiKoI6vEe5twRiZq9g#6nrLe?Mv#dc+YR2RaZ>g-f6ZwWyf+rf#JbdlaS+M#uuhtpEfJglNhsAZHi|=Ea<M+Q515&Bk*4y2x0@8!HLzF`@=528~G)mQf$e46Y)_co|+Jf0EuF5u_EFSuQmOK`<yRw+mPMY(edqZqlSwHnO@wETbhNPf?e;mz>aDbcHJa94fjWvsJoXCu|4B+N4jojVWGgdP6>@(0_DrNS2c=>z0nG-CuU2fen$^L=po`Pyy*B4KlTFGzW@PWSa6=7K8)KE7E!mqp%ITQ734=PnmJpkXQk6Wj}lDh!7LC5!cAj8=P@}@)yR%uK)xYrgIbRimiOSEdgvBO(*Py=O?87#z$?$)&-|8pEig}sMfHlZUxPu0{S~q$AX}n^h$1(K(`YwOV6!QA8LodGI(zIzzxt3+*qzc=ES(+`72JlD~<k6RA5rhS~dF=j`&UY?{0_!M3OUy4ZL#H?;YK9%dtf@9(VW6AsdXkn<a_Jk-AWo)F=bCpTD$qc@|16Ud2l-y_;49HE0a+Q<XMg(`5*49*~uW6$KTBB!!hq$8>u9S#6t#06AR=ARUCFf{be`VaZORd%;Vx6^sR(cx09k#%w~uQ)u&*I0zmsT!Zrw4PROufCj<^cOjJoX0I|3OnEYl>24-HVNFgS{uOQ#H5p}<7F5-jEdLr#j-5nVqO5$k70(f{{TTvq{sPw<*}$GvY6*nsMU;zulC|(Ip^g}GEEK{vkmj=p721B1$&LUwN|PqeUOD4pHj{bFSn~F!@qoQmc4F`r5SGDgWPt#Xo_*7eZMiAHWw;AdjHoP=#JHRv+7z-$foLD|#vEa`(;eF~G}Fj13KF7UP}Bx1VqjY2Ri@^C?5??0wdr(ae=VV}TF@p{=dM@oE#@KarQZRElG+Pnf^0VZoh^_vx@e^GkHA9!R!lqa9F7u?`R#j<!F0x-s4N+CjuK;1s!IVARrK$R!%3khkChL+bUSUMO{emCgIXzzoqj`wf(*7P;{i{64+S^;hdgH#f|_!>(!p$bya^nvqLTO6I_~Ow9(f(S1KnGnDfWFjkQE6=DIkcPbQHPt7l%8m-JgX`%O^<zz#O)J06Ai~ULY<>T)p&`+@gl#IqX)MaQ@0co69<1AxeRrQEEa5BPs;+;90*fnZla`<H^Nm_e!odH(9>aj@o(*)2cYtb-C=-V}rR|fT!j{B^0<4p1k4B>e#WhpE*QfY)AP~wi9~olROJ$m<uK^TMsG~MWQYQ7V;qxM{#B~wO5CJHsk5qB;nx}(hPmci^6cu(8>V@E2GV;Hlis-LW^y0NZVo~H_9YzK|4UIKyFi)$1$cN8f+XrsIpy~Xz|n(r2qzwFe=bO8;vG87?!oCv0E>wQ1q;=YX>3*bj~x!YeaAvXtz4VPdNrsYIiTKs6_ET0~WhX?svK3pG=O?DH4{PvMNXP)mNMgr=Y@XQX&8Pl1pE-@yNJbE*m0FL@;V_jemGwf{>>*Sl>*H3VL_bpcA6><y&Lyit)G=dyN|`0EZk4-3f>%wD+jeYHecg^$u|@Y~d>aW<mi&!L1z-d=k}xFA#(&aNiKxGOBnNg<ESc4XRHafh*&KNgO4yD!C@Gk8CNzSkUb?BB9!e-Q*69$X&cRg<fM4FcD7|Jjc?#7B6Io@w?DcZ$siQQ1Zsth@9#XIL<>co{*-1uGFnMzY3YY7rf6$6^AbMl{N~L!gOMfyZ7OzGz!AWp66~;!%1BuB13^!2W1>#D?UZ}l!vlx%XFlHR>mX<EMknpc{Czk#+OO0{Q4~+^YTA7B`{#12jD?|;cl`6L97<Y`U{{Gv?}U{<Xd|`_Jf~|{=E|bl}Q+Ze^c=is2voI3>MLJ4U%c23{e?tzP{@yS;Tq`f>*bJRJ`1FUmfe|pbD~UmYi^aT={MqJ`E@(l!Hu?&hi5-(<bo38e`Fj16OK!Q=D5t>r6y%X)5;cOm5RvY0(W{Ti2V<(^Vl8eIUmt5tq41jvN30I3B|0=Ai+grEt*>CA3^&za_f+6wnS222JUaoe|_%4vvFkr{iFNL(q5+=)KP*v3vkwQBxk=k<(7!4uR%TIM5k%g3*z2`ZB*;rwUQDC@emhi9y?wA@$k3qz~c3M{nm-Qz1Suy-II+Zb6#hcgq}2P-}8~Ck4MMhPtI%aEA&3oLL-C0c38N)wkgSCCm2i!)EnCD<2?1Us7qd5-T2$*Ud%>52qQF+JRIB*Q(5GeSb4XXBjp+_!Ls%plJW1m4ADgHBRBW(K?5=^)QvNhH^$u_~#x8BKB^d6Al_Cefno#(O>Zrl$HQ(El#*-Z0V4)U_tp{qmJ|XghDiDdSi}QR}KnJVqe)13C|8X7cqHz)Cokt%i>)wttnrwX?Z!EDV>IwgPfVBQq(p+JVkrdm1<>pSTP}8VMr1a>IYZBN<s+xWb^+I5VvHDlIJhDZQT)Gm*yPwo7&|{tWeO3Eg|j{K1u36O4sBlsh}%ukFf>iz*sE_T}m}9QYIA{VbZ|Yku&W<Czj9}@~!=P<rt$nK$fz!S%1rU+_IXpJTOg?t5Gi6s|}Z_B&B6-Pj`XJr&6ycXWNT&ubFuri4v<hOr=N`;vD1dOiJVjp4B0mO76PH1C?WdQVr-Mrf!qN49fW8Oa3T;2TokD-lHW=)C}0Smts?SYFimlgHV+?9n%Q$od&(soawE)G2fpXYV2{U+gKJtixl*h!?apBT<&<12x(!QE~F0k$itB$Gq*TvA}@X<Vi?{m5Xr0H=f>G)M)}+i@$YtLcqa-%qrUWsXyri?rBFF_j9*hT=q0coi(N<oolQELR5?Wr-Q)D>(75iYpg^q!>-I}9eT}#-ic-oMGHn>WQYoIc7-d!qus-3qI^~Pf4w_BH7fov_CG^sEj_)$e7kp@%>N>@@5w;NJsMM2mN6}eGHFYzP4ivHp2A<zI6fuF4MnDVS#js_wTnYV<Om1C_l6;z}i)_HgxW5s1KucHw&h0SnM%5=OM#O`@DHd*{alDZrOkz`nv;qLySkgG76<N*c`}D*kO_*(9Ik`T$Pw@(US;0SAL_&*PRK-(o2uKaR+6&I+n6&tGn9=|x7*tOpZoPaDFS^V8FBLLIkyA|x;cqyMK>6%!Aaz3671FthUeO~!rYX_`LSj-Q!r<p4T!l^HQ(zkep*cNM#xuS)ZKLtS18W=Ukeiu9YPP}PnBoC0o9zVf)f2-dY{e(D0`=r^Qj@BP)C<x>=wpVAR?(ASR)!CF#ZCFO@6?I~ec@497<<{X_drSZLjmwKAU*PQ2V)}%Lzng*)!K0|Zxo!v3mg5=Ic%wv>11uaD)64{U#!gJO0928VeVY+CAdzxHsV{<1uS(ybX2CPLuN%ld+T^?B%4!LFnTn;Bu^PfpLOo%`l^IZKo<~FiFWEbCS)Kh@`eC0r{X<b$c@Ex1ZcEKPls0o6ROW`uvEtSr65GWx4IvTZM+hBUZjfS*R1F=^~7b)T^Je^k*@86jG`?^M)P1jJkfVfMQ>{<$GN9!x<4oyX>zKm7HPxEIHCu5CV~Jm2_ctDp(ONpBwDz=24mEtYF&-a0y5@!dZ<{FHZ4ohBI;zC0yZuv*7iL%!E!1Rv;dWgfF;^2NL1qPAQI=HucV!@5)P7+(*`vP2+d-FAW9F#0{4`%Ww4nyE^v=Ugqz{2Sia~hV}&0WpoB7D+$wi`N1;bJ-MfZOlntFY3KS?9$&=R7#hw@#gEkU}yE6rO*Jvj>I5%dIXjl?(o15g{f5i+Su^bgJB1V@(j-fiu)tm%^-R6;)+#2KASt3{d%l{%x2Pxb0Hr`l6<XM=DH75EuT6|#Au!$^7LM`G4<83!Ot-x4+MVTvT*VLhP$A`6U4I~OI2S7s<wITTAQ!lG|NZJhzY0*PavB>Hf1sQ#m59FY5Ac`V`<|6B+F%!Z81{Fy$Jur~M7v9l&^$AK6q)NP}YIoEF4nmzGF)Yg=4~#t7wok(04S6Olk9m;iYEnJlW2RlZD+~sXDfy_#e&Bx6pi$ImbYCO3X#FLl)M9K?GzcLgf<y-gwTnyLyP2y@)?^hqI2+Gc>tdzUPy~tZst!>Yf&vD<#mSJw+LShtN(G}3ztEv$#>*G5P5L$N+fI86ew$SMAUf^Jjh}FZI3%k<^N_lJs(Oti0&H*3X(8?mqo3AsiBxPeN+?uuAVPW2TGd@B3Zf>;C^fF8PVyzOj1^*-^`{C_LAOOeV@j%1r?nkON35b=;!dqUE1dUE?<LvW&UR;Ao8{q<VyqR<HyDH0@E6R4MMvo(#*_Yx)vd&_{T@v<>T1~glZ~8heeV)=8Ku{Cr#d%?7+ybsm23HcXnq8Gs*&-jL*_v|*ljy)4susSGD#2x+o^Ohl8;@2O>C#%(l_YPP`d_31a{xB9$p#jjOKE?M+Ap0@C#Do^!`s=GQ>@gRiT`>JWAnv(%wHikG~7(*xOteHXhDj0Pl^X^y+q<6m5BG7}hL5nq&&1687-LSXd-n=EYDx+_-OH$9jNHxRBvWGPo%5^(KUv*gfE9XY3G%VxG1=i2?8DDkhCe4lqWOXmGOaQDoUT77w?36GX7k5PTnu(=0!**wrA<wVDDIa)(S_(S$Nw@M)MfIi2AIKge53L|lcUHTR-7@B5}zu`y}KB18BP_Uimur_zx&siv2BjcyI_T#uIt$M>eNgop&>g;zzh?Ob)z78PbbFzUx({B{Fs=@bGo>V~6KkX;`u!zb<tQ{c*rBC<Mprc!DvbG1sB1lH0NvKncWpBX#EQ;dzx&QV!GOfLk7th7d+V7pXT8y^@_&Yj}+m?W1Pgr>=kj_;pVq8d$QbP-ntR@h<{w9(vb5O+Fwr;kh~DXN16IT&}>OPARx9nwy&L_gR22Jl4dhPo5&@LnDHY7kK4>-3Z2Sw|AlB%+PD(wHd{$gLgW@EEdnZ0l`D`otL{9cJF>@P~4hBP8C70b#SV*Xv+=M=&p-Ob9_9t~{o~s&Il{SNaRsY#8E)N?}sRW*CCoss)dGJZZyGC&1YS6(5@lIXER=jPcszGO3EGGO$YbPKE{zDo-ca)gRavrpoa{4DtZUHwua|o+jMqW%=e&emhj29i*-8gRO^==2Dl-Y=Q>`UT;u+D{~JL`ikQ$c-LHK<jGcQgY>C}NLrF2+k&-T(-OH${jrLf=FY6_Jvas4A&9|O;T+~x`?8j0=^74-ANc}d;*^==Bx%QnTKqjf47{u9B<$earz49epZ)U5UOkphDz9rwNf!mey2GI3i>`tP>59V`JSeBurOuns0a)q0d@<;mO8AL0LokG+Hq-c)2+YA=wXK|M7GUC$@|c9!O&jc%ND%+qxO-|gT<m2*2&*qREwW$zdI}DAfAfxcIpdw0cPY&ou+y=xdQ*ibE1xZ?PiW<1@R;ZZCdQ&iF<!gXDc#PT1jhd^KqfC}2K#g-cJyFW=5@fmVBb`T3M#8~uE8?+pRELwF6*nbskCn9hP8n~+VMN3aIBPxXL?&cEox{p5)?1y6uzJpDdS<_c)DB-|MLF<JM^RU')))
_PLAN_IMPL=make_agent({0:_SCHEDULE},**{'hand_align': True, 'weed_repair': True, 'sell_lead': False, 'budget_guard': False, 'room_guard': False, 'clamp_sells': False, 'dead_stock': False, 'terminal_liquidation': True, 'front_run': False})
def standalone_plan_agent(observation,configuration=None):
    return _PLAN_IMPL(observation,configuration)
standalone_plan_agent.telemetry=_PLAN_IMPL.chassis.diagnostics
agent=standalone_plan_agent
kaggle_submission_agent=standalone_plan_agent
