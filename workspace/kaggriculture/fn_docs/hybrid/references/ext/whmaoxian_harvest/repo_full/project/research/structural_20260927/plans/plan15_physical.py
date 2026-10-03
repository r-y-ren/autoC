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
_SCHEDULE=json.loads(zlib.decompress(base64.b85decode('c-rk<O^+N`a{MoIo`a@)IHY`=rFtb|DUHC7ZL9@C5a2Zo80&-Vo8kX%?o5AFRYpccX1(S}_MX`2X;!`Oml+uu`O|-2{p&Bk{_U^7Uj5TgS3lmre}DDq`s&|)`Hz43&(B|c{`j|Fe*O2q{@3TvKVALd<6nNh|KZK|_iwMRuU<dwudZ)CT|a&O<GY7%KED3&`TPBMyZg`ozWDU%f39bbe)IZIAAg+u$K)mNcW>XGAM^Nv@7}!IU5O8*ZKto_f4AFxZozihv_E`&^Y)vcKllB^$H%9gS~h9*;r~89lz(}CdHfyk>T<;1-oM@*9yn{%e)s;vW2a9aet3BI;k(IKa!BEv-K2AN_`!D8jO9yb?O2RyTuA!uf86c9nRk3SQPUTmKOM*IY1BuJ#i5VWwK0FsHEQ2sL;ZC1`W_F%`@eVc`s(}L+lL>nt~Y*r;^;iR;u<w<v0|ppkllR$@NqfKv7cz!q3+2}ESKC3p4+EAarz7C&|y@Par)uIsdbANJx*L{peFm_{=@Dae?@tymQR|z_%MpN1?qi=aSrc0J^`IOu~*?wPmlFB-@GO9=2%=x?nod0rh0y(-$(je9%$or;hFXT_g<Gg8h$f=P{Xt5pZLMzpVsF`o)5Iyxw39l7oGXi!^?In8rFEcS+6+`9lRdMCvuKn;E}H%-oD+v{_yi3cke#DdHd#{=OZ)kv}0S!4~zGI^X}otWG<MYws^|%r|{f6-C@Mun{<C+M?(uE+yHzSLmNtF2AFlwxx#40F^|nVeS>;Np1rh5HuLwOVM@Q=-5(nB^ue1rZ@$2SIq#a&d#A_IqbW6io3cypv<U}ZdNPCKQ2HYv3?$Hf+{J75hhsxsgVvrMVCtR*C46}Lu^gHW9-8f{H3Kd1*hFuDRyL(JLW8X6?5)fhh}SP^ySRK0ZC~Y^o_G22rOdU#ulI*;`D|#8w+1nJ%5~^r?XJm|v*l3&Q#MX<wDnXooyRf*uHaUr5AND&r{@f_{8~@Eyy55V$ASTfzmn!oL^Z%3jE0Ye6D|ybf-^30NvCV^4QIRUp1^+LlYu#IK8-N-;y6Q3R&Ftdy(x1t9sABG0BljbJ{uWt9IX3?jn2ZV#!Jvd-VCG_nU5Q8S7v{JSkJH#;<g;{+bHe=&WGED1^WKOyZikgcJJQ(#cCfrw3cl#28O>qninUNkC{t8!be~K-Tk{i=Vn@L!1?$5n)X|8v`HpE5;i0Guxc#8R3H;Fe3*nHRt-eBVc=lL57VEWKCiVDQ`>PiPx$Lm{dbz>pWv5xxoz$Do*x&$_-VDh$)U^UatQ1-0M!d9+IBPrfP=EcM+R1^vh;MAJ;JFZ5E++wW-nAC{o7HOGc)YhyA)(#l4$^!MFA>~_T2eDD}&Z_Hx_R^JXPD%>9n8Q6<rMdeumM4ZAsk<c=#KzEnR%}0G&a))S!;`qjObL@Z59S^##3lm`sR!GaD%y2V8ZP6G$8EP-r}5mZSl8U%<*puF!REM|8@%4ak=Ag&G4Ku;;cxFEK%DtzlsKT>9k{6CLt$aL$$E7~OXx^Kz^ejkqA4HwcG%tXIHdOcXa?6)AB&0qU9yPvF+{1UA19Prx^Cu@SM}@ZVI7d-u~g^Bz5YsJ%_NvFEKH$qCHHt#V@$`+jnfDFQ;lzK`ZJI1mi1wLZCaq+mgWc0;dgTnK%(7vnR@q*;Lh1KQFMN{K^a1&!e>ZyPL;jp$r~S<U=&V*-1&frUS>F+L={<V!$=|9JlYkLT})MkbJz_hoF!-z?>0^QnF}pc8WtWrF5uQR{XbGbA3{886s2FbhC&PWD|#xjr4+$`1f`mXVy)Gb2x?tF)gh=1rWyNUJ!%5crq6zle&rf--@S0-yGBQ{ThDN;ta_E+TCpogLx?@Mjjj&WIN~X3Ub8b3u#NFxuC}n~k_;>jedScr8GA5$0*l7;xSIk_F~}8sCF|*ptu8x+rV{i^L5){t81OT>qD#CHOYxZH+>Pxqj$NVwV*N4o-5QXZSIqK_l@C1Q)MilJxo0^uO$#z~uhn;Vnpp0>h2WDUj+W?KjirE76Nj&s0_}3WXmA-ZV3g19n*KZ|{Hj=1O}Ir*{NxgLMqsC@8?P;BXfbwGn_-zS595P!Gv~)Z;JX2&8`jYiDvB;{VoLNRtz|JW-&PwRwuOQqF0O$`*hr0~B5+U#Sp&Y2-aKJ!0QWoeVwbXUY#da(dH{C_NY$J{xnRFRXXg=+FA{?Zd<S9TFBgG;WPMnavNAyopI>oh;w%3Oo0f?hm{LW{VHV#RS=obi4F7NwVfv(bAS(iwi9M1-gd@Z>LpV1G~Mrp}gqQ1)Eu5&f~dTL1=ke<gXt>=HF?2*j7fvN%T=xF>elQ?rDFE^JsE^6h;=A8AApcZb&+}@ZMFezEE4aB}$e+*146-AXBWt_dZE3z%0{VGySCZJYC#dr3esG-SiO`<PC$hXk}H@z_v<A>{6IU*%SidnnILghtoe%_^*>lEgPV*|3-Yx#)WwJPbMuZmp?bSLGM;$5;EmkQ{@Z}9SyA2;uX@fGMa-f%*CSi4PL!q=%R1A=gW9W4O!_2zao=V=kQ3VO-)$64<t73LvK*Gj>++qPL*wsw+SX5^0!fzQCI8^gz3+3icEkt=frZ+8)4;bDce~mG{K>RXYzJF=I0C`86@>=RWIhf#rbOK0J@6O+k$U+9#u4W@vmeQmu9){fc9Ae7Z&@ncxcbtYZ=n$#o5!T!eO)}liFaDw!y!-*w;0j;Lr_X18Nwa%nY>)ZH0zL?@3_X2+x;xed(PY6)ESHL`8cr<uM>E9Tsr!-RAk4vm{z%tD2A5PVfPN>SuL3zkl=gPmhs1?r=he<{;<u(Bo4}q^8*RQz2{0w}}lyKX#}>X#~cZ8aNz>$0j3b+c@HCBQDNh=}IaO;J7AUOt5p2*egXG*QYrF{i1ADokICkt=<x#nrtG&{-T-v(G&!M#_2JY>n~^tuij#e9EfPK$?Q2a!fkJsd4{qjPO$=Eb{7|E3sKBv*@_z)+`@|0T@T))=2k9jD#vZSen;A|X6acm^^H<Foj5Q4KJk`fS2QzPc=X<2(G~OB+f?FH$gjv&0k<g&*%z@vP?jwY9Wqj9j6SZ_;LIRST!0e4*Ot;Q?2%G)=#&s)&MG3#>Z%+gigE1T8$%YFf|lAUratv}Xo_hsTdmy!hO(BV7mSn0d;fUJ=dvT(n*)#K9U?0usouh3HF@5-rMlJr6R_OF?`ig=o>|Pp)*c-Ek=aEfd;f{XyTzNJ%~OvqBdOtVY62lcM<e@8xZdG+VWlY51yq@C*3MfK!1bNQ2qrTm97Qx(@VZmHNwE`@`!D5UGP`ZscM%J!fi8fOO+jry=XW((oHd@3Xjd+(0&!MJ3W8|mw6PRk$;vw}yS*{HjqFX-sHLkI7Zs-FOWv^FSS-}joo&4n`Ry-vAG9FBCsAHT7EC4N=>tX7s|SbN`Nd<f&*N=U#>-7u#UCENzyI)1Dv)|)nzEsWzUKKq9!KWzcIBxwr;iBe<C6fKt(*se@C8vCR?dU1QNatY7^|^HsNu{Ne$AApE~8)9CV`H_WbF~Wtv`=GPkV6!0Pl>JcAy~L=xz|nhq%4HqtN6W(U`<$=tRldpZvCAq<^sbXcnJeSTC_f3N`Hjvx(o&iAzYA=5kSwC|c^QH*mj@(j?Y7GotBy{TQ`vlM^j=#Jxmq#y(3B=L)9g?qT+Lr_MQu6XvovZ9vLpOHB9f-Nn@hUU4$TmTFtwrbGnzWr{)F`r-r^9gLeA<v!vv3}D(@FbzoU6h}Vp$(<1&XRu5JpG?fmW0MRoQRaL76dvJsRHsXZP_BpJBt67;EmXQNgZ4vW@KR9Ch`{2naL7-1SD*j<?txxoFFsXN;sWe4ZIufAPk&1<8d*QV%L5@g$!gn>j9}OA)68n4M!8Fu0y{|MiJTD8^Zx}PscWbnxl4!IeUDZ)pg~gfEOO#sSh1rRoM6g+%X{TTk`6X)9SyfDr1->my!JrT^PVl9LXkLi`em^9rr)1-U<|=<Wkf<4In`6QP`9+pJQqeCv0yz%M%;9sfjI&mW-foc))VjgFamakDi|;Xcn>&d*`AmUMs{w&fF5v`!C44g4mqFB8f?)_@EW{pRb~ZfVqmbIJ}dyP6!FgQoK6rhU1t#`J^jj<p4jsc=$j#7i*LX+l(%QVQIiAw4DEp-783A{?hJa?66kaZNZG<&6Us=rNMKEX6>2XIku(`tqLb)~q1orf;pkaK_dv8Th)D0;ot)mdl-<}%5d}9EGYS#n!}yqBRQTrXO+#@ZN(%t+*(nfKA)5i-pSOto?c<gwO~VPbf=h1xlpApV;+2$U0pHt;gNS#HN+OrR4tXN?EV1M!am}jPXVEu}FacF1wG2|o?&EB^v#DK?cO_s!>=(EY3KgFGv@4E*j#1mMeLcf_VpRe)2=TuxFQO(5EG{N>wq`f7vUgR&ngkQ$N>d907#keAg)pd^B^gvA1uCe5ZiLb?5;*l6QY*k_ZcW{S#7r~*xZa+cudP(BVUrvxwEyG`LQ*=bLYlN{Hqj)}gi`8Hg#$*P4WyKVjL(zoBd|E<bIW^LGrtnpj$jN35t;wzm|h91gO2dC<&3oGi%uGCasVw*&T(=)JR}~<38QUH={|WlfnF=;-lA<_Iw#^2_Gi(6T*5sBm>R$H(3qlCwmh&~3kSn8n?5YlVB5R=8Sc2b7fElcfc1A;rPEoYy6*G_@y@feJ7n}N*<R+Z>hdqMs`8y;_tn@7*ncVx=9cMNYGLHy5;{Ar@Niv_h{@#`DFy7;RaWE_7#<hLV5lda+44=n!c8dwp6pH|tvinUbQxJS(Fsx56ht~Td-v_P3B+<)0bLt(^NT=xnWP7+@YSTtQxxv@QsPID3BUw)a*RzXu^P}D8=G6O9Ja}Lz37YuSWD6Fw}~OtGg4(+rk*Y3N60!yT-%UP4}EwIn280@$H^%jMzyTc{|q0M8Pfo)tjs2p(D7td3ceyj7wznu0{N{*dsWt&TZ*bDe@``xVpUnyDuT>;k#0s6n(ptG<<{IJBvlzF@<B|G(c)yw311+4v0OI^PxKN6bf>S1y8}1GbO_^|ME|~Y00C98+$R&D6SdQlA`6pQEITVc@z2LyGXTfnRj=_q^_I|aCl?%~o;6r=40{-XUd7Oq@~83NZC?!nErn&+2CkA~P>WrLqd*P?q_|Uu^^^i!o@;OJq;z=7)S;DRF`(`5r7!@L5^gXyY!P>$Sb?dzk>3qwh=Cq4z`aQ3yvO}wyNxC((CiZ9*aedkXLdvms0;V9VI8x=DwvH>`XYuiBZj5H$qHx&+70E0pn*$Q7ZtHfGe~pf3_vBJHxVk}fEXYtnA&&buQZ}Cp2qft6vc@`NRPh8)w<1F?a=wD!+V!OYA%=0aiR%PhkWRk<x%7bOCoM#?K0y^j9wA}65+jGAjJ9Xp68&v`4aiqc2k&2fdNNKQwvI!N+`{_H&#WI?mhybEhfPrLu8t9l85hoz@$fgi!Fx&Cd?P*+1CMlLs9LDqf*QUpsD<3zH^NT<tI@anU2AX0sk9pp87He{EdLH8|MOTC^mj2z~8|3>PRp;&olmlhyBH2t3ziF5blNNk(`XH?SnwU;V_^d_!5pd4IC5iEbUPRP(c*&>E7m?1nzRr0qg93kyJas2n_cn^5&T0;JTXj2;4GbR07SGBJ;%{;XVWH4$}V=pg^O_`9z!9^aoL*E~5v=WYCHN8S^?8<`_^ccLN--AvObdJ3Ph!bh1;`=ZB*Eg`gX^YFVWWY`hPP!qA+1LP+Q8L3PrpfPzxabM6kvv>$rW!C_xix?nw+(xe_;@u^Ts%EZKq`Q;=`UI&KO)L@6xvDq(|eRKLD&FrreqSW1`Ffb+rCkwa<Sq{3JWJ$0sSS#B>*_@n)6e<lO_yR|ZeUh2b13-V(VC<a+BN#IV-<O$J<5vRgBVP65WID?<&MqmW0c{DIf`;qb8H#bj-w_!fc^d6DQ9WWAZ6p;<Ejh15Ur<e%Y<g*d8>`Sv!AECKSF;dgEuIZKO7Co_&P<0Ork*AULR^~jv-GwdQ$7=LZB-+H@-X{^XOmJ3*WHmf4S|ECkZCt8;#XW$uX1ddTWQ01K_MuwhA&7^jWs~aE<Tw{$B_V!4?`00kLrvfHL|9w(v0}P0moVf(cNzq(JVlgX8sOyp{*oxWu7>cKoBWdo#<)lI$%JLGk4fnq}cBWEPy24A{062*q4$pRu@_%1Z7Uv_keVVE>=%)o}8Z)SZfLlQmto+6jL-69ISQJgc9!bpt3TlV1ix6XlR<}V%gmhEQQkq>((bb>qfItrRaBn)+V?omJ)*QK&1#eJic<o%mtAYUAfAwI+-@xrHS?`n(ePlpiq|9CG<in8K8qqDG__o-@6J@Bhj=hP4m_BG0L_KQE~ZWT%5XGxb*#ZyWNkLi+eh`PySx?J^Kn<LpWjcFArV2A@s0U1__fm6z2Q8a`L<k!}8@f9<i#e^R)CmeX<x#U=**Z)LkK5F{UA<PHUVW6kS%`z`70^bl51S-UUYs)ETl97J|>yYMnx*DBBalK9n@JdL4@+8u_$u6OhgoZb~cq_LRK{2QTpovU>((2Z|+FYO#8%;=C|VHtDH)(_%>$mCD4~<}xLi9}n06Vl_4i2VezrcZ=8jXdTZmrYnytpHF1wL=-k6%#EKdxp=K$r;197`|8LsN>@faL}a}{A(4wcb)!7ds$r_&(lJBlBj*KC{t3+9s1TVfWj!JU3*#j4bV1&<XC{X_OGBoLl9wIeM=aB(%$vo!u}XCdL0A_3Y5^P0>Qy&X66GO?^_WvBH~2I<PN7=U)TjlVJOr#Lm1$WxXb&vX{d|Ba6MC2GQ`w-ppTL2e?w<k0Hyw=V=C{VU$}<crr6x_nl_lIY6M?!o4{KZDVX?}b7hzs)FTuR3U}mdmSLKAs(KM{B?iXibHD;(qxYF6Yx^Ij#u!f^l6Y#L8SRI<T17{WBhWbW>V@(UfDji<JyR*c1gHC3Fy3*tnabHx^B%)cKrx`L1_zRa)W`lM6dh)erB+7%A_(-{~urQpUc`YtAe^*9fOcjYsiNu_aKuHniL|Alyl^H|$qQ&E_<*0KT*o<w|04OMzmy^`;O>f5h-HQqF31<=w%TusfwQlE8*(~@9oF^SY#fvLaLEno>()f`$<oFYsyNi9Toq4Z#rz;Ds`5X;e%?Q>US5Q)^i-@?Hmta-ko@JV_%CHJmnPA_b1Zqjd)6U4wgmn6tAAl)rq9(7RLe&I@Aj||ZX3h=npMm#O(1zN@U{z_#+G=N+@+3%F0{syWu~HqsdGoCmYNT9Jr9@#RuFubWZsOi7r|zyN!RE6OxsA9cQ@gBIHWNj;$-u+SGi#Rh7-l8V5J7}1punMIGrs&+)61mf*sB!;vW?Dm0@?p8q1(P(2Ghg<Mw{oiEpswUHi4&0S5Yx^_+*h*;2gD>@fe=z0GijU70KFFKMh~ki^{g}V|F0*lNh4`t?VFCq0~|qA3|V@D7m^Q!_O$<CsRM5n+mpN#>Bx@KhX)|aCy*$v{KYe#b0^S2-Wv*GNx;sJdgQVt3^^Mh2~MCSjn8FsjSRiYBQVLq(F=f8E?EetEcS_fi93+2kjlUd+iN!y}o#*^vP&Vvr@t?lXO<y@2Pj!<p(U5l2YdBkO57=vFf`~MiC^QJ#A&rEF4}`Rp@C6t)MV*$G)&Bt;8@k*qiDtPC%W?3F1Zk9CF1XC2s7LttmRee5DM}>ZTUklr|TRlBs(tBz37u1x&i%R<pAbLfa|RbYZt8G=(79PDhGkfCN<1-1fBie0POMPmagi=@pM(6sSWkC2xkFWuEQtTm@}4yasrBUxs_PX>srTytF?1?l??eg<;x!TJ01;Z%q{sQ$9~y42?1hM@auy7+Tfr)dKMW05fg^7G;gw+FBORfVvaw6A=?)P!@5e_N%%5hT;jp{qwSFaszc06=>Y%0l0!J(q!Y;z3L1rNn*AwO){aK^ofWyB;b2vzbFi-ozm8jS1SV133Li`4P%=dj81x3u-v4f)!R%~3$ehRDdi|os|$(0%SF6!QPO2y7$4xV;5(-@nmVzfFQAQ~lBkDqaC9KajKXv1L=~W;X~prO7EzAVUNCRa!Asb|#!4iWC~>qFBp0aZp$`HTS7crq4k)_t^F7vv=ZLa=siuib`#Bk4U|bx<)ZUJBfR!WB<FJn=Hscb1VBYv9tpc2Knu02QNC8}19s#(0`DM;iHP8}AR^I))-4HoMUU`|Hji6m{`K93wa@}n!dyCfnFr)UzRTwYqrzcTlA{GjmVim_Q45AC>>$02Y5Q{iSsn`U%$hEABXcnf4BcTCjB+7Dek+t_FamR*UoJAMg;;qH6<;9AeEz@XcR*SRZjK$jy4bZMa+O|pSLUU*3xXY0ONlntdojlBGftS~g>y{l|T~RhGVp}COMaEAQ%aA8&Mu5QlAaJ2CxaI{FF*QH=+8RgWqpYf0;l{jn1y2hw8M9r)bX>|j%zO9KgJAkD3=8{f2#Hoz5GpDP+#&dF`a(onBE~~UN_^!8yH#o~nRtO+`;;#$L(!`Q8FiT!Y@gN8M2lLYiZSyj(d8;WWO1Q71;f&;Uc)I|u~*Id2iAqfQ;I4I2e+B)wzmE#$<#~NuAi&7xacpQ$SegF_e*}D6nJ!N7jm0(gz{iE+&N*;If+hqn4ttnK&~<SQE=MW`3b9CJKI&N1vjy-KqhykQTM(!1eG$==}Cn|`Qv!$7!_lkQ|<&klvEX<LGlm!zJ{Q(TYpxNmRH<&mDmOt=;JAn*OgN14(vlG?DjZeFTw40CjiV$M!!le=RrDN7$F}Sj(WMNLaUI*uQ3ezWgte0CT3?_x1MWEhz|kX_1VIVuy{fa!H*0(!OkG&G)5CE%o&Z_PhF;5E!lW0sWXTPWG2GUB-~-eQvD(mS>ZRGCSiciKGbM4><CVBL3)>jAaDA~$e<*oSj9zJmzAyD5X+qIp%zp@pk!YW!#0F8W+^sRP2sFWVL<uFJ1OT(`a+E?5XZ!TD&H_=^|ww^`w-uav0n=jqf%{!bWqo1CDoRw<VXW8D*x;$qD2|kHJl1Q&dlnF7>s-fTsDMs2}QDiOG=PyCv(G^blo8-(BQy{bSATk0YB!uaxMu!i=T14G^pI*R_&+DrujlbSbj?Qku|f($N<K%9my0e5~oOpE_N>_<XU%uMv|rDDBCf(rznr=@dy!~P%WE6P|AYxMg^&qG0=XM4+pID<EjA}XL-nGk&oU%qw#zXbln$FmV)Bt#t2@Jy;V5v++fT?os>YucVO>)Eucrr4wMPv+0BIz#^c1Jv^E)qlT694;aQ^Q(kJv?7<I&FxKq)@BRuYVYB!N`x*CZDc3)(gjjWRE<YsvA<Mhkvz9|5cxw7d~kD-#5M{-0Qch4&IFvlkY<~GF~w+iv!G!e%U1vDCph#tA9V2eid%Jx!4S>0l>g4OC(j&PkAW>5cz+_Wv)tEi=Z-G(X^3n`{~7eth)O<`~2p?Y1KoEbXG-39>UTIGOO!+DS{S`bl_wu@3kWamr=yQEB7LxI&+$MKKdwKaak?$Y$poOzyu8RYB%13E0>n<sm*`Y|O*HLVZP&tRlN0i^%{%{ME9xD69`Q)3U`wFUJkd5V@C*3srt7?q$~Qo@d-uT%)6Rj@S!NFA<VzVUgsBdu)GVQx`&B%5Z`JOF`Mm9iw<zcql%Od6b|`(|J_+73|H)4!+zu5IODzBK2N)wBhfAj-Hm?*X<R>-pv(D`hfRRCN{{4W0-pqv6&H;#ojlL3f$+AW<L=Y`*%U6T7Wep`K=S(?5F0CQqWDo`zrBw8$lj@RWJ&*R-N|_Nmk}!Nas=QmBt2X^zL`j0WQgI{FQ=99;&Sl|WsAR>#m9g$|>yg_jZ-bFgsxNwQsEvK0S9d4>+RQE63n<nk=2IjN*PjJH^+BtQkfvh3x{kQKFK#KEKW1xs2$;y4ncT8G?aFRW4{bL~~XREijHP%9V(N<9g_JR&-rKi1fPwS;Hp03i@3KU;45@Gi8nG%q&Rm!wQJK?rOtTji)-k5o1<nAVgR8U2ij`Oe_BxpqjG=viR`@%c=5gei+YAh%md;xqTeNhtMu-OU{Zi;v6oamt(!Ee7Wfo%uSQL{cj35))SEk`gZ=9z25C!~9^k1Q@N|VpOYKr4_lU)}n`O=`pD8azqL?v&F2H^x{h03~P3W1-SgEgLh6>Wd%hZ249y*p)FaKy^1d+pz1NN$gR8dI=UJN)m(WGi~=s2s8&{>{F`17-jVzqQG1HHo-_%4Io||uyrWe!=#9p10--H#*9c4nACN?*QU2n^a>{NCG)b#cwNQ=*RzJ8k&+yU-w?yaH@sDvdTp5-*KxK4q9nATR(vW`jV6G9_$><(k=b3yUk_?y8b2K1MCI180qAvl-KCG2Ud?pdd)rB@1#Vsr%WJ&jNPYyknStRK2Y3Y>96t=AkLRu0d?W}A6jBmjpoTvzvT8FV1*q}yTTN_)oYAB1|37X)@iquV@-qjpum7%R%)(lIm72Ra}Dv<Q-0#p@idO-1LoMhALJq!RSN)=1agA2psTS0VukQP--Gjrdl3`JHxiPx>-_%Y!{10&i~Ie7|*SvQ~BxMkTvA439%juq<}xkroON~<O+sX`=?b3+(*C^#!f_u|-)Wy4tZuU=^(O;sk?0!)jBH;7Qt*!neAogqgyNew<fLvtcu2_G4rpUxrKeZW^4Tq|Kffu^s^#zqNVGGomO4U_b3BPuWeOvVe&2ukObtz5ZbQYfZ~PqOP7-oqr2Kr_?W6|qF?{KVtO*#xO+NN4iag;50F4(hXcRY^}!WLD#T@k<vcdK`qUlj7~x&z@wn&R_e5YG&W2(6CmMyiA4cwe_$!iidexIW7;g&tn_M%Z%wk)Bkj55Hsxp0zNd|$rw-~M5f%NBOAdo5L0-unt@rwbTfmZW}n(soS75}5%-vGjx`En;(V`-9SpK5$(BZzo)&|1TyM1ifI*@P!X%}K)(E(w8+$DS8stm!@;AtBO8|=wQi~#2I58S}%~&;(<Wa3zUl~Y}=Ohyu!sgKwrE;?PHz|Kih><Am=HT4vZADd<0L7${dc|E{kBf2FPZnDtVNCM{XlhbpsRn<%#^$9CUo`xcp1D3T{Q~K2)l7-=C}i>2Z<TCd6v)ZvY}<|!RHWw^)avW36%-nY+R=Hb_7)~vI^8s2j|-^tHCF@-Ou<HxcFH*k0J~i)ENUecYzoL3z_;Y`rn$#vnJam^zUnVob|$IQMQczh+_#zK1ITI~stoEX5r%^<tC9uUt%X^_J)sO8m+<seh-qkOy(A^oYG;!a5k8e5QqWB$H~JB+dl_k$mHKX6kAqjWVeHDpuay&XQ-Q?n<nIYG`G1NhY2|`XO5Z#qQ8JO+TMOG&a7U!yDv-xPWXZMp(Z36Zr1Hf}DVU~qq>~7-@6jkZ$Vg3*x`<?r@kO>}gGni2$90v2O{K`2ejd0}ep^|GW+~QoiQvmrtS8c+6-bho_Z~8B`#N;abooHSdV($qzPh_HJxUWHUJ80IN#&OmE{m&um=`1t`EmsZG3-4lL)JhswIup5smM|(1J^fp-O^H3qP|)p=dE!bC7>#l$vTydCWuZh9*3&`PEb7+5SFE`JNa=dijY@oXau?_gHsB6k3tn>6rFERz)Dd$tyqoSsb6IC?&OL={BhQW98YD+Y0DXwge{&QM2SjX(O;(k?zUWsxmH`}+znYudnW}KFS6&E@TEESENDSXzBt8E98PP<@9k;F5R!pisgi#x@_7?bo-=fONnh4G8uui!pJxPqvC|x~l`j=8k<CJ#$4Yz-aUg1k`19mf&k23oGJUa7EVF<VZWB?jwPeQaC^DlwtgAJ!>m1MN*>>CZDtwr;3%>cXn{Ir9q5+#$l?bJe$<A|BePG7al6c`}z0#nsESb|d9Ad8ZK9k>{_*(=l?c&1bmFw03ZPX(G*2+vJp_k1q;BHm(qbOjweB3aFuA<~!+-Cw7=R#IihJJKaR#ra&(cb7(GU0ZG2Z6Nsgm_5HL1qP|QUQh<Z;hSKU40MccX8l}&?7vf7Ac=hFa7~IJq>>E8>NntRWVRi&{eQBbp>k)1rfPd-6(|d{H#S<u3AO&)CFjr%=InYBdDNj_he2}f(<4JFVFZ<^^64Xm8#}*wu!@;y+93KrOM)FS__Vp73>*e25^Br2OUo#B_k#zLkX((0Z2o<=^@aZ9vSQ+FYJ?*=27v;G)c33J|u}Fv<9?Y)udK)is&^ER(Ntjsd7LJzpbFKL~_<o4XUW3dJALgW)z|`ER#6KYZX?cChC!t>`8HjS1ft^*z+t?`-LulLy-j<pgCn{(>}UVnmAp}E3u7uk55P8i)XE{y{!RpW~uGPH=Lug9bHS?uFbmw#WhDqq(U}IV#g1(%Amx5!qIHlEElhY-F0tG%C=2xELFIvmLnJTaY|UM5Hv;<uC87;t=U~el+8;`Q*N3|G;FGY*4D6J6iCSKCrCwOJ@0KoIQ3lVAM058gfHLAEX-X35B`_&twz;rY+0l<M(7$yPRriQYUQ(iVg027fXVu$N{u$RG%<8?#lU4LKDcIl4%g9m*cORsb=_f*zhzM+X|rE+D*c&&4mxu@2@)bCQ`oP-Atf+6Iu{#+CrOb`w52wc!cYY{Qa;em1wjRQO7OX^XBC;V3RN!v6v}Y%($V7@GQ}5)dF*s&Qmlg4^XBo@*ePl%7Ye;6x2GHBBA_S0Q!=ZV#=QfdC((i6$;$YE7bSx+#C1eV(z~LjvT|F1fjmK{%*-|IPFVB48rY;;p-Ns$1EiNHv~8?ovr8-KR14V_wF#XNWXfU_>{PQDeUjh`F*UjnZXII806%kd`snKH!}W=>v<kNp0h9t<dzx|A7tk9!p2{)TIa-9D97A@zl86;TLQ~`u#aj$!u9jY^@KQ{Q%kE}F{tf)cCMxMybgiguT6bo8qDk?2VOZ79C~g$FwLq#mPDa`hu;VKgK3ofJWBA%kJX(kah}w60RoR*7b-X~=Af^t8ox*0M8on%MQ3^R8;En7n<#bJh%%^X%6{OZTgZJcNY4A_)KnE<9Z4-i0HF1OYL04V960T1R0vi-Ul%9ib@VjqrD;x**+P#4y<eAV)OH;9ugkx&vh1q&DWbVki_)1jw1O<<%UrQkf$TjCzHUH~k76sMnx@XIQDa(1iN#j8(l*xwA0_Tk25DyJA<5yh4vhoC2Ik%o~dLro`p(SPPr#J+8l5ywWymUB9FA5bVUX{t|yS%h5XY-kyF2W8#Os%tgsklRIK2uQZ`Z8*6Lp)`>?gU+I!D>R-=wwfI0j>F2eNFzbx3f{HkM0n<NST(+3fiMOF=**?YOC8AK^5}tGn_<uK;fas$!X(LH1DS?*6NB@m16OJ-B?al<mm4Te6kn>j<#${Cu;&hD9UJ)(a5D$TX<?&^E?vm);Pr|s!)!A!2En}-+wK^k_G639G?{BED`cS!{Ba2b`5J-BR4=&V%1EY?W{u47$^8O6MAcSH>|HrK*q0e>B&<>8bOMtSWUK9N>rxs0`O?y3+mZS5JTSops9pQ+pOTy>XtXcXmOkz8`Wpxa3VPmX+?hJthq?8FMC*^tEToZ?H>YY&?L?!oAgYc8c9BYE}cH4{boJ;TKLfDWV=MiI(^OowHK}f6SJ3AHa7bps;-C<70=(wzvCyL{ui0x;xG')))
_PLAN_IMPL=make_agent({0:_SCHEDULE},**{'hand_align': True, 'weed_repair': True, 'sell_lead': False, 'budget_guard': False, 'room_guard': False, 'clamp_sells': False, 'dead_stock': False, 'terminal_liquidation': True, 'front_run': False})
def standalone_plan_agent(observation,configuration=None):
    return _PLAN_IMPL(observation,configuration)
standalone_plan_agent.telemetry=_PLAN_IMPL.chassis.diagnostics
agent=standalone_plan_agent
kaggle_submission_agent=standalone_plan_agent
