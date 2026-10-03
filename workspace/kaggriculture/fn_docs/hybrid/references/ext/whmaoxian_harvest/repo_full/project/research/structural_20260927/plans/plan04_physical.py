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
_SCHEDULE=json.loads(zlib.decompress(base64.b85decode('c-rk<!ERhflKdB*d5}no*6fXzdTe22)1agwW(~nGu(McTF?;atZL$Bp9FhI{^~=bJ$gFBf#>~ldlj>KmDyu3pGBWb#|2_NnUw`}CUw=FMm!Hpmx_S5R?Bn^_fBgDi|MuSxA3Xf{w_ktz&%gf9!_PmTef!}rzuf%z=7*cNXXj_HZtu^|pMN}m{P?H4+t(jny?^-p{`=j{!+&4wf3y69ci-=JKdt^r;TIqO@BC<#Z(jZB!%wR*B;$Rzd;9h<qEFxd{hPbpnfM`j&BxzwhVt!)H*a76@-S`hKYaSv%ScwET)!Xx@bEC}@A%tpC++Rcs~wuNpU-~0y?g)tr&mWm-S6JLUw<U$7}`U=h);iTc{HTuq1&gQ$2m_%<_+W3&34`5*YBrpy%vYzkl)4uz1!_xKm6?vySKMLo}FL#)AckDYx@GveR>--e~&-t5pACP$G`vj=(+J3amL^r{`h`*&e1qFPu$&X-}K$>hhUXkbH?*=fAfBKN8UP{?frA$CfU47VY3)dj`Mw3!N-?bKP3)j|H<R`*VlVL*T;sIzVGI7$D?dcel+#NchcvXroJ3F^0}*Z9iDq}JjZp9-ya@5bJpWQ=*{}p_G_2Y#@|>zfiu1`yH9^rUSamQd~W3@<++aII2>_dCC`B!PI%(-!pZ5nU2tnpRi3*{z24Ik9(#CNG_Y(W<dSk8kUnzy_r~q8-Q2ft-|k+$|K*RnyZ3M2zWLWrFP?bKnP;5%ldG@v-AXc4b_&z)Sq_`ch!PJg91eVrR)!1z5SglUY?5zU9R}(<U*FySl$|6`zgs?HX18(1FOsiZe80yZ<n-qb?uB&$A`63|gX`Zqp5C&p4(5gyYQXj`^yLdyWHtSdrc{1e;#?lyHGa3;p-<nt8sMYtmA+&d%JOaKmLHqv_|#>@2P2PD&vwqnOGC5bpVRw0iQkv<Tk^T}zl6Nl)(>mGS>qn_ug8CW$;ljqCagB!ix~DS7|N8~&A#JNbT0sg09^EWPDb|e@d@t1e!-VwZpqUK$NW0uWH+Cvee(F#%iJtKSSW;l83Fi?2l&kQ+G5$p$s7Uc!_cO@DcEq{tLni+(55kHiUBTP^Zm`;pF0ER-@bei3eJ~DrvBf%_jfn<-|p`2{^G6o`X!b-13?mdr(pGf<|x4X1JD?ZWi#1Dmm{La`$sGWUhsqu^9IkI<+~S8Ff6R$fUW0RJZCxR)(a|Pg%pL2vj@)6=;P`ai&xb0EvaXTzjzo6ipXC6EB#^sJBOPnL!iEHT<G}9|7OVTi~hksu$y=I=rj6x%hQ>k_qn~g=Pj=e`4Xm&WIQnXdfa5P3tHcQ;06Ns9y|sI+&=_>5%&){B>H6JZrbrpb#yR3-V9B+7{pKOi!oxDtx<1bR^zIwdPc}IjLt=zD-M@6oyF*;MRaLvF1?w6?p1W*z?>YGLK={Av(oJ2d33?1IplCq;!Wjc58RW(7s3!=Sw{KYaH&F0b@MvWgl$wZT`dsufgJBdw6ZpQCmmX!eeks)x%m~lhcn<ouu*e58ymZUEzxI5|KLkImuxaVmzz17+~k-Z0SRV0o`9fXCx^Xp0A~Pzj|?#Gz$BYAFL|vTsG5gQMi+qaWe*?azOxrbI;l7m-d7&Nd4?3$*+S0-`Sqekb3_?vunXYdmH8P>M=6^AGB1Y#68g=+OhrHV;0KT?Sq~^da!)W%(Q96|HU;0N;l0p7r1w>X77hB8a1YlTD3TU74p-ArT<k8+Fo0}5CgXF1rkjo4eQt3oGj_xIEaC%kTpJ68c+L3(Qf!?$%aOxlL$sE0f2kZj18Wag;^xS^It}knk?>CDT4x0npBJ@_^$+2am;~d-)3KeJ=aoL-*@x|oh<=KTH^3{*evwC0lY9wshHfv9`usZwQ;t2?yw~{6Xcz0R2CEiOoD_@g9nz71c=}i_J{&AWhpAw4SOwR<uqey7#I%h3Ua}~Jv16TeR)NVOJ@1nX$QQ4sJd$Q64LKzUHNQBeu*@6sNvVxB2EvK5>0uvw7)S#q^_@2k%%|?#Wd^A2B<xmm!jBSiCU7b)0gm<l{f>SJZC)F0?g2q4I0ow%Di3b&w%^`9{O5Wf^TXjXWDo?=%ezqEbPH`dqg&v+?{073?IKjMEe(fgK>^)Rp88_S>+ygyInD?={5IEF8K@})@CX056ca4}3@rcbl`W@d9zn8Kw;@F?bAxCVn-h~U;Pm^&L4Y`7J;H6`8QT&<QSmgOp&M40Rd>huGg=SuKp`O|-7L;T=dvM&ZyO7*3&s+OeW{J2pC&Izv>}+pWoH#PL*##jyS}kC*!cxc9q>B>)FUR#oDG`_87!lb_5qCz0EX2PN&6nvJA@ktd;$JX;wiC>cKr9O7i6+?lPCLOB4*so;xQUc3ye^j78v-^!ZFh_<PVOXMui@rw25aSaW{9RQ0UnR4#Et1NESm`L4DgbjbNjrvsgo%NpIb2C&coU&C?Hmkzb^_6>N}&&e|W%lBhlfLt%*8_Cy~XEFthw6_HjM0zA?47bq~rj0%Ngy8tC&r$}N2ziJRCfsW@j`Hch$VDiiVaFjX*fge((Um&eTj?qjFju+L~o{<*vTmQ<*9L9fCNBE;(0B{GDUKq26a)cghP94f%F$3!*#<&VeOicn_1+SsB8S(|6G_psQJrnZ^TP2mwEX6ELd=4jPfrHzs_V$!rUg-Q|+zas)bOs!~nqM5Pi?Kz4e444V<<TnTCiPRHaM1U}UWh)~x%e|#dc(@2VxktDvYsTP7Q0kQQ~Ov)=aJzqg}sB$Iz_$)VMu|r;!|VtR}?aDnxZLOa8EQeFC#Z&7x`2w)=4YtZJrrG-Xbc)LCi*O)8fyuahOF@7NH0@H5c79u{j;)$nwN8oe5Aw$m`w*2Q%_R-F*T%=&v9%uEV&?G&3&J<t92watS}YdHbiQpcD>XoyjylqO!I$dFVU$*B_@wA~>twB~KPOPau}m?g5KXz=eYbR?j<I_#~z=M4y&PZpVK<GT(&a5Zy6Ks89v^C<+sqV-`-Vw&>vv7-J*)a)77dxw5nv&9s;cJI!w&HmY2#lBWfiW4>V;IUE*Y_y!bn4kEio6@UiUDef0EV?<gk6}_=i851POQw4|!+9$$WjL6uQMtAK$<{ThePiEN&+4S(whf9cL^2ZGD*lLumr~g{^cBTO$F~EjE`+2h+1ZUvHH9*B@mQjk6s{c;W@s<t*dg=8Z%l8u&xHygJnfNui4C=>nx^87cMqxuCNYBb}bK`AT+*k__^d4-oA(k?D2?9-SUsiz94aquy%X7l*jaK(i3mQfPf(^7GEG53Cb+F<y(((n_hF*YXSrW2QP!JN4#8@TUkR_GJ$RECN34@hpzig+4-MlyM9+!2n6NL~_NC3AUi=qcQ6ld?-!F5R4#A1MH$F}XgjFwH&;<rgm!fd~)w-|)54`AA(?qhzYKUK$pHqd)R_tim_AF@J5#Xzwl{0=i!CJ&)Y`|ZqxTAi%nZdF4pkz7*|BaOsMlNPbrl&uo#^}9wWL~)9!1Hc6@y|byrJV-ecm*idI$%b(WGTA2RlNmH~d2JmhbnKvZiqVe`e>TAZj>1O@rv=VeTxpF$cepIjTB1>*qTq}bWMy3HoL}%5G;boMA;ELg=zH&ghH(RS9+>WERpj=bjuC=DA=G{W(8exe;yr3z;`sUSx<nQn*pf6GRz?A?%waS6Fq0H|VTBAH&@j26lxn$=(g=h+@#Yro@H@_b-WUNNIRs50Xosh<<(d(r8i7isxFK@h{1`s2r<(&U*&c`@5hO`5k$}nS2?0+g@~rayFD380pk<+o$XQ}pj6)w3&rXiSph6;aR&+`q93fw?QE5g@{zK(LAS7;w)RUc}IeqzZKwcZoEMwEq_EJQ#mxbexbcoAR_CUEg;CeW^l1SqK1?Oc|f7)u|`5&7Kz+5mKI#>aw^6GG>86qcUMWz|BM*xaH>vc}psvfI^uO+Od*NsDZthW(Q08u9?g*shi>v<irJWLI(o?-H&z@xEnrg^or(Oa?`7BaB}hCPvj{e7|eqXzQEGz$$?3`D6Kl3Xf^lmI5V|0g%)=Jd~Y<MWHIFF`4)Fg{BuanzM88|@bQLtzbwyVMN@k^<O)(ApJ>wkQlaLJFKJ#1B8_`4DXcsIPrLn!C0OeL%n=SCFBS2&T!peon~9$5JUKA((2uI>#`@LMGJn#KCzSG%9BVJjmVPu>efVZlZwFH0qjQ?{1+aJ;K_<OWoaiITz{xeKNbJHzV#6NHTKtq>G#TEmkO>%YaC@`RQUsvPIBI>~TzKT^xX^mzA5jPkfKs=LS@X!8()ZBJ->3U~T7U9JE{ndjUF~Txc3ZcT~JDs?q_v3qTq3x;#1NMcU8w)ILOL41bNbv0JHsIrOqlseYkK9hwE@Wwn~<klr42)Zmb;m*5wBEtUK!1(X5w!Y8(QA`ESqk|jqVghtbZ%Bymkuv(p{sftGhFSAj&uI~c6O9VavLw(loyuPYfZ9w*Ky6@nZZ!jtVrR4%+vN$4s@jv6nF)kNlp#xyKwmBm#td0l}Izdc=ihiW4C#^-HP1m*h3qu+t70gjkT}IoHGcf}y_4fy(YU+rSx~Wa&yq&X$)|Nt4U^suFrB=r(kns-CqF!+v^0bAx=q!u~95o7Z2sau|ZLtVv0Eno{(=dt=ax9z!D^5XLH!|TGCpZD~u6R6WloY|}UXPZCk<k{Ai@mle&$=cc5IDpZyh1F=o#1Xyu$jtfpJZF(V`ep?<3Bh`L%;csC1#vTsqQLK0zu2dt<{0RS+R=$>6Knu1x+;cbVrlZ=Viw0Y0SItz5^o$S~;ZiQzS*jU!h$SekTWdRY~$|H0kO~FsM!eCxOd=<m6np+YsVyHFzmBe<9+R#1AZ7dR=j$5}k|Gr4av?T>gGphsLO+25%3UVs*7mDg+^ORmjmGA~$t`45Xfh*0m8wv_d#W#|bp(zNV?rQcwga{>mIkR;e_RK8~>5#+6=Exk3%NuT4%wK`u)gwk=H)f1vp!yiXG&8d7tmdb-T9$<k>XykN9jEZk#-OullN!I@&5(QZ0YAkhqPgfD(Pxpm^-#6E9~=0#E8q}7&A&o<j{APMCx&;lo^jjiCdo`O2A2TU8sZ06KBz-eSGlpqUD)B4qJRF<2?{J=o*Qi~Pty-rHd0hlW#Ad#MZ>oud8AmTvG1d9Ql4Vd$m=8&nqiQ{AdR**t-xbEV_u8opbTqT=2UdUihW21p+63sE=nf3D?N_7CZyxGyOzG}lJr@9;t21Ip(Asr4Jl^JsCmGSI1-(?c_UmC|F0fLwuHrx(TQk>28%Edpnrp*V}Q*onjDxHUb>vQq-@{%Z!#5x$S&8Yfn(YuX@DB@=nL@V1}MlRc(BuJbCatV2%Se;|_`N5t7ky&@xP)oFZYL%b_E(Cbi(!Ed#6So#nszzqq5}8|;4!d6lF)6M{6^ku>DUQS4OYF!t98g*z4O<G(IJgF*FbwQ#u%J|VT$MYb5CZ%gQjv5~Q5lIpXaaa8R+VS$keciybWCAP%`Kk%vu2%0F`J{1e&GaXV`n-nDef~X6VJ+xIOvHex@@qeB2LVqBb3<VXZy-{PU!`cC!lT?4`ETWQZ^bGawjJ<*nU%(-<ZATQnGxai783cJHYbP6ZKX&Ku%oY6jwTm!mkbSWsBY-{Jsh_J%)h*DyBda8Fq*K_oUcoCOO?xI_H<%>U9$4sI#3;Acd_VUk05y`e+4ZiGoOrqj^m`|Iu)%!%8w5oYBsDxcU_B^C+hPzl8Kd+gr-B74npJ#v0-*U3`HGxSrON3osFVB{&^x7c-+PUFg@0cR|#E;yu)qXZ?k^MOb|#I-Z1Rq{z`NonybPRGnHR2|UxNMFgRVcjuU|tnKHftmNz?dGhJU*DcI)xs6^*_RVCweIACDza<UCGqNwZTh(rguaW8lI7S~Kq$as5AsBdWe4aAog(s!SCVVXfm+JY-elEaG!~K<sVi)7@lq6DF&@hWg0m1iFhfA?|-0oL^uQau-P--DoxuGS#Kq6X~sl)27IyOyjr@FM3OI-mV3ZWJAf<RC7q#mUMhoDJsE|k>}L)`G<Pq`R5>XVQO!~RCu16d1Q;ayNBxL{N8eieQJ(iG%}>&z<Kg5DWZePjU`rc@*+5rZ}|6OOh3E44Cmsv)+_ZJEQuzK@wA3`Sh5-AXVwbh>cIDfTZYql?{Dk(Wc6X<kh!C_yuQ(M=`fhLZ$eVSfzjH09SITGY^s=IX?49?+AQa-O3#<}0}^)0UmZ1kd=(mKB<4$^pOnMW>IN(1ud!9WWz#oL{+A&2DK5Yk<dWB%gAmumG(wi+%R7TXMm2yDTx3R~%r+bw-N?2n}{5YK1?+`BV&5!3M{4Igq^{Sfs5NF7~*tvw<0?1pr#!md4ZhM>ND*t&}e;2$0%3t&s_qnI+A2qLE$C*b$&K041^SD@-Cq7G>xX3$BNc-Zs;pDbYtuE7ac9s2zmFXo>B!(<M{Pg_IoPhXuNME30j93(uA)R|UB835{@qMv#<fHWj6s)!;ti$p)9~OqUkgAv^^^Oq<)YD&xL^?jtOS<=VEC{>SeTROd<i*HFJO$IpbXrKnIgY8i?Wz_dmO(4!m)^h#q1(Lv9+fR>yW<6Ls_9gy9(BI9HkI1mLp`Vzk{Ny&PZsl<W3Frsrx6N&+-2?mp&C~gz&1u2aNry&-uk@83Y@8#O0Hf`uwb!U`2WWz6~k~`upqHu2zlQ@(%3?!DE)j4urRUv6kWQpwd#^9nb898;3AbNegy%}vfKpW(Bv}dH)qg(QWm8T2I66!{@LN#`1*!*wKN3KMiTotUiF1$;&Pm4+vXebfYw=N3_xX&TyLNzvn1E$VA)5MNf7*!#RMcHI(JAKj^Vq}Xsf?HSw`Q;@rA$=lNXRFuygm2}%>a*2FxCNcU^M`!)178&EN87ss<E*A0Gd$H``%dD@mNpIPlFU5m0y!b|&n|p%WD-9lv2zl<5$Z=gkKrxHJJRF`=M3ngq6$7BRm)wg^g^7#f>R}Oo)kE3>@?K5o9=`pHU?~B&<onuZU*<nm3x11!lYT}g)T<1#~t9ON$neN`$3Llny>I=1h!X}v6$XT=9OM%#BQfp!|M!X!%k{%tEQxWBLs#<RWK;%y&sn>W6V$c0P&I)5E@&8JtXxa$`n=Zl#bY>O4snlfrcY?{W}AwW~wM%8r-23lMx-g6&6m0T)phzRYXNwb_uf6^_>Q4c}qLkXWD2-N<2s_9=1!zz5?|nyXBa3B~8@VRyGB&3P)7CZdGX&h29_#7Derp7WSSeu{*B_9jM4OHMpdBHO+@PBnqEQ#9JD8&ENAvg;6md5`@qnVAxbsTp6kxVx=|Y2bw}BvUU=T;`*5PLnlG0m!siAlGoVoc@dm)u9D1IQ%Rc>>LK%(l*28KQcPOrI2az3QI~aLVZM5ZCLkrhXDtt5quC7Of}z!G{f1HJ`w>NPS=JM&%F`<5Y*9WPsG`rfvJVVrB~$sL*^aAJ^v@;WwItMxo?@^uwLPIc_nj!Ad$!eVTBk(6=%GOQbHrwnT#V71P88-kCHYh!iIQ%xr8Av;$=CC0@#v7NC4y^Md4B}GED<ahj+0fDj?HP`DR9%wjj^4sdnI+*yC1Q5o_*E|JI74j+Krm+p4XJOtzyzwyOm5Nl)W#Yy*Od*k(Vn{X8UpP3vDC`#s5&8OFj-pQJK=q#$gIJMX!owH0~nnSpkx~7U;$GsaF%0!fKbVU#X3B+5sa(q+ZB^Y?fdE(t+(D7nSA!yhXFhlK`+6p5h~jE>dX6!}sFKZU{@s8RuQuS7tBRBi;K86t1h-2N5t<RTxg(?}W)Bi_?$oiH2$+%i<{~2~=wGo7IKsU`esV>`_Xfl^B8Ojj=W#r4pn<3U(=WxNJiY(vg$;^OE_R8Qm;fVnql2ED}-tccQ=LoEwDwQgF!=?t`lX&R`D|;63V&E|sfVoq??NW7v#Wc|?ZX<CL-hUzGZhB3X;aE=G>!U<5)$nT8NH<}yhvjHNYBw1}wMb&*O*fsY`YmvF;kKrSfaiCmxZED~3nm$^ncYqy2h=7PC`fI~sW31~NIM3t6WZYuSR!lw=UsuW%SE~raId;@+6m@v!Vt*7&<N?*#i$cgAnKJ&fi7_>yYp-E06F9}IM=p%ncoFz{dctB2lMBCeAHTfM^8j{|1?h*h3g;Fgrn=$rZ576<;AK7JBE%zvh>exAHDb-Mt5R!(gv^QBlO$r4NId3aN$n^j(jC2(+4&3jhNdODGbgtf#&z}RMj)9s$2D&H<E;OV)S1l!dtyk1yjO44yie5|crX>u+t^0W!l%d2Op9Mn|uU!F<6~=Tvt!%8Mkwj4n4%6IEWx|QDny7ZG;u#32S>oT*@TAAHrYFSYihU7U%BROy+#brbbcLgUSO@bgIO;c6f2ApF(1%NMV0!Up2;Ea~1!NG_U8u1QR@Cb3)&kH%+6s8h_bQ2nu=_TAnoQjwZPuCpA0>M^(n{ZKk(4Xls14vhQECbN5tFdmew9~7RH|OPP!Q1Z?f4b7WxGtdM?<jBWmSFks$aDh{XS5bU1Zx7LpO>X4S*)RMVqI!bczBsreM+$SPEG%zfhxBF~Zsl)e`?>dbbm(M1K83w_;O@Bq#z!F9u}<FM1D)(Xi~Kk3m^Vg=jz8IOcHWAJOh4Xo;<AmKDW&MfxLJ7r-*QCT&yBHJ~vod~|BVd|7apWl>>yPA*Mim1C?o1#Lm>RW!^i6d~~d<@W$condQplFK%!D(TQJ4lGoPOI9sYbDCvegpI`+S5^xSax_*Y1!0Iz+cxa%4q4l;sg2DB&F>9(3Z)xjL9=3_I+ot7tc%F{Dxydj%(BvdR$Dhx;YZmnzObHf++?>^cxPiQL=>Uv-V8DD*R6sBh@yo3_ErFZOhFA26;oPE-ZXULGjtlF0`nm@RxM6CV9S9m^uq8BC})nT2v-6bLgjkGvLv|m6=Ou;fWc6M$6>iJYNH&U(7hv*HLP-E_f@{nJCin94_(FzVRjy)ZiPfNZVO73j(m+)rnBDlMVVk<mJg5xg}DxS2^6p!x6`AjGrtW<Rc-#z4V|c{f;^3i>Uc5T%3RlC7Z6WqVKN>N`LY>bWqWRUZ3X@Q^}S|SM68#orR2&e7G|S}7&F63LGWX-L9x^dT?CVf3h}TiY9Ue2ixAO?b@?)|ETgFa%~Wk`yRZ5U$H0p?Awo^eGj^-7)sbulUTjNCS)$p2%C~YNkkaZXW@4|zY0pi?m#SCP7fVoTw8pYsE|*xIQ!!g_XM6fWxHwAPS!BqqU|_)vU^m`OI$I;<f_F|p-EJ#Hi^V;D2dk<iykx5}y-`HYJE;{14rd--uLU@fm4Gs?8@;q0dXQ>nQ3P`-zc=NZCj*mGO)#h|%sL@A#d^E!z)<CI=*^aYWOS7KC$lLqn_?H2W<A@A*i@}svj|MGaIG$3(}O=aOG#)p`%%W}b+zjxraGB}mf7h@=-!Ced?Iaf#Y`!5bUd30dLL@OU4D>5t*<qnjT?nAngoVGHLa`a!>pejZ)uH!Jj-@y!DGE*%~p(8=0hF&dZB37b4L^yfh8l05VgKK8i=XtT2$!NPE{0BO5Zn)FXFNWT99@X`>Tk~4REkXHI^^;Py1sS6}Y9g>MS!XPj(w8bgHb#IY5J7k+~?MC{^M2={ze!La>DENhn8}B%ivP57=38VT>Xx-4L%*CBzg~I_;tIQyBD}u9BVNU<r7_AUmo7#me>U&g-pY9Rw+OB9R-BDI2ac4||j>HZN-*q(~qlH;4s0c;+b&XKBRDn^{Dsg_ptaal<@9shg260TphbVKhL1luc|sM2>L&BhZ)zp`jcII;Hs0(`h-6&O}OA6oF+_=$Q~5tJ#5On>Js_^1h<$YvUC%4lRqvPFREjU{RMf5`ufwlBA5<#rQ5z@ioh4IxSBNTVZOFmTVB80^TSSf|u~D_Y9P6n5oUhix?%Urzh=HX^|>B^iZqYo28ps6YREnym=^37UzYNq6%4(D8WbEnN<%pApQ&j*FvjTrZfFqz=>##JblYj%ssbVLWdoOV67XW!+KL-neNv<r5B}8hoOP1FKgHwFsp~6Y!RXH&I(9}2OX}gBwYh3ymli}b<R%Z7m+)U4U0tXo~R%b&!<6E5xn7j)h%tbR@sPOc4UYxRmvh_To+vyQMflWR&V(iScLt#N_vy}<9V{()PTUWvjVmxs>r(Q2(9jdMwf9;F_|U_2oe>hr}17%IE{yU5@>k&yR5JSP`4w)RH&+R8^+D6sGFz9<h6$_g&4NZaG_DU@Z*PuTd$l;T=3C)MWdw{q;;6G*C<+n$)4eQOsBr?d~$YiStfr$1jKf4X^Qr?M$(I(o>hg0WqgGOxPFjFNgFYVc&A0@D>JcriXW=o_#p3sAdPJ{!)aSXb(6WWph+uMqzzzMHOlN>@R(FrIb4|LNQpdChcntID{uHCgzf21wQfvP%22`4!B1G-fz1+hCv+5B#Msp7a-^bC9x4K^=klEl<zNWWD!L7C(PZUgrd7>Z!ZJ+NnH~G0&NG;v+3|cNTnAPNSQ+=bcV>UT2wfFvM+Lmck))=!l^qNWAV~*G=GFq~cR~#hqYUX1Od%gIye0~8(^d=2&Mn!k=Px5!#JlH{j=TF|gKluL`Yc-aB%47I3#p@{xtHwUF_ov^b$J{_oLJ4=MS2?N{HFQLr~RDGBtJdu#aFxKX;)kC^waMi1D<P*+{}}4(%Il8Q-ap=o)$l1cNYbS%nK|Lh7|Z7e^5!@Vc4$|gCl`q(%+tH0rWJECbOQp>P-N=aVsZCu=qLHPfR$tprtZwU4_anx9GG6rx*6K-65OwFwcOIa+M&7Gh5ES-&ISTIJk^iAV5|-yb`;_X-gsU7fw^G;v$}|9?jugf_=cLH<Qa!=|ymF7eM)9XR|kn7ZF=~*%Lfr;2ZB8In%a$N{1&akD&KCjEVA=g$FnX3ZpkTgR#YlOJ310PHAk57%~y986q?uMaTn}u^S?9(z%-fR9a=ep5L_C>&)P(1Z7%G$q}qOcJ4d|IDyW}5I88vWF8wBSVU){7ie|b4bA9zwlA6G%tUBuJPf6?JhCgkv<MlUd#D~N=M9bJ61jf>C2as;qgt<YStqMfhN1Sm|N2W1pCsZ0Ka{a)&UiXeG2YcU9z}$m?sx7*O<YTfFxkAcSY20&TKA>5!>UfhJ@jl*r<#r>y7o4*gEPD)Qsqcxo_#DMOXQ!Zut+R-?)%BQ7}cD-Qr#umj`@UcuWU+zp!H&eiLJ&6qQ<hkH4eq+=p`nODy{TNDfA5uawp)RS;$fga3+5fQjjSd>4XbqhSZ*|8KUc_#H!NUU7}E4rK)0V5}iO--Pb{$+U*1Sz3VE}H4gr<?gOMkNw&utw0_+w3mwU(j7&KbQ^3w@#4S#5jkJmh+TcY#q@N}N`<<?bdAeE<)$<aI!fNA{K~TAFh&Ws8tR}{^aqDW6*Vy_oV^l_2?j-g##ee*25W5KuGRGw<rTA(N-<St`24-xt0=z0MB4G(BTV=}JDg;qkcb+$fs{&COszwM;0C55aSM2EcSTIX>LZbk05AHnsofqFBS7|!n6ac}~72ef=nUq)1>?~VXsbM2<lHy{ETRoC`434x1hoHcAtL!MVNf0_rg;BQnW=1WKp74z+a+^YT$|-kK+e-OIMo8pF?4LzNN}yf97vQm>TQM{vl42EfAk9RtNe@|I2YHKhp)}5oE;cIkU|nxop(#i@8Y;0R32%*PRHWuvh~^aYb+vY^{>4mPkJd_+!23ikxG4P{D_R5?YSr)1HnyFxi>-H|bBatq0se$Y!vu#%goBhOQP{l5+WeeKx}%?_d7g+$v8)d43RJO`vdW;tKdPoebcD6eGU=y2AU1F7<tu^`Es<lqF&a<`07DE#96?OXXa*|`90JB|NJ|W1e)$;s=mQhDxJhz-sC>j4j1a%x@NDe&Na2aA3Gl?e>gdbh6HdtB!V;%crOq7O&NAfZh7tU--Vm)yhbBM8XFr>AF3tK3R^_5wQBZTJa^J1u4sjxy-I!G4y<yHf$=?<Xb1=}cQwRmg7i+1RV<Uxs5^yAsSnD=tv-MR|wG#<u7Gr5q)WTz)+PUG_huLjtFh0R+$jC;mC9FYSzC?#`OpVHeQb4IRT<jfTpQbdZXga=3tSXOyO9EwH$&T)}P%|qs4q0g<RK>RJ!?A`?F@;alhBQmvNSf*n)m8~57*_f|wGrWPlpoaW%vwBMRa`}bWLm7libbk{^k6hV&kWM;m}z`Kt&-)3!!#H%<;!|(4DBHXv~k#=W+axGXi3}=qQPd|>@k<$d;ysfOTmZ&qjRF!!axOg(=6)J4tT*$>9oPfJcqH!0G){V#KfLlTk{jnR#)PI`U0Gg&o5)-joZ?Ej^D@AR)x{f+Vw&f!KVdRs%^FNByje4wT#%7fqE!D13<BLm!B5{AT`P_6vTPC(Y0M>JIkCm5-$0tJrRGuo}Qj}BPNG<n>!OKGK;Sda#@b6!PZh1Wl;rV!(}dxOj@_CoDfm$mb4>p9UFam;P11OyO?XiZZJ4Q=qBW>$-N&OR$Ovxu7F(JH;I*A>RzmDPQmYhPru!Yv*VAa2UUY6@IEmNInj{YArtu<Ys{I%fp6x~LLALWun_SFeW728A*Yx{v=K6D5IM`Wu`T5ID9$gBkN*!L$&oq')))
_PLAN_IMPL=make_agent({0:_SCHEDULE},**{'hand_align': True, 'weed_repair': True, 'sell_lead': False, 'budget_guard': False, 'room_guard': False, 'clamp_sells': False, 'dead_stock': False, 'terminal_liquidation': True, 'front_run': False})
def standalone_plan_agent(observation,configuration=None):
    return _PLAN_IMPL(observation,configuration)
standalone_plan_agent.telemetry=_PLAN_IMPL.chassis.diagnostics
agent=standalone_plan_agent
kaggle_submission_agent=standalone_plan_agent
