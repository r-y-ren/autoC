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
_SCHEDULE=json.loads(zlib.decompress(base64.b85decode('c-rM%OK)W7b^I^0=E6a=v3HcFZ4FG#3^+4sD1smuh=Txuvv9Ht^4~KO$?kjasZ*!U_ilPeG|BG1-{U;%RQ>e7Z~px+fB)NG|NiC=KfQVX;qmkLZ+^ae^B;ftuYddRudjUl@o#_m`+xrRf4=_w)0=O<{P@fL`*%OwKfJkn^WBH@o4bGd`R?iEPp8w{uP^>^did~u^Rn~T;N|b%J)Yj+A9nxo>HE{^<MDs+U;O-kcl6<Ydh_w!cYpr!@$jzv#p^ddzGT<x<Ku_7U%vbN^-s><pYA_z7GUMy95?5%jOWv*&-+#U_RG76x4(S6|MdCG^L|{G=J~z9`Srz@^}qaN7Yv-DPp5~6&6oTg|Nh=zAKy59rjHNz-<=L;;Q6o25AJh3e~o`We2dG=hi~!qGv9ySJw7_B*8}*+U*GQOz1<A}XY=^%_n%LX`-i{olzn8dckw*~Ul6RX{j2!H=$c)=^kt=9K6Y!4b|0EsDEp1SyMO-S^4W)vBp-0P_fFyU>puStdhoBO|HBt?xvqBxE!XuSo*y~$6kwUmT0DRJ?|=XM=xntz09ixW<b4DOWcI@`p6Czb+wpuLc6)Kz(zlNvKH6R0e@e|(6kF+|*{pk$coQyn>Ua>ZYg2lqu5V;6Zf+;Rt$Nv9@O7iD3=Pla+Zv}WtqD4J#*-YDojts9&s&RPFA#XG;4`k@@3N@ZpJG!B4jS{T;TN=<bot-wNjUCX>Vd)6yS(4i59IB>`|$8^`tI{De>^>Ye)sV1U-zeVZ%0V1|MbJ*y`L==dUSV5q2=0qxeD`DZ0)aKHVBZ>V&;w-+>T8kbX>RMo!y>3d#a-caW)*-kC)J4yM<2tz->#>VQA&~w4(#k5p-TIn`y7>Qv_GBshhKSzYoUmguO_tw^KN9US1)LvxfMx5x{M-o1XKa*Z16}GbRbpJ&L=H=+Qt<usaa@?=kWK2*%JJVVfF)sHSi7(e1B~SN-Yfp~b$e3_3}Q5nb$A!R90PbPVHe{TVN*95~>|-)WD?Z>5)9@mi9*>dACP+hlGV!xTn*6gOrrjJ%0WMW0(<hp`#bHOtXgi6kW;JISO^zyX4U4CTOesn7Kt(R;^x%Z?3NiQ_{hzBWy&lJTCCFBGKBlD)B^K$sH_kMr~p85jZd%hy)ktny;SayVy^uD92Tnd_?ULpsj}Yk6Lcqr+1kGXtBnAUjNr2Hmmg8-@PbNsqS83K(+G2$PmgXFYoPqS#U#DF$3S3@_{Q{r%&=*wb-&HIX(#K)|r0VIcxRankko=_|2(`dPKIAhth~1GBq*+gH0@w&`s{R`Eo3iC?g#V~=tt2D(O|k#kwMi?KR(Q)<u9bI$zf^W**b+tcIYkKnr=fdqW7fx|JoF4X<7@v>>4?T@l0icc@Nr%niT*%P!ArC1-Eq0!=(t+F3#hvea}Ps&#q)Nd}8xy+-_y>KjLKXfKGHHiJau&a{Vbn|9H(dv1Fai7j_*5i^%Tzs(QSP(UO{b3~~Pa+(O${fz-(K--Gi6yfIE-tMIX;t26@#5pBR4y{L4F5N<vctjyArqTW`d+Jy6IL78YR3KTQGqkT$cTk1FOh4On9%;8vD`Ou7FvQAmrB+$^?2sMSj*zJEeCgKT~5fn!X<FEK|id%pMGn_3mqwiQy{dUPU^nO9myfJ;+UV-c;d5E<Y^kE^i7J*42#2HzIH`Ht;6Q46)V=`ca^A0P#3|KLJN<(p`4oclidSBD@5ZSh_{vi#tl8L`;cKp#wPm!43)cHA%4~*{K6j5%r<;VloNvYvDFzJK*}%_VacqpjG=^=slftpyTEZk*X;Pq6h;PoRq{i@0h6{kQSM<i2GDo_b>gD2!FV7c3H)hN-Dx{<3u`*|a*3_>g_EoNDn#KlLp@qIv-%7`<9?tF=$iOo3j?=CH;&s6C7^79P6aJ|D3TlOx;Uv~+rzRAIVsVy<)$(@G=Bdrc4jop!~5I-nkj7}dNhx704i118I-3mD<)=7LYV+y8(2vOt;e|-jRjd@5_OVf68Z9RyejPn1rqL>My3`g&?v<L;q-BisT_7e^X#G(u~ZoLYbTPXBl86sNwYR9k<zfF38Z<)Wh$FiM{(Mr=un!i9;*Y@oGsvBpgFqq)B@s2DM}cbJEP^3BB+5@KPi}(-~%T$dzeUWa{+Dx5JNcgug|n=WK)IqI5&2ln0s#;A<d61sgDe^Qh^$5O3IncI|O^y0W&gT^V<aF5}^Pem{})HZ+D*)ZqB;;vVrDiar(F}vsmfcxBcd!wN|)!AgndaY~ThKq2Nbm{)8ULCWA0qXoj)2kG*mojpm<6VvOxe2$?<iNQA#>Y2unf6+n6wH7`a0R#wI$0th|De>WY$UT64=*lf2K-#XBod$%)bJM4$-%R9H$^kKyWR?yGDpC(z3%+50SaRaQ=^b61C?;2k3vCo;E=Al=0zDv?LeULS($0APOI0>Coc|hv`>a?zW1Jh37(^KT&RB%ICMaUm)pMFzPtW50&2Fr`?%24udAmNl^u^e{5THcpS$6x2LiT;uqxDOv5qJqG~{rk6X)=&WvNtnT$zOzOEsiz(uu!3AEB%6x3L^4T+nWDJ|-K&whm8V$~He2L|+H0UuAru>k|G`Lx;Bh8jB*t0XGG^+IgGl2i2w?{Z9bm%l*fkLd2qPHQ(o#W3Y-uHP3s5NrkCcF+77Nv}Up6spB5*;lAq{kic*|zzaQy5kG18VH@gzG8D1;aysnhUXTNrVCuq<1O`CI6`ic~Ag4x2E>1y23}+E>c@%G3YLadPo~X~2qMtN~E2cw7CLt<f1CuNqWwmIT@&dz20wP7{h(!?@N+H4hXd6mqSCB6U)4Pu1h{cHBrh`IpHYpOiKcS8W4>-kjeXaa0`Nq>zV+ci(`CtD4?p9>@Dd0k>CTZPcA2I930I<lvxGF^sB_aTePqH23_RQ21Po-qoe3($f_U$;`7NSUMn<*HabNnhN0{%lXTuv4C>XSmf-DNj~L~w1pXFw9T%Nm`ISA7dc~Dw^ztY!%C@ZOlNSnS0tmTL0*eQCLR25=r&lL+1WL!O@&S)VHTZ>QcISWQ`{;{F7o=)+joC*d+_Cj;jyRKlDvQ{+bWyI>{Ohy{f5EAz42(2O9heRpBfg+hI4zhIH<OEU_sl+w7uF2gFi;d#(Kje$ACBqqG+%uv>Gf~l7)uD5(r#WZR9&7(nn_S)ifjkmHQX3S0F{rVq6q@%j9B(;%>a&Eal+Ev|QGbZ|;MMEK*~{Spjq-l1fTJFJG-rmJYFv*kedbF9k&viu`Ir|0OY)(W4G+a3vRes-#kc!z!C`?OJ}(!CMg!flyhuBG7ZPwV<Voc`BmEDbbKxUFRmNjsC;Chd;CNbXtjzjtOhhUcUa*H|Rr!a~Bp|opSDGS)%${qN;XTkL`I?7<V-0Lb#;2#9G&R^f?qEJQRCy-Gj41u>e-xtK*FjV4m@oC9X^s{HUYmKurbS2}E#0iRhe^$wI_x<pK*9y2}kL{gnOxB`%MQeul6-i+2L$9on!fe8TY-Ft}*-_b}eHYaYX^?iNZxT5*xrH=sNf)}9pWtN~xQxi!_7%2I@Zp*0J+#E5P3UIgpi=4v$@{M8{@+SdwzJj~R=byirN5H8i7rDX%RLm=L*7&yBzHfq2a)@x$ac9`zbEwI=dX&YH(m@-zF1BV7UPR6GW7mAtcMD>!g&v8H*RTb1xwDgQz-`d(zKve<+bfgX+f6!PJfdPS$MM0E`CwxTj0(O=RccP@;;1}(}*%!<3NE%dSrh>+tA_|&rd!jQ$x1HYOGKBGVHJ|Of%4|t209`bfVeBp-txXg+>CS_yGN`WmlNU}V%Di=kvcNB*(povksg#I|NR-}+N-9%+PMolO(Y|hGI$JR3oJ=Bvd|b_gUyjTrhot?vms5qw>`3#n^~ApO&*4GXpsIjW38$pbZ7&0h)}`(%?GelkGh^DJGekn{i4~779~U))nQD6-o8r}8i|b1ROoPbPXT0BKW~uu}rXtj3EumHGUY_Lg4xOcVD0t$i0O7N-cM!N~wy>bc(5SE$UKg4)18@Mva$M}D%~?|u+D%(ubtSN<@Y9D%3yq9!Gdwz*Wk=JYO+=}?K-^P&=p~DH+rEd6yl4&w)OHR(WbId-cgSr)cspvkF5sSkA{8oMP#7pvV>$fLmC$M-IEOHEXjfEo8?2hCQ9)GCf48<-?Nz`c#%_sx5y%5zPK=$xlB<<X@ijeE;VL_m#YY<~7quxU5HhIa-M8&Q+qwWxz0|XHKU@fk!eLFy^1MCQ%-#AV4NW|6Hr8*EPZZhnsP9A0wJTNUS&Vv8mvSC2+O^3tB&g&Yey_Ax8{229h}t!%45iB#N~ABm=fFY-9?v<Nq-p9l(dY*lM;7=b8eqEZ+kLor^mvn#HY`gTi<I+5oe=?}p%Te^W=??~N0-U^juW#NU1}7<?XrLO*~67IuT?7vcA`D;`Y%LQQ%12`joX^vju6b&W9UrRw9!zvI#|Rw?sTH%Jo{XSg6%DgO|Y9{fH_1>mrL&j`mN0poA%lD<a`~Co(H@pTW@bS4Ad8I?J^aVh=+(TLi9+QU5||eGXP-A+f-JhEk!H0EV=P=0c9+@E+D)?k)?y+x-e)SqA=3gp=B?Wj!NS^_O|_nRyZ8_qd4F)&Z1chKAh!?WH;g17=R~hbt5(^@xsdgyVoAKF;yQxE5irF*fbKqD1_!tnnk{K<8>Jue>!)^xp7oDj%evf^_fge8V|&FW_w9S&wQ78Zg$)`w^JD1!WvzoWJc8k*9eBYg}lIbM^I!Bun;b^SQ(^%_{OQkMETQ}Vk;Qo9-<rFu1(lo*jp+>uxZ@+g%M$3PN8pNG4v7hwD<!y0MQ7xgAh6~`X}Mu^d$8gKgJ&wX4E0GG_i1)rKlwAA%|B#Q7*qz-CQX;!}4a6L(sL<=+J0ys_SKGk7jN6`I)8}idOk=nV}M6vvGX8z32^^*(gvTu?V}+7^Q=<*zL%Z^vfyMU=-H@B!_?!A_znn&C_gA50re{N_$1z6&oRl=VIf*Qi!BTv2;J%gZ)9q;P3(-O{4i-KHCAGRJ8Ljj~D{=&HpkcEB_OR1BuE+xlpvB^IT*CwXo8~;1859fFoU1e(?qMaN6pvPsb+dvf&}PIWuXD=e=HDd@A3!Q0-V{M!yQ$6t#cB^%Hw8?Y2x(T4^_#Hv(eOWXz61FKxTULi`2&s<GpCErRUg$rm`7sAr4>=z=)Uq$a{#hgH)=s5-@<4_^Sovtx|%nZ8}Z^n~T-tqfr9<;E8<C#}wNySy@!SAbfpLYC&(fE205!D^3dUi7^KX+;MypVPGx2rz-mC^Ynb?XkFh_c$@UL5trIh{)_nm>&>S$PBn)pWct4DVe8A3nG#@hwC>3-On#Vd&7bWUif3?9#qJW2fS(Js0GnT4-=oCJ`>?#U>o*0j3eNzwUroJ|4jEILF_`&MU)z(chkLh(3gt|ZOM|ZTrl(O(AAP5q+_T)K-Fo55G7kjMp#vEL>V^Qso*u9a8{Hni!j^0hJf06frRcrMW4kNClwoQl}>dfprhaxG}ye-#)_{FtstEHjhD>38kG)O<PSuzVYDRlAL@`$MG?IlqN3$&2so&ed01U`NnTnSLGaBD`u8z$rDb-e*(SH=jM2m+b6`pXbbYEvqee@_M|CY2ao~T-DcX*jv6zIMPRw8O(|bywq3+~x$82?@Zf47nuM_WXIcA3@t=k?2HY&(fj%ccNsd%kHP~+0g>&g?*s0AGGB2!Hq@c7*S$n0&0J$Fk$_PTb>B+*KAF$mQRR@zHdiqk@{CF&S6Igj-nvcb|0jvMx>L4P|a!&5C-JQiw!I9w~ym#v;k98@7~0Tzh2s)87dAr&(0HSjVPg4~-)h&+4uuV47_!)M|3iW1)Q$qcYJ*CU_Qfa9Empz1_r5GT$VGzLc<Whw5DV%APgbQ{$g&U`qBaF83cf`0+lfpE)AXz}K5K=v-_;d`87A{SFc`ty>%?7pdOPzb!70rl-VAnZo?(a_Y{lpQX%o!h|`09q5*oBIjKOD9>L5g8JcmeZ;!0fn#4Vz%3*I2b?t>Pm`5Op^H!7>Y?AKaxO#5fKZwteP0yAR+<))X2Hsdxw~~S4*N%1?@~AGHi+vH)KWTC5eU(1r=&lexj=wLfu4MPB?3x7})?O&w<?lEEFm6&xKcZ;}MW8;CAVeZ1>JmTN6oJ>5QwEvdULZJdgRmFuxJGMrd-0$jBlw>tju(9e%2*x=e3vj)HJaAiP&<W>};KcF|FxEr#BYR2ggiw&hyUs8&OTfw<7Oli;+4Ff`<G=pVKvy34FahTAMb&cdNsmptm=ff}SXx6(C;o19U-47&6LX-XE(g+DJ)3@*b=cTA5=xO=tZNYY02^|9IrWf<@Q*NwEEYO2h-Oifz-R+C^MNdJyf-aUq2(?mVmpsPOX=JB!H+U{ssy=Gps3_gNm6sMAXC?*6LOLTmph~DL&UJJ;?v91w9nAulwA@)6rT@gW&*O|gn*s?Y*85h>hu8<b*!3Bdf7UeRMNCqNN`-w;uu!rciPoE#}&)=RNAAdB9R}sAyFuJfB-^u3%r39fAV5Pq}P8Mto)lyWrvkO=_fE(mvvE<Qk0o~z~)p~`GmL_P`&eG(F%t-w@r_;x!5t=;+T>%cwk=D*p;<Ts;O<zx9zEx@A1Tj(6TGRK!9j$99s<i^ePE{u-O5cv=1<AV-B(F5hKE=d@))}EG1mG+b<<$jf0_)u~gIG=!AR%)S&^QN{0@2L}@sF#UGPCyBd=x4Jg-v@^M*AG@*eN|O)@AjoZ$txgZP7&(W`_eCX1jYaOpR01YvusB3TQA0%}u}G)GZ(fkPvc%<wO!u3kczPu*fGM5@eYQ?#qoRHK_Eciop`P3}FXRqzSW)ddAfDTCtD`qS9!wPd-yJ_25#>)vTe=Q#+@Wd5xaf1V}Uxd^<NDN@xb_X^I4K&>p0*OM@GxOwp0{rO02F^;K*PE^3kC&>OA!CZODQw+J5UX6<cp_>KG;6-tgoQuv=O;MuwXJZ$7msV|~huHNLWkuY1YEUwz2FoxhDA|I%Q`AKl`Ok(6|QMsL|i<JxJIQc|0EXmnPF91jtUq;bjmW*P;Oi(A%oxn_R;FyEbR$+S`k@hWCtCYfJ6pSNs-no*yQ0gy%e#kIO^|d3W!=gT7I7mxn9>DoxYvlpP8=w?~c^}CxEg&^E6#$aE1n@B1q6`RPX`Loug}EI?gXSf=k{d_U=BV=$HrY$G45pA{H!S;rie}h31Pv71j{yl?)H*v(vD}F1>)R$fD}i#jWnf#l?rG3(AYyW>(AcivqJp9-aWDA#0G5nE<u)GQcZc&46W;+v+g&a-n95P8fAssrONFRGz(z0e4U(d}g>@OyV_<U247zV2HHqMfkf9HCjQUN357x`!mOX(`1dv-9UPN1L=b;7O5p(+5pa_#Nr%VN*9cRQ5!X-MF&UaUMfCa|4_ugbzHW2I>ZEg6#P%b{d{}SFd9)M8Q+2h(scCm-YCTyr?<nh9F1l#p4uvANRWK7n+v>W%Rl%I9`=AM9B$6Wz&>H-7ISRxqNlyq<@xR~NXj#bWOrxIGH>gA|yT3ZPK4uJqgg$(3KlyD&tp1lfs3+r;4K^>om(1Q3+X?ro^x^I|u7i*zHr8m}VWeIjzmZfk!f<0Mga%8-R(6K#Hul;g0^h^Y8Ne~*Smt%Vo1{0Eu7|epnJaDTzx&%55u$7>3<zrrYgjX$D@In+J^U4v1_=P%Z`<c%?s$7DIZJ3YXoCe5h79r>eIM0IudLC;_D1S7NnIpR7F03H(&E1wc?*XifrV_+dWjK_Iiz!a0@W4!}HpNE07u88UuIR<OJ^9|>>>8rN-LBa;1<V=&0>ivLM;|?1!EdTU?2FmQ<S}J<uCVh&CBS`zkPgPGMsx8O_Z!t4!qO|u9zr9Xy9x{_W+7&z84vmA3<jW0lrf}$Ih%C|)T!xUc!46-nM_KBleJ}&`O|SrjWK>v=BX3n0~0NZBvsN570G+`YsQF@tFT99QA31VLTfdrJ2Y)L)Z5gG3KHNZVlJArwvz$NGyQf05$3E0OW7CMHIXYks39vROk)#qu$u{=(r2&gDIMAxLeO7eWWhFA)2rJXXRq_|q-kx((F`{rvjq#Ak!V-E4Xlfn3$(8}Dw(X~)sdGtwV|*t?GZZzFJg_ITN!*En^@O4kjvc=5EJ42P+bwFsFJA~P`O^CD#)M$x~2>6bw?Y2tnk@8mQ)QN!+kY8w~Wc?DeDsb2Xrw!KUYkOvJlxD>qk%$2*KwQFJR{?8pcd*GW2eFzJS9g#7JD5#>ILiRK7>3U@V0rO9#F7gr_DOX;bgIahK+(M(<h4qrW=Om^D<eq?N$F;IUNF%C_NcY4o%(2c?f8bLvl=Wr#9mMR}ydrr5UNF%X9;k6ck!e&nDD;G3>2L0gQPaZiCJ^QTwjiI2d#ihZzuog`0Pvj{|C?JAHu7?#Chb?{H@@LF`i9!b!Mt$G08b8$&7E?T>+L2Qa(8<SQL2=&6TX$(Pa!8#$r#G0j$)1m=MN<eWUzL;ZJN>VRH$Ub;!x6nQn;zN=w&f5(70DyNt7?J|u-2$Dhbx=ADnHP28v&3iuYHXtD-E6JhC^jb2Ia?jf0Mtt_z>f3C?KqWET}C{RsoWn<4<FtSr4H01-vlL725tyI1O&~NsAfcSqm3nO7bDdwws1rqP#_RcWx?R=$${}^H4WUVI6X(rVVyefsg?0Mz)eW$U(XmTX)*6WNi;$qpIO>~@{GsYE!nab(ijT{b7|uYRI9C*VCvl#1hOQRPtS1IN#7~S4;KN_#RxM&)}d23ptCt{12ZNnig{w0dE4^@8*A6SRo=1col0;ufCbzxHJHPB#!_s{3eSiNfX0As8|)wJzS#ms`{qN3Dr6I~M54)YoQa0<tt*ZKm`7zEYqz4*dDeD4s>_%4asf1e#{q{)lusEp0%$%nopFA;mL&+rD87<|&geyQ;7o^-Op$Gyh=EO$UP4pGTdSUjw|OG&CNllF=2Kx^^5^;x3)r9lpu|^@dJ0B6$C*uf*NfI*Ghy-Wbz)UySIVUtXH66dY@9%LQU@fsYpH5l!GcU0Rg~oo2d`eU*2jye+~v1AR6fYHbJ|SBXo0W{gk4lUxwTUJ=)zVP?m4io7~yte`61^#^Ka@1!j+b~F}cwexR4g>%@;4g=lf=i3cd|!;I6_w4x+6{aF8u)5jF^ajDUw5kCp8_qF+H})dPyeddGPCHa9cTTjp^D?!YUQT@B$x^*liqlK{uK7=1+s#m?&~HF&Oo)A7|d;v?Wz91RmGEF6Y|p@YLf^fDwd)8}U?U_Qi3CS;hL&`!lx@Hx%pR(S;tIaq2#fyvQey6_ep3c85C_I>~H^R(q{HW<F^=!huW0huZ^cvl+Z7AjaxR(nE=Mv}ggXieadVm*?aI;d3{%W9?wf*L~9=uG(=kUarfxrB##J)^j1g46RkN<=UX+C;P$8dFfe!j8|7whHwUJk4|(ltU_A2^xuQ@y4d@dZNuZ|4cCRNYfWAJ#S*Q{mjLTA&S1yb*A#>LyAJ;E2lwY3adx+H7k=G;T!VYO2EHrG5}m@w`F;AdWU5Yq)%lJD9hWC<wA@znnK?iO|BMc2KU@iSNY7^%a>KPtR<obcCt<`iO@`8SgN=e@HQ~Zgkeg=N84*qG^@2rUyIs%ue}w>@aTlney8$==NcLiGFPL&7(La+z))GAd@r6@k-3$oQWmSDx)KQNxiS)0Mr3X`F{%wg+&9Sw8lQSQ0G*)i0C->^q?A;w0!KT?#ZU##?XUj9=ncU{0Uv6JH2Kb4WVg|{LV!7}6`w43&(G@_wa0mOMUg>#;9vW+qFuPHrm4w_sp)V@fKE~>9YKEjPkAg<uU0k1=D~mLCB>mH6FPz|B8C!b+rK-aefECI-}DAZDTwZgFeK5KI_IH86WOO!xi1h}Tdy5TRc=@jBF4b;k_1@d*4gnS2tj2Ar&E~Fa<@J5R>qi}_rnhjj{7LpvZ+Nr+LCh`*caMXPAsQT3h;5zL6G3mEo>20hdIgHcYmUCDKIPx*-xU(+uBra7W<pJJWk_j<pLs&NS2!l>RPG>xJeM*<P0B-*UMakmcwe=9<~B@h}5#Ts4x`82s_T%Ur$#C>@)zXF@2VbGXnvyEz>mV#Q_+H2P2|gc=B7$TbJz+2+i;jhd02+UwYdP<8_YZ_VTvgkfK(<EJnpAT<I~Nqkt&n@=+gb7@=O(V^&0Kd_2sPJvb}F0`h5`Naj%y<yfJwmvOr`5@kI1ptU9>1caT5gP+<G{fw-1v~k+8Z;m{u<t&NJeE{u*whFLaORl*^DB73=qRb~Vz!Na!FPF}u(xUxjxQ<i_e#N1rt`Td(UGN4VK-(}k+z7tkk?W*}J_b~0(Mn0jmk58<F!9YnfO}^d_SCCJQvwuZk(CD<3=Kalh};Ggs*OYzHXB?Uk#@YJ@D|jk1g50*mNcN4j8wABE5a~V0<APcym;jrgUP^fzO*Zw;fw)Y6pM;-r{2<{PZ1_~LG=C6wfCr+;;a~BWO*8lNDUhje2ymF^dQ4xsWW4LJXw@-YLrS2e-%g3D{==RMInkNi6iMks#6FCsZr`GhA5EN9LAh79C>zGB@A;E8QC8a=w!Ue`#gOLm1t`+a3vm#q9c~hMGPuuKd2+DN7IM5hEVNA0$WkbAA-!yU5Ll8UEPAj4Tzah7vqpp_UGwr2lI^?_FUSvW_%F~;%>Vj-a^Q8Oj>xBnQp+yfURW#1VK6M_0}d!d9Tw`Mu~b4lmWj`?8Y*b_HEn^xHSPeb#_ebC40A)3$wZcR}yrvp_DM|rY=6#rE;aydED(#sl~RWaF&PYt1(P=IX=Qne}b``Frfx24=9wp8{t^i5D;K<*nu2L)PK`yP!4I`E0`bEAd|n@hNp7SZ?+*g=RVOtu*bF|jd#g3tO<jIMkBjO@0ieyY14(E+bK?4(_dB-RgOehj0pH`*pdef%j~Wc48==G|7h9^QK^D*?unEF%oiUJePeL<li5cL$`fQ_oip>{28Rn|N`nA8XdL$6of0qNPF-ulNR$NSctQFk0L}YPiRuntCD4jg)sLussv*CvSdBS4(LqH`9Q%i8&<j4mt~&4Yw@jG|3en@o+n5>{unJ^q5UF#bvJTpcW8MEB14v4_JdvH?rr2w$@ZfTf5$J<@S$<GZg!D#+NG;RtZw@Rzln4E-W|=1ffE@{Y7dqopS_C3$QFH$2Kjzz|8J<~ezBVC~>4twnd0x;($cRyilr$oPC<97mgNAzPDShHrQ<MzUz{I7j>~A&Kum?V*nm_@%2Ek2mkzIeHstM4j??kNxBMQoGyyinIth7j^@;#3a^EsxsM&yN!Y6>S6_acc%86Mv*PqKPtQA$4*XHpT{lp_-F7t{LHD97hw#eDGo=m3C=a8wi;vDae}%{(OZy_cP0ic0mcJOE#G8EaK^Tlg;^##yiJJ0ke!vf^}r%z_#=8*z|N0wjml?I!%dxPi)ibs5GeNSK`#5-hb{S@=k?JIj^KhE^Sp9p9{iBps30_`y7In&%Jlz4Ad|=Nd>e7F*jryR|xAhc+68-F#Tv#>;{dFG&X-59~4Ezs}vlalEf(7FMYKi=7vMQFgjzr-U79bo#rL{u>H-#RHh4><2BfSR>SL#CuV^)P8vb0xafDMNWg7er{JA-eI+^_smC;+ugaKJrHIyFxm!?I~5LI$z8_eJUB0<t)d}b8A%GQZmcI)Iw*i*^Ai?Kb)cn-JJ;S{bnMG5SQ&G$+RuM*1Z!ttUx$u#P*#b1+G;0UWK<Oq!b6gwN&{o%F#=5hFw4X&Oc15#EOZM}h$Tu`d9o4_Lg1I>Vem7Ei+*AKTpdk=GoGM#M_k8Rpt4@Y#x%!C$kS1V;`sIX?%%)r;r=%smG4idk2^d<h(5SH$M%0Y8K_QT5{Lt4te-<za@=aN6y>W%*h``!v2AsQJjZlHwl5Y!WI9wFN`C{lAh$OpLj#QxxQ;qb1b}SdJJM4jf<MM65LF!pxJykcq8e*8#f^Y?j%{E1vdmE68W8k}AS~lY;6yK#Z;xUTOJ8uU1e#0NpANs(n0#powloof(c!mW-aWki<>S{|@a6I3ZHxV*2r|R|<1E(|2G;-j0p@JXaAC{e7)v;dZ2k%qxs8Cz_V2HYPWHJGh;AwLHN6NnQUJl3ErD|iC-9%bKDQpCY#<ijx^Nyi_z-b>R!KJ@8y9-_^HH{92a8dKH<t&8Y2>q@b_4J%wByDL_LtSRCdgCF=@@yfF?OlyF<E?z^#F!t2$~z$6Wjuoc*Kv-hEAD~Rcyky7hu1*V?h#ah_0M5uK=y{qU(Ab@pXpk90+0qlxNSgH;zj{AFOf^D7wrEeghDRBM!cBGX7S;xXnaoD59`HZ!G4f@hQp&f?4|6b#N6#i49R{oe54)S2M{ffkm(o3UCIvwM#D(pV+<OpQuCMDTZrCMM#FZXkGFw3VQlMc%PGdJ8(m0qun-)#}mV$aRqd?9eGdJ!}0^vQe>}edj?4X7_@olHERgNx*k_9)A?eJuRmyvjgqtTBnnltu85jVB$Cari`0-eil8544chBv7A8%;pn1!xhnH%G1R!*Y9Sp4ub(V#Fm#u#{RpoiYTlj#Lwge+y<DLO%5~%2aMua0-xH5@IkfGuER86Lm-w4<k5!VurI;O~Am|_oeV2nDZcdu})5_D|~izp{DTIlF{v5ljhlJ0b4?Yq8w#dR87vjNfCQdw48SWQU}w;Z$?GtLtVVN`O7;@$u*B!#s)50o^co!+TzQZ#K3Qn^6cg7zAL2_s$jNyX6~Q`?LcJtO`J3s40W55LLY7GgiXr<?S*3Gz<@{dF5Jq49a8Wu+nfH=(MJVx~a17!?`nIya>an&EDv`Lw=Bi^KarQQ0;O03zSgEpS?l+nzdS2&2*!*fo$*o}z9@N3&xmgNCk&E^<-pnKC;5V@%UIB}|Va@aWok#Kn2;>Yc`IaG%+3Dix#$W*@JpsN-~e;|Z%gpsZ9(vKh|isQwln_IQ5XotC#<SCLcd<^tT-@EV+{klG;#g+VTkll<xZ*Si(itKx*7Db=7&0z0Ac7Y5jbkub5rylW<XM}8(MRcRVqFuCY0eY5CXPJ)5W;ctj5TWb34!6*)l9(@E^<^)rhXX7<LD6U0X69Ao~7QJN&hA|qqg3J;fX#sRFx%NR4k5JY-F7A1bIJK6Z2e;s9Q-FF&pA*?H{8?=5?J@YY0=ObpwUE*gmg6YJ&mrU-;VVb@ygGWA(Gouad5ey$8S`Re<&T7+6qgv0bQ;fU`$ItLgr!*Cf+fVJhw+_G{!L~Ag()eqZL}>S5MiB9sfcMser3IoDx%9kiH<BPlRrRe3CTisZ^@KEqySEUSlAY>Mw2<IV-(v_JgF<a=ZI++oi~EkUw}2Yrx`ZUA~c4LvdWokTVeNm3@)RYS<)21V^l#em;mk=uWk+BQ2!<GayiSUE$p&_I(~$d)M0pTM_>$VWdBVsg5~M@OrdNOG+59tfi{6TAUCf$M2EYqKPC|+1BY>BYggvgCNX{~7=l&~P^Z|}rt#oChH-99MyxvO8OWW8%blSqMtzQA8gfm2rU6j2&G=gngAMA_UUdyz2Rqu45dh`aN^OlS(GcvQHkwG)I97|2l7g3VWEHOodUdQAL`H^B^{V5#6kycIKGikS!<5v@t#W9MSIYN^5*#oNxCJ)|{fKR{dcGhy2?GQ{A_Oc&2f~_;9<p+TpQ_-nSv!u2;iy<d3*C8ae|=G5!gxa)upX-r(xrWBn(hfW`EG^!0kfiueCB97;2hH8GxFK&(zn~2Vi_-#AfQV}X|YyA3=FI#jvB%eyuauIRNEPCZLgoS;#f%pz={|QDQEymb44zIA`Z&er3lEhUh#loCP6(46#0q<Pj+P(37eP1NsSF4LFx#fV*ic%@~zkcKzvJelt%R%v<HN6l-8s+rHm~J4Xdm{#Lx?bVH)6nw$J%ZI~2n#?er1a-qD_rkzqbV9_>2qunZ2{Ds*LR%UqV+3N;4YgmNsvtoL|I^2CCYGU(V66pp-8@)2EVb`f9_3b@K-U<am%Sh(O;N$`(ye@eN)ku<2du44sy^*EBmN8RB&8iWAz$~Z84YlLmi1|d(!(4?`*`Ghi@gBaNCFAeGtrqRb0Fg_W<S_~EQU=4gwY-F5t676%cQnTuK7s|95EDlSdgd@N6)OZ$gU}elS(n-`IaG;FogHCG^Z+;7CqSjKXN9=hilv~k!i&h|erw4;|gOccH-iH^VYA{5gvw3_ZZ;e807ZN&+=+bZ8A21X)_KKiG67^s?0)3u}O+r@!4_r{%cu{(35P+gzWakhjsYn!LI$(oX1+*mn<FO`;(ywI@Zh@*Jn{|(ecV!|BAC_xRZvApD#AIQE@t~ZDp(P@K9?qX^%OYdS7c-_9*g@u~KFS|vQF1Aq-<VV+BEFW8IoMxeTnVB_*qu2CG|r;oPoE#}&)=RNAAg)ljakP?ap^;wdB5H21b!*Uf{-Sj&`jk(RZCiw2)W%fT&gJqm(fNHPP~dKBE|@^*gRvsMt^tWh~Y%a#qXOXo;U+4MpslCP*Nb3wsL-n(G%x+H3<;S@y;@6iQ4r%E^Nm+`~d@!1*eY;UdzyisNq_zOmHKbrR}+0MHPZ_At*@V>illPIO}bUrw|z^IDpOY8}f!_%>M07$np>$xWlk>gD4P!wQk;^951a^PWFMMuYoo4K}NvslK%J*9*^eiHu*6V#Gw*+)mZH>IM7TiCGL;T%jH@ZbHkvMFdpC%EG{>O8%Cq}8sf!vL>gfiA;2>*@pZ(4H3=0nx5*IO2B$0oy<#vj6>wvt@z~c!8ehd814v`oArE>EfXS*c;Af=%P6k{i$;*q>`vQ1$H1AhC6HG=-81o4BN!WjhjF`)@`}RAXupNk(6j;`9cydQ=RLtozBe+sP$sF2<0wfVn$A8P_7KRoen!;bGGonnF+%GYE>i^lwSwM#w2XM<b?Z-&?0*RI6bS?TLE-Hs?K)vwn7rGpMkpzML2&X=))vaOiQ<4@O0O!GSef(S_!mHIdu>(pm$Q`_0Iv~m*D%qwI-j&sa0Q|+d)z`&3S=LQ_{T0r(&d7|&6ow$i(c%%gP7nqr=}rBs$!Og2S6>@Kn0ncS5)gna;K(tFtc@M^Joq-{M*D`Wcsp%vVQz>}B=eaSI6ooI!)dLKZrnseK&L`asSHveG%$`mr>IL32?Z`OS5&|?On~FKJDnh`wTpXL_a(_{^CQ?aLWcz&6b6FXYh;a){iu;hUY7f+F{{2VJ&kg9N5UnrE?`E(ow*on!)wb)QJ0f&;n=Bnx;Ha(`{sp~jOE}gsTT8Ntt>-DPU)nMJ=9<>g^#09j$ayKGmX_(W=QePXC!50y}*j!##m*=2>dzghKMRp6qmu$RLRmVqjwjgE2Bwvc?i&YuA^4-t;VlKOePLPx~d#PNBzJ{0h{#f8h^``Rc9nE`wOZ+IQukKcW5Elj$Lmi;=!1xDY<=d47-%FwDnf1EJwr`wmp<g0DK|LLq_g^4M5V?FF1^_@N!<T(K)Ka3|2m%_+ZOR!DgvA^yaZnc8FA@3u2H)F~?#tR5XyjI82mKche;V4dbNI-EpuaQ6)%3V)kh+^J11Az#S>kgg7{3R@5>WHDx<?ky&eBXre@|olpz%dJCkqYy~vLc`=oNuuu-07Xc7}>SNWC(>HrfYSkCE^zF^KoKTB$i2>P|>B(Q_+R(YWx!%T1#R^O(W-34{g2jp8bk`SomQe%Gp|>Rv1kd*Z3F?sL@JtTB4C%^)Q$}n=w>C7`wv5B&-DZSu!H_Q$x}ItYZ^sdzwWh#@KDJD_onfhi%?*O6Nxbb-?*@$NNf!X!0AGUAdo6%G-cWrZ!N(fXFO;KFbtu?abF^L&EokP_OJGMe0uZXJ2r#Iw+gqilAWTk31(e<wKZtebVs{Ps^{>Q$<ImR){T6!J!<BgjJQ=y7d_1&qU@yp>bUIPPjm}EkRH0GGjB0sZr@&TYwI#tYROY~=5ID4NM`wsw>mBKYQA)JI<m2r-!LVc%p=~l@nO*GyINf|sCy`HxB9}ZpaM(o;>tBu-SdtlTXn)srAE4<Am8JoO3R+%Qk8bfmwUyv^C?k+2SfPm88)AtZLE^$)6K?=uP<W)M<i!Z-QTpjx_Kk(pqvH>NVI1h-(?v8Im!BuU(UP}claUJ79qRX3-kzrq*@wUt_=x7*4|Rt+8YQ;jy^U)fiO{n|5B0RY;n4dUtJf`Oi**83UM^oJEc}fA`k5^j?@|wcIv(FF1dd>e4^i99fjQ9M1bsEF)uUd$Q8<c%v5ykO1&E{c+01hcsep;Ugk_n{F4V8QUF?R)k_uByoYR5~ug^e*jgSCsBwT4D;({9#GL0|@PDzS5BY2(-v(#IjR5X_+IsN8XZ%bdg21Z2zvQCs;fG$=$DGUuhWs-A60)BGaAU4Dc&+UM&j%ZuBeASa!FFf(cu2HU7hu^rO%r#^Pzb7$ofDvS4kRj~}F4hnv+Z+|@MZ<+erCz71;SlLV&F9t_7xE0$GIa%|<OGSjm&{KY*Br+<U&5(`SKbSQ;9OfmAN<xDbfoJpimfV2-~qS7=poELDr>Y*ZAoen7XYDIZd>J<mxc;jYe6F(&G37<eVFbqpaazpB8|FG4r#i=gC0X`xFppaQMHZ}*Bd9nrD3Bvx_J8Tn9a>{MolSl>(B~8C<;1_AuaLIg5L}adjHxVqEOM-6Vz}ML?df2wP$_x?)WA+fOtEMCUC^qTnuTA-CeDqV__W;RM8ojVw0rEQk&OGhC^=$FUE#OXkj1QWJ-TWupAZ9!J>p>g-M6X-5=|ys?i-_y->xCWs-$G$YLpi=vRj_0R>sAGjLY9B923<MaYn%yFEyoqoy@S#1qeiRV?vGJ>=%P;Rj|iOGs-96N%(mA4RY{xGdIS-dCFeE&^<{V2>Gw7Ogqi!8Bw{Vx<pa%&6H;%986gfXXdj*Yijpb|-9ItJdX6!#yWK;dVxlBX*dF+73~SHZJkuP4M4Qj?;k9^j7k*K2-{ly)+W{3KdDUp^`32Xr)K;OkxKVdEukU$-N?2PE&5L;WhU*5nFK1wEnJGeVps9TJ$g3Fb<UC<CA+%C{{wneS3Vbxs@mUjFI_-*&VHK%tnq?cK8R-uTZu!N_BDciCx5<$0cS&^ANbHT}Ow(!5n2=`#u%q&r|c;u25g4poXn542$E8V8Ml|9wtEM6EVmWoFl*MOQyAPMe(u*_H;$1a?o8N3sW&y**zLacB%@6b}zpN%_z94@BTDSeys7a0@ug>pm*)^W4!yWRI}F1JVr_zGJ<si)wvfhyZz=qZ?t6NirEQPVl0RwM6z<I5^dS)qvLz|eIS7~qkY&K3h?v)18TBDYX')))
_PLAN_IMPL=make_agent({0:_SCHEDULE},**{'hand_align': True, 'weed_repair': True, 'sell_lead': False, 'budget_guard': False, 'room_guard': False, 'clamp_sells': False, 'dead_stock': False, 'terminal_liquidation': True, 'front_run': False})
def standalone_plan_agent(observation,configuration=None):
    return _PLAN_IMPL(observation,configuration)
standalone_plan_agent.telemetry=_PLAN_IMPL.chassis.diagnostics
agent=standalone_plan_agent
kaggle_submission_agent=standalone_plan_agent
