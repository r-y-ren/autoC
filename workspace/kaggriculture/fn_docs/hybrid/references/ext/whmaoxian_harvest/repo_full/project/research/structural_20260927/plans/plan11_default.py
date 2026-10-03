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
_SCHEDULE=json.loads(zlib.decompress(base64.b85decode('c-rM%O^;kha{MoIo`a`*NKw9Vsa}a#N+a-N8*5=82=E#PjP*hG&G3IW&FPQVFC!x&v#Lj0`?S41V!x_-Syh>lk&!?B*Ui8D^6TIJ`s>X<{&e%>>kl7p9&c~{^_PGD=l}Tp#pjQI`{mbv`|E#x{`}L;A3pu%=hr{H{r>g4o7<Z=5Br<jyT{w7uYY|1@Xe<;A3uM;|8DpC^Z&kheEjd*i=Te`=1-q~T>Qi2As=?{-kpEu%LBf9`+j#LK9I4UzW(stZufZv+x5`?@agTlZ+`wf_m7{x{Mu<`i%}o`?Ux_rU!ETx|2sa_^@_cF{bq+2?5CR_9^QZa?#sN<r~U53$D2pFtnj_vrSI+VA8aoM^7N?N#fS4SR?8Y~Nk9CLyWKaJFJ%3$;FFIlXRf=w7KcYI?PL9<TQtPOw)*Mj&1<|8AO3fqw>RJK-aY(qbGz|J6c^~}5x00~tJk$0h@9$&hff#wb(_BoJwZ8*wb|X_H+<e~hrf|29abh;s~<j|#<zOZmzP&ss>N1({c-o6Kcc)?>t9+t_^^(61nPN*l@8B4{sNp}oYu)Yj(>XkU2hLw4kcb9tNUqb(PX6$e^WER(~o0@QeJ7}dFS7ZCoNsy-qVtwhTqIz)bQK4aRJJYi@WpuljkEX8Z=ndWFH=f4bRGJt|Zu)-clZhN9J~%fLONhsrHlPhpeA`^YHH7?#;)a|G0bq@$I{}|8%(;m+R>`k=cjUW50R-@Z(LvAM0FAr>%IpqgLO*<8-kQ#IM;XA8&JcOQKaq2a<Fuj!ObfAWn4mTKpbx8xDR!Sctfu`mKQBo__`}%F~dq@{)k7C&oYrTX#FcxqW)j>BGs<)q59S1NhzLe;9gPH2UQYc>HPnaQR|4E04xs)sqhg#u8jnZd7hq5k|!<AH4OjlC@10XY3y-#2JoOdHSHkA8@rE|8ZP^rwNoogwwCB!*(a)Ad_C&ZR(iIh=$C5wT8~mft&yQD{H6Ont$BPVR&)=BR{(ce$R2n(7cbUw{R63zxSLTR1=w-;Y$IGhrwOr-j(v-l5<xY6qpj2TjBT%PdJS~pNIqtpTlcBuRJ&bKtxo)r)<Ayz4V<`sJms^%79RRXc^)?1;CQ2Ge^GChI??SzizFD#L&UTi-5&=EQ6&Yu=;ZN_gOl^9~wv@oWDv(h7bG;Pw>OX_pkSV*u8)M7Y|N|E+{&rY}|`J{=3)j|4fin;4z#(o&T+~X&CSo=efS1N0&K1eK~qCO)!9=g^mLt8H>}|as6e8m_AsH=;%#ei!_#n51+gQ@!?qzIDg`&C~TFjYR&tUEc7u`u+?*~{)}&G9~Yc!xiKfc{`KI^|2Gahacb8?E#VQwh3EdA<H7UgcK!L)fNEBBcIdI+NS9wBfAZxjXO;&S62av$#6=nf`-wD+h>y?lGRGRC#|x6;5-wjRDm&2Pov}MK4t@>_pcjRpMntAD)+pX5F(6?m2*)_(fY9n70uLC=d1=m<BjxlIm;vXjK6_Qm*Ri&<(nCS&IKNL<U~Cy|rd|g-#{t54TK@HMGcCYjPR9z~b=DrnFvPnC-iJnJ#=Pqb&RRa_5M?#Taj>t&f0QtA$dYK7W?FcA`j9heYPUBtFbjv0$197CQaEFlRaw(x5lfGEK)rV9bo`%n)vxWdPjlXZYn*z^F12;YkIyD526hd9-g*ssCnau01*bL;dT%JhPQJ<|cq>^q8_VGbcP9ACCWQ2P5@1B(n}sz?Qb==n5kl1?M*a_q-Yk!wj4ApXDjZWV&|q`|LJ>PqIeoZ*ztNYKK-l)Da!v!tOh88v8EA?u>V%X|_H2-ashz9C^g`I@UAHS7_}VWn5^&hc@K}9Px(ApLwDLKFAr(NUwTb(Q2a6-)iNPB3RZOd*#^jEO#U0>X#T#hKx)3G@x<T@&dT<;FQ_AC?xEPG<<d1^JF-C|~BVCoFrqdhmg-`3V`~G?J90W!)ady`O&8{<2uM{JZ)Oo3t1#TW2SYnZzWyWi9?k)=*M3gd2i>DjdA%i3|5rI~N9~73JgN<6+=P+5~INjsOP`wn}@09Q3beMn_g8+L80>wG=&?uo~_{9o3Ag6bk5uL~(Q20ILZUKnzB2hHRk8dQDNHXSfyy(x18`3M!W~~0IlYq{q2;VY_@wodR*ApCZkdjoODw7x^mfEdiLWf~K<Rp1-p)%W;TJTQB9-rQFO;|!@<OxnTi}?DLjDnT1BE>NcScue&wCMf<^@yCSp~vwOO%TA>Z;W|GmC^%;2*G)mL|uyH%OZ~Mc_?7@AwEH4bU%*}GdK}&04FRQ5{m;K9zOri%j0$O*?PaZ(XRPnaA;zTgKiH4h|APvXP|sZa!M0C3;<)TLQ+j=I-d=JqX8D2apNynv%}y)j#RRCK~rOWyBB`T-<{bR5{)&!N$KswQzb=6orHx~A)rD=a20D5AXaTIM+Ks*Y*s>?fY`i{O(KTRwqZ5Lk*G!WTxc*2mPd{ASbeaCx8QJZM-WwXW2sbe!4j9ew{Sj;O?!Cz#Bb<mZ*7wnY^q8PcOlml3o5|2iNFdc+g&1t_Xf)<t}60QDJ3L|`*5o%Yr=rqllT@-*RGw+T(7s0)!bI%b%1qTs2Rk>3^8#NtKB^B(Zf)8V&JRt@3M&)aP8`D!sDZMBB7A3G7tj#PPRZK^k6l9Ca2|>0o8cG;ib}2X^^?^2}N1C#Tc+77`njLwuxy#D2Jy!3xi-ml2`9~jrc#F(zK*Ki%0yb8F=5pp=rIsZ2~LR3!!(q(x#++5QE!Ug+(1;B^RZ+uedr*h9H<2N+vb(htaJ{->?)eFeqvjmO9tLOw1FaZF)u=t}EBpZ>raH8qX$&reE&XqEGr+FL3xN6UG@9j}>6y7}{5DsB(ZaUDyf-F6O12X*!m1o<Nl4vl_SBFERFAJbuo{e&#Wm$=oLPQ#wF8HLt|2jSnBVm$s$)29c5AriIXjWJS0J+YrQH)$H#HGm{wOijO@*0yX+K@SqnK2Au3{h%E~N$KDe6bP4{5t{enzW~^#VS(0krEDE2Jd9$<tQZOs?@K$)()Fn&Bg|kQ|%%VWkjJ&4!#!#3K*qX+;XRH%P0}-R4KvkMm444X!;JQSVi8noy&0}wbJo!)Qz?zH;a`E03I*TCy58785Z~ptY@BZ{9<;hQ6Q64f19URu=G#CYVFvfF_@K7niawI)^jIa2JB`<-MzvSS@3<sYSDd?DdS6B0^>r_TE03h+upd?312S7>XGo40z%9!{X;&BRgq`lZ^DSM?s`&F)Da$VSgcNau&SNK*$NZ1Vs4R2K4hCn1X>4(Jf0GD$k(+!sylCQKi*?!W3dVBEZ15`n?d&G3G>+G}Iz%A~|Mfzcwo=`KR48kMu9`e!!S<f+bw6rvg#rC{Dbg)BBo~I9XhOWbt5itgWJpRL6^)$S_%M$y>`9m9h9asM2!}qU0J~-yrOa2$9%u@a!qpIkcgdi3fBWVYoYfqYWJfJ%GflA4m2nEc=obS|m0eJ<cW&$pkh5%J@*wF*bAXQr=?bgK%w93H<d;*LK7K$1jqH-gu5wF^oM3IZ^g%vOR*{m|yj?3#@<GTWeq0KDfw%jHDZzn*!&qzYKVl~QUF6M-;Y!f(pQ7mVP6_<r66-fm!`5P51D?Nuu^-RPpig*-LB_ZV)_tz+HxyNNWak5nS#%*!dnQgm$w2@N2$Cese#2Rx1I3RLNcGIid71qSnXf%)KWD{1yOZP1nge%;xFz5zSsc+skL;I7bX?^?f@L^YoYFrK{sh9AHM<~vA${wBh79y9Btp<EuZ}bl9trV~I18^d+0*(YnI!@}dXl2&aEZc`^U0nqPrKh9hLMz~CiI-ztTRTFI^)2#p5PX=T<&RDqk{c$wW2K@o2a>210vOFwO-L-k24&1SD}dz6-pD3v?jGPWHQazMJ^@ZoKPR=W`*`zk*tUQRWjY0|qZI;ND%fEs$I*J1Z#5d4PR}+=Y#5Y@F!ZqNkZXco8w&lp@DbIFSlLI?UCSXg#Y@w?%zKu#zGIgbL5Il{3<;-fp2>hy$S7?x5n+>=P@V<=P)ilg6#q>E>v?r>I-!`SJn@xa<s1wGO}xWQ_>bdu{B)_en3NaYSI^J;+WW}deeFx$-^e8+y_h3B$)sM;C+L~u7?J%sff(Vdx!YElv8-7w!2B-QeNx-Ugck{wXj>F5u9YBy%Q1f+sWGO^uo6d@Cx=gO2b{_9x(DH+-$W;lZuwYSvgbT}h-90pnWgS+apd5Zh%185Z{^@apNy`}pt_V=93R+078b3T^h-Dts=S<~0u^74oWlwH0G<INk%o8flN!}z?_Q>}Jv+j1wr&<xgwm(Ah<nSg{v$#3dIjn}U(AHC&Th**3^>T_v<Su2t~67g69ERf-&NB-i`RYl4{RBc)BK!kHCof<1F^OpZB-)*OBaXU=|LkbX_fRqW8I~cbgm>g;LsOLnnlwIryqF<%hxy#YFywJqM5|yvoHT2V9mgE8xIw`p=ty#lrRoMFI;gxUWhjSZY*JSc8B_P7A1cA1ndT#7Djt|f|gO%_4vDBUcUhQfU}(KDT;k|S3e$Es5COC=}Au%2R7a=IsMz3pmMT);1ptvLY8|X$5V+kM(KI};o}aB%NptX&0~)(eJzx&**>4Fk%;;`U={qcReSw}e0*J*5KF#QA*%*%$3U!VuU_QulWJ_HHIO0_-3GEvbcr?!Va+Xvn}|>c*Lz-y-Uz;eUh0T>U`kbK(MjXGMP4S4y%-0g7#woQgLY|xWx4>Z^l{BjP~u}@R(uOA9W+=U2=^q`K^6R@K{0?ciC5QRt*>U#@s|hO(r=NI#?BV0aPAll;5X6=HBw4s1D^8$9W5)E$-06`^3&dm_^b4sL$z6{O!e}N!N`CrBhPFyjjT%Oluhqs3<IUqOO9Ev4p+qxdGSZG!XCa$!K(@20#cg7!Bs&))ROvzL0}VEpaR$y@5bc;=(?v10%lo$u^^6NhJ;kq>q_F_xC5<Ak795Fi_0fZf`JHo1Dt|TDC147OOPAe`@D58_PB!E5G0WUpTGpY61HSdAihJqofC~7f~jMJYsuBpDnPNKrY1qLi{d0u=K{gGuW*cjVEtyaI&k@(7!~JUBR0Hn_`)E+8l1L68a+88G53qzd~C9PxNGaJMIZvisNWw05f^0gMZJ2tQZx@hClxBkHwc2F6wD$+f7PjW1EF!DIF#h=9DYIO+mx%={B%PS3-|P=48`xBo8~D}h7daIcHwD&^}15puLjk9kX|_JaI7@Cf;@cyn>`Yd%}nDA3;+Cp&<%x?uV=I|N{VJ$gKsNPGoTmF;9RK3vXaVV1460cr4K!*57TY{lsNcaF|ZB;+|r+ZIa-Q$F<I&YP)ZXhLPN80no``s)RuGt`cfke9Rg{dPeMI{c@Aec*Xw6_f2R%*k|zG!HI*)w+bE-@u$xkaeTMxC3*DgwfjPleFX(Mw{v=|3_fbSz=u2;E)AC4avyJf3(h%h>y4)p(v_yG4!im_F);vL=E7j4G&q@Qy!<yG5#ENBOVrNtU9;Rh85$l;q+ZiP5K)yLhQ5wyZ?xku1Z<>5-w>e{R6v*K2(hoZ8QsMHjSUtuBDF0vNc@TE?IFn$Q=;H~tdNFe|;@#&7et3mu%ziI&E_sxGw9B<lJf0}>BP#G2DH^AJLK0PLo&3mw5qi)3!{g-gh<MacezYz^tT9~ckd27ZY>lr*w?V&L&#j(JTv%gkmQKRR3yH@QsI0;jLEzt}`*0Y3(%@bU5DFQw0(jv>tTMpCu@^gGTrEVKWANl<f7Rwn(O?>-GGr|SPsrB8pEg@6Gh^C4D$BoFab7x^HZH&)Ymo^-*ap60eo#~L#Hv3r*dc`_fMMfx0ZMFH#A)Ddr_GsHvleO*!|rB+&kM7mOw~>~U)D4cuMpV4TneaL+|x#8h`Vd;UJ%=I*$Jrtv~odT8q5XHhcvq^mC@MC0dFefHJh_orGw+!P$M#TS4U)m91OfLCGm!oyEasR7D~CnI(vQJmJ<N<c0PQo4r~NbN@ahde<nr+35NI%p)GY9ZPr5Dz(TYpWM;C-kcj#?ilTo7BYtp~FybsIQYsckRMeFGsN1hJI#cBRJTPSoR9+Fonqu$@>&<v0CZFQTV+bCPdX@AV3Lc2AS(jnKgB4;`EiA}|syN;%Kt_eFln^1m292e1>RLhjSw#>%P7>JuJjY&VNf6Tn<@u=C2X6d~d**by>^G+?lyKTq2BfS8?uKSk+tn-b)Vx)wqHlyzb!w`yVdYj~;66o*f(c>Miua+yUpvK5k-QYTq{k>Eq~Uu89Z={fR{&8<8CHehHZd06>}E57D+$na7$C%r^0d5ocPI8pjx(77HwdS0b%xDka-^MW6yHF!MLi5}_wBb%zaAAWKY#Ns7=_NN(}`S-B|5UL^bNSz^8>(9tn?_9=s5G?i&80WiA6cQ3IqhTah%Y}Vg#|@SvijKOrqnc=ke-sI1C%B)Y;|a^%YN~5_S*xx9X0eSgU$h1QAK>sxHk)vgEv17=J;-@uy!2!i0)!H^&5L?S4pv%jRkM7PQTV!IC&4o7hCt`QYaicw!qcqt6sv)m7qY3X}q4fUXP|Et}||M6GavqrU|u%SsDHu1PcsVbGLsHjx~Szf8RwQba@PcV6aF&`)G(dfEd%(_OkEiN%#Suu4Bvr-ISh+|DMwppJr=Z~@B8Ycv@aU@i;twgXM%EC<PpLB;m0opdxVkC!=3^s`pm?V1<25?6y?z6{E6=PH&HNjx&Ow{hMSExEguN9$Y?U|YK#s_=c)et@AUx6)S?ow{kKDkU5PnNr72^-^T;Afte*O`KLb5(@eHx1f@w5mT*cR0gS-YYA8+dRCNI0yGXxMsFJw;#(kL2?$>)0uu?VPHJ4Zxn1pn6S>1CAdxw)PIzjJ*Ht)-PvN&^A-k|ne;M9Oq4A3b;*ugwaSKcHNf@LY2GTm9Td9w*(u$N_2rRj3$x+I?Bv=d2Twhwkww6noK|MhatR(h|+L(2NC%7k)kI^R!h!|6t83>b>R8<q4#XKDn@ZSjZL;Lzlohj?l*^1iHQ5m7J0{8<9ee%Lf&9&?o$x`ULMrI;#B_pfZdH{-<*^_Y<S3SjN#I|H;EvtJ3No5ZMD3rsk!Fx39K$#MS7@Y=sy|^|ng{;oQ66dzL6t^RqsiedEV!%#+HMWa9lHjbVg0r~Q+Zp{8&<HcMuA?YU%E=h{%M;PuSkR$@B3?aqNJvZ_hqeq-yfZS~qKic3m`POW^tIA8OWt;+psLdlw%jgUUdm;87Nd{QbLz6lR@els5C<T!%~%bzgtJ}^DX_!<FXpWTGRVmQW~*#I$8AAYRZtRg`CU;ZRPWb5OX%KC$X}dF>slmce5)svQuEOp0e%8DA>moCesHXYrm1P+r>b55pvWX3mTq;t6b+eNF5A^CIkvHi{*%+N&^KY=uG6qt^zLSN!p6DarFDP3I2A9Y<$bI7tryP0D&GeuLAgJ<Z~Y9A@Djz+8|qTjyV6`Z8S3&=y#j;U#!$Fat~)^l6g;Uyxh*!H1Zku152Nf;xE!7L6&BfCjHuII)t14GFR__nSDQtJBxu*yL@}We&jJ`2>48;*RP{XFj#%&>8QMs+6|IY_GJ>OqlzTj_mTU<Xg97(X=_<NTZ6k2D$SM|PdnVU0+Pac#j6!J9+8_y!K=k|7(re^u;o>m91mt1i9bp*GF3%qB(%ifbSYMFB`!2I*d61<dwfDaT<);i5ZGF~{DIU|L_-qCJ!RIS92tNc)q8rsjj%<+wrdrslGB7*aH|01wHRui{sHD|7UWDQ*C5yflL`=aWRCu)Kiyc>TjN+Z#lK^x&?9>3KM)8d=NQz$@tsm0cf&)6rW|MpvEi+hvO+~fEy5N-z?nw7(P8&g55mtS9aUXcHEO9WPsa!?Wd#0FrQX$p@)4-MB2~zY$E=%b?1~_p6s)i5_l_n%=+<it-8d<j>*zw9U(IAzO@nowTj}qweKe$&XWJtLfBC9QFQ3z};X4Y>)pn3Z%G}+;(BB|46D7aU2ahKS*6Tur=im;XiM(PxPFt4STwcytx!m)C-w2;c%f?2^!N!%6QCT?Q^Dib_huLh+>@QPW*iNgJ7o={F+qkE%*5oS|!-Ah0m!-qa4#RWL%_7ZZ5Qb4q$H-~yasn_X)29)ZJowgNRXnQUA2OQ;o<LMCsQA-bq*Vc{khz7gBf(oQ(YUtGH`zn*7SLadKRc11Hv=_crGyt6Yw6d%TrqzXh94l@@9(ids^qr*;N~t5+o^pD;K2tVf<FNf+J<e`;Lo0+bf-mP+_uAKTeO1qUNtw)sLpTu_qN1QC3C1#4`{j4>6z+~_*KtOh5H1gCxqlVi&Uglh{p}J{iV4vyT%n;Na*&8`4q-6;rsp<Y$r_651}Uv};q<DwMh6yRIx+)PZm8VR>7@uYt#`}&ohpa8tGTkz#Gj;`3GX?DcJr*RQ&eA`#L(u_bMRxJ{LD`?vAqgw1fj7vYd9&vMP441Ch0hH25-`kJb3%96#LcML4L|oSC_87(^f8Du4t%jd{v;cl<|v2<%SuoKT{#pwh*0fbevzHv}{-s#+)As{%}+EOL`BT!3f8`*cF$=g#wchq$34+_}ve#*1;MCI3hpTmEGi*L8lxyhVR0ew@Rdp44>(*Kb`x0cS!5z9S89N-0fmaIwZ2F7xIYqZlBZZI0=n-p7T2t*`}ex%S>7+@Nwm!aaE9xKy179jW}hYc$LTa6(v0-$rIk&MA@59+bX2*Z5e8nrQFp@ycB)f*Pz-n`K#qaU~-%DAdFHJaE#xNnKuLOMT1!6?*Tt5cf36bj4wX*%My`-3y)A`uo(OljYq0~i;Ldug}yGmno?0xNNh8nhV4hnu2GKm-KKBpXzx)6=JWxyQFU+!uZm#?P6>$Xz?tBDAxoy{N)QQSi5h(^r;Zp{j-hmBGo*2P(AV0d1dziP>2Gv`L?t#OkjzRKt5-D~7954g^E`umT%i-~fr0ywqdZ4R_*Yj~xbfTMVgUf>%WajcQjov7OACDD)GKMpHG#tJ@xz31W^h>wZH|Kn?RQ5h^b#qsTxesTK`M(3;I($Fs#&Vn+s9WxeLq_3ZOeqbG%7LbJHe>=(p^$KJnKr<4?G<XMKHe>$y{{1=tvcBqct#XU{i0Mdppv7B1>ZXZV+-7j4o43B!q7Y0wIEJDB|}Tx~a}s7hG)X8u+@yRVj@Ia6J{laMQxV`GXp1TmrMO>V7E?*8xzNHQ699TyZJ5=_!s<!6`89L(+K$O0vkdmn6O{Py$Y1x6#}4>D`KQL^^%3--V88w{#>4I_<7CL?XqCNLp05LJ5rB{)pCyv8l9*qgLqlA*wE&OtgzoZGfVdL|j>xR@A8;=MoSun{aGRthz$Dx0fZBXd|dr@gE`D2-y!&%*5JuR0^G50=iHp5AveCOJ&1L-V#e;O)3fU>Twq2^hB%rja8MmHNXj)3oB;P0Rqx5m{JI3k%$_FI72GS9YRqg8wd`O@j{fI^7E8Q3EB`MJ6ONiq*UxuA!X$Uh}!!)B{az``Grz`A;(Nwh`8yF%@F&oA;O#C{S{PH*V_#RFw6y4Me`%pkwKa~Lw^CxLrLjObI~z(TcO71z4=tKE(+u{u`P6WhfaFvx06(+A3R}rG68F!)7Z8sK3sqqYvAv`O8V>4%T$Y1!aY`%Mi<!fyy#X^UPNwH3t3lkI^DL<g(|J%PB_JeE-P$W)20dJE{-!eviojxb+;6#eKq4Ge~Z!!s3^Ah>XScpH?=-eqm7mXilsR9EI4E3Ww3e3Mi%`dP|g$!4`Sp&OFTXO+YD}198*rnWJ8nH?-VHG-D&|=;MBjF;%Pp!iNL-`<m7&>q;v10OZKkdYRZOF$u)Wm+SUE<5ooH*@06?61hz4zz_TD~jMuAqqGiJGYAwx5U|IFSx+|bfv<=jVr20%XP+O&#t0dZuuv!whiSGjX=V)|GNhreBFHYxgNzSlpS`-yXhEvAX(NpR1xquD@jB`(}XV)=&)Z{KG<-ufbo7N49MgW0k3#?9<YLE2|&MEXc{V~_7z$l)D^1Iqyp(9RFz?HRcmhAIVvC&KfM@5!)#j(%v>*|A8{3Hb%64J4%0&9a%8~qxH2%FuPp(MO-un(@>r8`Dr;B^kOs+rjp42(ycyb1{=RA%%m>TY=u`BP$R7ESLwap8&E#yOBFb7#pv0Wo)8DD39!?z~1!LdmL9ZK-;RJB*YIz+jA$cphZ*1)y~B=>t?rOj>8wNCO0EV)jG!C>3&pcZv=&zV6>1J``(no5qU14-_D?)e%LTxP#d5uD}K0wV8eO_f2pbuBlVX=0+`@COy6Ake*cZ7)4SU1qyl?z(FykiHawe(ZyWQor=4nBey!*x5=w~tH6d?fZx`P)>@l8qq}@j<hUVsoO1>BnG0jO*4sA)7YFm=#x=;`S{XWUBGlYgt`R=0a``;{KnBVe_px82$)fNqC8yec73*yHW&pTdh9gwkeAIjTxmBmvXpbz9IFzcBBAeMstkL=B!1F}O6zL6bsyVeVW6soz)wY_~zaKNIcG;b18fmIGp&41$qC^AXu^-T=%!Fm;pkfBJ$}jDkNGca8n3j_$_mf(ck5iXj?nJHWV$Fam!mf+yexAeohmWQb7^xExWh9D{;qfSrVdzWa<wT#Oa;CHMD3v7{YsHOx4u*d!#+N5xmhA0=StvQF@Snq%5B@80$cjqFcA*`C&FKNJkM$ZlXY{fCy3|Q*(NG*;urN`{Y933>rn@CO^SDdx27F~W>M3-*|GTNNvx~bV6s4Bq8dZ0__G8H4Cc;h4K4iS(o|(gc{;IkHhQUN!wXjB|l#U1USqGYmD--o*s9(?G6Mrf3xxTo&A|eL=s4rX4e=688>X~X@P?er}q@B1T@D#d>p*c+6U=%e%)Mdi{fDx3*y{j6k<V&?x_GMjJi?IEa37Q*DDcZGFk|CQl=pv4*YI-G5NVVK<XL+mgz_-%lIWr3O@#B&eW8v#uO&(V22g;GtQ$sKnR%1InRm$Ev&CE(Fxa&Mz>1yIdtZucNDZbqjIm&<y6Yz+4Ah_PmpqBni?mzT&_&RD`g6?Cs<J6U79fyPlyA<PqVHH_tPbel6PL6vyB?4IrpH}T>ZQYVGb^MAbsU|6|kcDX*E#5@s;qg$jB?JHz+e?D~<3boujoA%}Bi;ke<PsUC`eGPmxe$N)J%}33>yV}@&C0#gW&kc;v$PWQ(v(cJ02y;<%<iieUncL^RFLeuLi04cul+DPu$H&A7!Ub{!LaQzF(5BoGfLUGrc$9ZQ%5SY2@=v&A}d$c{zEL9AD}IX1|11qhe9e~uN0kNd7k!L1Y%k=ZKgAilrUN#s~cn*VC68II>qZ@u;GOXw0Co({dxiWv`+wIU*xe$Z3}wgBV>FK;u>?di(2qQ94?({1$Zu42!{#7{#i@yu8mF68dGLLdm^xt8;a<gqZ#?}aD->4;E6ch8*A4nVEa{4XC;ioz7CH1MFoP5a7Iu_j@Gb<bsM!vp#q8zB`A6E8^>`<DxkV_`ow9lx8<t}V#+THC2GzoMpUYKx5bKTRqCoIVy7N~m630_s08hvN;Q&9ouREp`c4a<m2@9KA$Tl-qmg{7oGZU$oM%{Nb);ol*0Hqi-OOr@27K8@Z#2~w)Gs8`u7LjnS&MBafmM?DZ7SumWM5J&JFV$tGa#Wjas^}BJH5JksLeowG~@E-@#%h47+70Wya>F0_VRW^GZWF6F3s8j*%7uM^Qr+D)Yg1AqzR23?YJSMo#ut{v@pwY)jR~p3-_qKkWeTup;&mR^}4N++QJ3e-)tJjC5XLlXs%*u+bOqam?F+CiCk46(c<uzRhYe6an^dw@Th8KDgI`n`P8$5aZ&fl20S|o-n7(!R0ea5Mer~3<oC-Sd1}8ap;4^J3r0D;K4vB{PL$_6IgBe6q)7R8aJePII`V?oJTP#15hV>;b_>GgmM$k-Gm0Ys`5u-+w)M%+H82iTrTSCC{p|M?1@`|m?-HIf*w8hx$3>A++7mq2E#k#e7{zgpHdnp$gyyjNlJqLAA)3E2P7`P+ZNSD)Px5?sEfNik;a(R$2SZX`t;Z)4q?&D8H^`0#I*juouECLeEdUMAl!B;EH_a-%`3mY%fvTOV5j%md%+$~kZIOx$@Ju?e1yy61TEz%M4dC0E`$=-l3L1-c5-<l#E8QaK3#HWG1dD4Jex^(b-fIRM3f3_1S*$Hgyg$|rR|NJ6+pb3T#`|2#uPDaLUiG@Y*Elc<C8CE2oyrihF(>OZoMXYq-KH!fBv?@)7AGZB!}czuFS#T+e!uN>JFqN+mK@!G;{8=RYZf|L(=*A-NZWmEs0Rm|A_vfcmSe<t)?3BnhWM(qj+9`;gVy!<3ayx9rO3YHPQ(KyE?y~2&LWI-M>D93VPq3{0;dCTS<Q0%auWydj6LpU+0wffIIhtmJ8rtD`=c5>``=g4Z42MBrfKw^>Jnv^#=f<cl9A@+7gXW0k5OMu1k7;dbk!02y>r*uO@>l|{bF%IyY^p%u6gxC)gw^sL`hdMy!8?<t=b}TUkw#hr|@RK)RJnaM}ZeTgslL_q8Y0wqOc3x8hQ0d6}LKZa^I*bPBGs#93*L+b1a~y1MrDwG^yhaQ$*WxEL;(`n%tv9wS(~z@T7IZb-eV#7-~c-s9`!*+d{ex)PN-vqbH3HEQhU7EpsLGVCD}@8s}I2VfvnWjGdyftiCbN)uYe;wL6U%7ShU(f*(>1uFe79ZEW}2#{&FQ)`|<=fNBvcmIOI=`Ianxl66<hknTl^5VDg56llp6Xlm;oYiyu2jd-T-9n;ZP$~hg?<NpBjS)F7')))
_PLAN_IMPL=make_agent({0:_SCHEDULE},**{})
def standalone_plan_agent(observation,configuration=None):
    return _PLAN_IMPL(observation,configuration)
standalone_plan_agent.telemetry=_PLAN_IMPL.chassis.diagnostics
agent=standalone_plan_agent
kaggle_submission_agent=standalone_plan_agent
