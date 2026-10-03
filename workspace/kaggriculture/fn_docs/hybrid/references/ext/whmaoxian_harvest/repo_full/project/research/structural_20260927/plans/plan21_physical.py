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
_SCHEDULE=json.loads(zlib.decompress(base64.b85decode('c-qxnO>bODa{Mnk^DtyL_2HXV(>o)qW++IM8|#IzSiox-FxH2)Z-)Q7xx;4n>z9!cky+K0e43sn#rLWzt12@xGV)LV^WxwB^7p^}_3tnK=}#{{zWx09#n-DB|NfW%{MY|__~PN?-~RIV|M=^FKYaevi=W?r+CBW#`|!IjfBf^?U*G@o_QQ*-7w_)&FRre`*Pnmh?LIDk@bS~#k6+&1Km26>^X~1#f8Tul`oCAp7yNwp<^Jd88=k&;c>DM7{_y4F>hJz~_i6p()7!*<u^jR0*~ec#yxh&%Yn+~Q`n2DDzK36(&+F&ihYzPed%Yg>kDu;7o(~!P-P5PveR==k$3H);<o%b!Qp9IANA~f<+jqNkeoqUrdWF(xpZ?zB1>U_q4CMGBjxm07_(Npa;8AEaKfeFzd^Hb0Iv*CY_to=$zuWzI{<!$oz(^McewhE$&yYF&<4r#Q<55>He%XDv`xU$i*hWvIjL$edKb!y30>@c+c;v75$G1Iu(DB3W?YYVGM>fwNF>By_S#HX=_q$K|IaK)ad^)U=9^O2g^MmP%<BA=S3zK^sXW8cBJH&OTZ?znA#R}A_hC>Z5>T&nS4|KuM>RdG^?Cd07O<i{E53CqCALDZuW*<(D!&Yw}Q|qU}g#p*?@zi+w1CKL5Z)FY-M^`eKp=dc`L5i;f*6DO+GYf{h=rRTy=I5{^&NpqldHRdkTYU6&&t_=->4F9m_ws4{=oqxus%ISNk-*PcPxLBYfb)C&u>KkO!|(1seAvCa|MTy6pYGp(c>gcwvsVvGV03Y#J?+v;=m&ts$nF(*wJoOO(e{Ri%qKeedHOXCeY8Uk+){GwTG5qU;o1O`uRE{8gRawFIeNb6A;<muc;$IU<5@;L&5v(#dL?jl7N#JE0*Ccke1LKF>Q1Z0cwpj_FV`2g8_6$ceB;k}oQ~WJzDZx}Qg_(Fsam|<%DuxA#+(glaYsjvu0-mTmY#LmamR6;9sw-=@vG|We!l<ocK^HGr%!(z@*a+_7+l@O18nEB0Ku>oPUAW9ti!~5SFXDdt!G3xEY6*L6m|5_COuhQ@XBVmdSJQYDbBDJBl3xVIZkDIb#&o5G?%8cR)Lg@pGvNBbdcqTNggu*O1_a3ow?J+X9A4K^C87+jCoM#9PPT(zQ+^2h{egGylG}&;r>7RXhmoF<g|icnBdDD&zN-J#wtsHVRb1aZgImuJ>Kon8K!rHKB^<Ee!AD!r>O7PimXSxeNPU92RQql3-gp{_%z8mO&`&{<|3qddgq_te)?yQtDZZX6;~xqr!Ak`M-b_YF?TIu%)}+=`Y~YogTvOG^I$|^GFMZ4mi`+-vs<A@nzZ3)WgY6)=Pg^G)fwFN&^ew#=D+av@w6B`)hUqeJCGv|Y7^#SUg^g2N(&KCZl*)7Cj)KJe(>Rt=x|9lQNfea9bvG@$*7M0$mx2jd2$5!i_XE)Aed+6IdXAU!6AQi8kPsK8l(Aq0k}s?i5v)d$Wb6Yo<zstHlUQm<N%s>9LM8Ymr#1(TGyx{%QdM$-EleA=%61lmL28z7SVCn=SXm=;kKhFN(WEH-b{@W2dA;;XvJ%Mjg;nKdUM>=W9dX397v(a|LSkA{d?@G#83mSX3rO1yYe)&HqFL;wuh9$Pm`YtOa#Ff!i%mxHjOEkuHE`QO4ovzMIXEeZoouTbI^aBfn7#l=rYN5g5M41SV52oeK+PvNjJ9cX~l_+SWwQBsyXHnodJ_ubdu|yVw&x#Pag0fPqRm2*^USKG<ncZSkLHGsEJVP6EC42VR<enXM<Q%KM&fD$fkty8;1lsYmRqL1!OFGg4nGI$xG}W&Uy*yj&_m>42uABY=d-kY#^YHkILhW8ZwSo3^ByxZyKBOYRIdSD=E$vd3I6<5*-bd{6+*8*MW5paAj~lz$pjG2*)W7NM&Iktqp41=bnC-4kj4i1>8%3WDVaU$|s5*-nbve?#Ed3vz*cfT6tL2hXdlr7kVKzI@NGH3C}NrZ<-GWhazdmd2V&jPWAMGMMPA4o$x8~tOM%-3W$R9=igQEJpj!)E?7E#bFkcHP4@cnct1|enxru}bcd*sPKG&hpV-5>E~V5AcxcMtn|Svlgld{|&c*})v9905@O_F-wS3f=%5qbW1*2xiiJ*W_*ir(BmbQT(Lo@RRJnNoYrJ^N2(;ZBqtDdm>yQke|RR(PGFORM;OM4f+OK`DDe9zQM;Lb0ct9bEQ<VTUAGHSo98*+=!iQ`pxN|lPsle#WMVdC!Y;Xf~nPUgas4B5xy80dY`Ds4N<nErHk_jy+Y_o5?<cy)NDk1Mx)FbE~&{XPfECKuQ$cdwiQKvuQwrH6E7Kx#0d$DHK5yD-V#{ZH=HAu|F|ms)gaJx}@0<#(KUM)}o4`SOk4D<BIAR)m)5I3{Lp`>vIFo8nBv0R0)bpu?Oeu+pnNphjiv@S0G{oO3oJvuY#A6+qX@YO?H9*CmcKQdLDN<<@2fW~Q);qo-MX^+Il9$o@vJb2jPVAOrgc!8`*m>t_eN9lvn*Bc2V06H_8{vmcD`!S}b!v+Z;d;U%gL7zUDWj771ik$!1yiq>Gt$5wGbaYh~wmP;>5yeH5LQ{N><_Cz~@ugRvzD`V^{@av9Z&KSn0lVwsbr;J_>N=tq_Ws@2{F@mGS`o9QePkjfkbhlOQ>0LkF7w4%6nSUhEPnld^5Ht1D2nz{D{0o3zL87lh#c%|8Ahc+fpv<hUcES!=6|BirGXR=6ai?%TPi_v!lyK<B5yPLNAaZr$G>U=Okz{8<fyxP@`hZm8Fqd>dCMg!Cuqxi6%0(DoM>rX&+7>9-1bt+M<deooyl{qxcgR%0&qww~hnVpN3`?@Iu&E0`=_r->uO)1eg10mpva31LGGVYMX!wcv7*qUNOuZqji}i0cr5r2?$9Ys;o{`<@sIXa%O_JP&iHxaV3akKn;`*y+3VEv0(3_g_fbi*@ENwxQxjP1!2nR_yrWk#dNiIkawn4>w-A|T-!^BL#IIi0-??3!uk=WByAMw8E&4O13VTqtj&dHa?Ko(kf7Rlxg9AiRz^Ih^bU)LA~ZN_b~LX?l-7?#N}V0BrP=#-Sm_iDGI?viHjfk~s>jhbdi7#>rFMY43%E1ezpDE10?t-`dfgS>J+!&jOC(~bNn#w=Qe_!H!B!0eF>35D}LPHOp`^Tr;hx1bjScV$^QvX{lqUYu1h!3djcK{A02D&bTyVo$z_Xs^X2MAFkiCn(mj$VDt?6=1?`NG*w<N(0u^l~3jwQ-0#)IF4y##Rf85Ljd{Pqz?u=oQ8y~8{%aM3@(+_wUwYN%|*agiykSpiF8XpOA`{B@g#>0Z(~9-OU1lxJSUx`tLa69HR#9%mtYB4QF;8PQPv=Ds@n-r#tb|lhXJ-Sut0lhB*A+9g8=}X9!m2VG2Y}!!AoU?!C8b}_l!}Wa$B1<xIz$Kvz;O2MJUi)7P-5|P}2hf#!&6Qq0#j*c|)4>0k|CPurOSu>X+Jy+8K5s#ru~L2Y<7jjqn@CnJfT`VlE8Q((`7l%&qOHyE4IMPY0!|FV1)nSxY%sR(b}l6TMt&M1z6rIAT?Fc+3N}Rp*mVKz(QIjNCD8auNW6^0J{?^l1KU`eV_L6{s`lY{>{Q#=ulPm{z&EHgb4v0;=F2c;Mv6{{knI6#l*hGpyB^2yN|JTxJhYT>i~-L}LaB0kAk*agedU08huo@Z0-+m+M?%Y>o33)~?muGl?y}8UWW8MAYj+c-&BKPa~B)RPP@{XTYUUSE|U*i-4eM2N8-CTdY>1j}MmyZ=*(8Cm-e!I*^0&!!%T+)iuQGywu^eS8)$Y^HGG1fq~Tp{$rR9VJ4<8Wyt;~L@?!*1Wcr;0nb=y#ka=V3H10m;|Mr6P%1lZ9x!xppoxJxhM2kpQ?9&nhJt!!b5XG(E91IMKe@iH@lQb6fSblr%bWJ}!UKLxQY;BKi#a$kQ__LoRFsN*z61R#GZEmiW|zCkw~3}tb4TD^(Wgk8%Dg))2}kOCRn<$%crmPPxJw<hI>W}UCsnNR<HDN|agNbOm+SFg--K<qY3obLk}Yt4vg)O(%bYB&Q@#rQ2EWU!$?V_aaYhuCRJkUjYol%oW&tM}Na&<hOWUNHYJA7mVe5>|FOuF$6vs^Rfg`+jA8slJy&i_y6^@JT0}F`gCiM=UujahO2Z5OZcBl4eB=>i}yuH8c8f%<trBM<OmZx7lya{L3w0p()mbWhg&8)XMfZt~HeXkhZalgATG}v#ls9pK8T&{iw+Q^%uJG7ydp+Xlr`CW1{k$`H`Z18iwqMptMlAI=IZi8*!tA7&Qqx^5p#n}><^O=x0=%Dn!yw%lw=nxVp-N5-o!A4eYY_%z?lmbm@8Xn8a!7<OzBdsdh6O@nFFql<J^H5b7`t3lmX-V+|RPB?~8&!n_X-MTfq)rgWZh;{vFaU;RrB*>0)Z2Z&pIFnvx;Lq@GGc^R<S^vwp%O_F6?xZTo+yR1of@jHwgK?5N$OcehFL~_YF3)cI(R6&3EY%lo0PP46`g2nq+NnLTP$wUUyRzapX>nkth;~0<6-HOGLi&ILsKpu-DSfr3KJv*h)g*}En_LC=%xrag}}Omkh0VX?zE?ga5MBd5-UI5B1=Q8k(6-OWH*bn12IY*%9$ljgl;xkQwQGPq>a0!b@HrFcKTs6?0)*`DR8@pA<-L)H#FuH-f0LOyMa-q+L@{GF<IqHyK<jlbyA%<Esbu#jO>Ji9lZV0qRzUN;dH)r<vCq>ygIg<9~=}Sf-WNJUe$xKTCsV!4ah|-L!8%_!fjwEn4JT8aqCtUV?o<1VlypmP`~CGkCc(!TM{jgK-}$Op&u(^8geZ;ct-C0Vmxm)pg9}dO;ezS_%(KXE{LmZ;E0qc**6xEZlQu?2Hyf?k>E(zP~C*0nWzA>&n-%YW_IO(4%6z@EjGxLW6D&lZiW{Mx*gdsOM~WCC>$+1VjspSs#7{7B5sHlu?xuZHZqgGys=Wn1@xZDy&U!#@A&L^0|XMxLsaB;FAgz!zcvd>NCLsG<?BSQc&~xKGoe<?NpzbAw0EG60xTtWC)$hXJ2Rz&3YQBKFF*A8TS6TUTafZDn-*ibC=m!uOlD`|uWs=Z?}U6<lXDC+WhV=Z1OBp8{s|fnTcv+bp&;D!G;H0rt4Wc;6-oe{k&f%gT$jpR;_h8s6X>9D)Nhn{{a`7t$$iVPDIH{byJU3gy@qLSrp1G99`Vf|5}0H2wI%pdq~8pcyRlIA0#e44Xf_-B%dM<!(DDCu8`B}7H0v4f*P59Bm>qj>664*bt44xrz_E#$ah`E#bw?S9SrjX>!5_ht=Bk>8uf>`vlGfQ2a`L6tJBhUwYl(3vc<J}LK8e};ZK20ZR_)}|#Jw8xqRC477Z3lf2&qJNLrsoQbPY}g%c&Kvy3yF@w~Kn2jyPDu%Xnm;yd1YvF6W@v)HUYy$cR^sJY;=oH<FH5@4j)PJZ4pKXW}<za+8eaxA59qojW@1)0_nmJGNdO_1ng{ZP!L+xi!?T)ToMcLOISjIEw0Dt%vAsbVT~C@`xOKXD-Wzl@%%thW$=!l+;PNqS8OZmCnDX(KJT}p<zyHJya4l_P|O*#zx?O-VVlGY4c@G$^pj?+Po7`7nY#)9z6)`fXw<X!i;mhG(~(G5UbYk#LnosZSnVHhqs<G5CBFf)DwRz9a$~0Br&e-r8qAUD3)EHx_lQ4E_v04OE|CMNP+>-Nkv3Ph({NhFGkN4+?L3Vie*R+JQm7skpa6xL<q{j19rw%@i8Xs#S}em?ng6XZUdIF2_|J_O2ajH^VMJQ23x~(dJSrU(HOQ+<iR2Rf+5z^@bJF&R1PF3{CsI&ef68TqVu9a4=B(`NM<zac;?{b90BxLT43^LQp+MJ(Qk9v#DSXfLIojdbHm%%A(sg-mFSc}sg(!*4JUXNF~ZkhoBd2{)gTJeaVi&MnirU&nF|H~a;RXUuZNLT;+Rm4m&vV>GelPsE1_(JfKDDAr14H*_W;L+h236SohmaLmAo@diqZq*sX;&WQ6;L{3Ap~UdX#z@WTSQ~W2mNFQAM0>%8-v<8u<3B4-?2B$`eM(+AR&&%PfI{m$REJ9d+eD|Ge9Mv_<Ud(k92hzx;B!hOZRP5U11QVu<lxjaP$ueVe2o1*heuts1jwHsJ`j!>hWLM4X9JsfGHw*Z(T&1D;;5+gC~jaF1f{52kqkC9qk#APtk!A$?@K4C=FV!f#sd%e|1G<&5ZhRj8SeJ+dnuEE-vCU}BcO+UZb72ikabL{XB+ql*(AMbhpx+v8y5g^iQsQDof=*c>N$p!YwaO<5$Phy|zRDn@xo4E*C65;kIO2=Qn{T|+utlNB2WoEDhXA&m)gQm`qcjIhLVMBoq9snC`djY*1vQ%Uez0W6@(CNwl<(PnwV4Q^y|vRgrNr<7E^dhqIb+VMoG`9xZQWb&ll2|UwusY_uPzFK@dA2f6ERi$sELX)@%o@2u3teDu~(b6LF@JWn)AC3qIR^yFWWZ9I?PO`GxwX)H)YKnvbwcmNQ=U(Tfd?r$PMM`wp^h-s~U!~S*Nz`dLZT#kSIOi{ufuydFnUKk+_V1zv>E&7-^4$ciS1{Q)A6->U=A1aNNX}73G=JSTEu^WqfsPfz@=Znl_sz4zV)WGKpqC`uST)1B@AKLiU%563#?5)3-U2m1$$|(#tF~;>seln&WU=5KiUmp>wFtuN89)&%w2YQOs^~p--6$0*fo+p;)B_Bn&q%L(r(tR^4A1d+j$e_z<mhhfiiN8ME9@|>mj6D+DV)p%$L)Nk48!&oK`{!&^u4|WKAzNwEZ`v$5e=?W?(2kAxNgy>2A#naM!{s&g-^FDI6`1%(Nzm@3tE!T6Z*$x^5IHZhr-GtW0SYoB?|AdrEYtUOR9qpkvO8hv~m=9*~D@DPr#7bdP*MbZwlRXjH5RD?C(HJzSF^pvL29n^;p-yr}^j0<=3Q+YFd~~>nt*+0v&rI2WnA8r1iZv;TU>JQ9mJe1(f_LUR&oM0>q?MVVVm+sbyuVNl~`rtd0scW$>xC^?I;YP*rb{rq?Y>-U`|jYsyK=JGGC;wcAuG2&{z>Tcq1+u*EU(*%S=CORJ@_J)9s(Zjmg#C?c&CfJ$Cts3ezg{3p8va+(P%ojU<n7lxZ;toTflH;ob!pK}#D-`;%n3p@bFqfl=E6&YNh$xw}W(-^EJU0|1hkvhCg24zZHEtX%D_zUUhLvKpZd$NK)5i=vuU!nd%VOjlMRxRZy>*|P$+v@MiDpcA;9556>ZZVT_S^eDvz0yLnO;&?Wrxmq2Zt_%!vJrHam?qg+bC611E#-3996Q37@`WQDKE375viksFe5z=5SE;;*aty5v0Y*XCp=JG)USIQbI#XB2rdfqu(oqsZ4loPS+%>qy=f;E_nlf?=AjLzn@Z=p~z6l~fv?7SHR8yqH_6S)1U_=gul=wBYP4go~(B9@KlqsePpLjovueAHPZXY7mrq&|G`Lq$>55W;L0YK&67JLz;%;XgLA>`;E1HN4QIYw9mRd*)QOKQ%Q2Lz!na@C6lS$+eFUd^m~>9S6Trejb(>FCky2}N=g80drLy3ASILxQDIcugVorN%|N|N3=8xW0YHF6>O&X!~3gtS1Y9gT?)4^RlAw5u;_H!Qg`%$`VO`)0BkfqDN)&)wnp)%$D*l{X^05p#+^(&*iHwLtP{IQyBRc<DnR1KU(itHJ}QJ)z8(Q=xDIB1A=GW^ShmFa5RLNkcS(+pgisLelu&Lnd7T~%D&h;5$ACMYu0s9aA}-EhH!KG8XY&2)P9DWsT1%R3bYpLMGYOr#(t{MF_rh|>2cO*ba9t~y`XRg+E*B)0P3Oe!`pqjySLa7YTwaTlBTjxV3~v%bV8Uf`FRr1!o&p1caeWH%vwnuIL#Q)SlUV%naYOnm@vEV6i^HrFoLMq6yFhH!l+bHUNa|T1Suz2Xmhl9@K+Pt)RTg|b4WNVTRQyv!y(lYnVR3W9+?kI+prNLBVMts<~9b~S=w>zm4O|OccL#y$1R-Yr-|aoS6G{cIZ=dZ!c|i)Gd@B={EDIN!`G)^hgp16MQ)tlWw6pX0l{nr?$gxYxFZ>=S$wQko>{aQs7Ke=lL%(pZ$U5%$y*Z{d<HUEy=XBxgufH&80DdS-^{VSr9uE>obQ1<CY-kT7u_9mtt%7jB(nHH%U4*;F<UKcoJI!NR1BEn9u}O3Mjt%6$4G4G%B!X`FhS-TnlUn)hDL7(sCo|a7)V&ys;t>(=%9{r#}r<lsxs{il^usbR&1kZOUacb$U*YOWRLZGb+byECN;9wpolfE7-Er$%CDS92mC|7wRdK%y@Gey1oCyIqODYjLj&iy!Lm)*M87DSRgg8KUp0G8sRLr|xLq^5h%@Oc@c0eyL$FdVi_ErfxnntiV$(Uux575<TRzT!^ROcUQ)Z}6`hRmNa61P)-lx1h1AM+v7s$-@@MJ;bZxQDJZb`2h+ANHW(h}JqXevNg8W$SISv)a{@F9ef`~_A%d7Am%hr3_F^*4rjeJ5<N%{Uuu2B7tQ(8H8BinI*|MZ1DrnP^LPaSB<X$R6CBlUuY$ib7O3p+1={ebQ{z9_N|iCKZ0gl(?*-gzK`zcxZ1?zq?(#T5z@yIq*cX2W*_l*dwI|rz)UfGX>evCYiA=NLt3NPE9$+q#O5^{9uicid!oy*p^W77^hGOx;v%61125uDRdN^6w0ACJCik=cjVP;7%@cA;AvWY9;RVVLo_YAj#kxdrM0k;Lbp4$BMhpv9HutZ!ImjZH=|NG!)~Z7M2?%Ywac#RT7c#%57_<Lsr7WDiScHI0)rubkJWfY^`!|d9SWsnpf_Q1U3mqWN)I3n!Y@f-@?S4j1{kN_rK&~^je;Xc0SG=O7j*Jgu^K2_4JnAC6%jeDolx|I&%$<5mB_FpdcED<eK_yQazK~1bBhp{0)0<3=I#G)tuB;{Xz=vMaHYWz^sIr;6Ch=P0aZn=M>D&AT|o&Q`jqji<Ha(U;#S${o-fVJg~q;#Mi=+TWSDyag|3>a4=+Z-TVD#JHUTHQktCy3F@gxSnhFL*)#+^_Rg$!qVke8`jG=xBgfiJvrnIlqRlsI{__f4)uaKD5Jh;|hgO)@=Y3=N0AwpLsegKq$u)K&mMbyHM^5&63#ld>bI{F2H_3-+7V$4wSDqKaDN^!orAl8|<?l|L3pc-TGuJuFWS;gjdwC_U#A~3kq$q`IJ34)hhSIbiN#RLPoY$(>!R+G{I(xjp$1LrAf!!Jj9s)W93mf0QGPf^uoG$G`r1wBiI3_VW?LZqAu#jR=~0rQ}LuA9^_Yas}%Dv6~eGJct8G!3=Q#2$jp=+nSvdfZDqC@4N2z$(~_B0^gk_GJ_*=Cm!cJey&v)f48GY4>lx5&f!1#X@(NC$aM!gsRA_^4lO{|2%@?R_ntaRf_YcCbm87L|-$wRp4y{oeJHqDvuiRvPo4sHByydi`s%FD@a!zFKX5GFv6Qj=$gR2VybL=(`~7sRBK$Ugeye|NmRsUH3)ta@4~JiSW*lgPYPU-3hDb291f#*^A)HRYFW_4bFv_^Bf3qUpKfF#$}(fTzb+Thp(q+F!X*RPju0c_wxn>TiluWcpL27k>oKJ?f}=Gu>rf-yc&4ldZD`vU`Cx@Ug+L^FEkk5UCxd@L31V9SGi>|en{G?#MXolx9^qmWNG8#t<A;c<_OnUTvq~EYZA7J~_5{j5%e;p<vd)&d6dH@ClHK0wW@Bt3|9}#BQSYqPC}wP>3RPX16#ck(RzxCs*545;<LcAd#4tx>oGiQF)kNcgq?#vo<}2uJW-90<O<i+gud76ZOREp0Wychux|z^j(r4aURgo-d>Xk_!Rhup)A9j@H{DBo`e;cyfW{m8%nV=i?t@Xi<V>(~;nR;Pz&A*oxl;1>0tj=}g=YQS=uh6V`s&JUiq>&QK!yON*>R=JL5puwVIcBEdkkp9#O@5^IMaMR56Q-pxx=0{LVCo>L3(1S}y{wp!hc&u8>#nSlgC=L^bc&2Y8^`D9<m=aTTS1mO5u#?Pp01g)oQ)3TIRVnE)1!)a79XTrLF~y76d20rz0**378W7js?$-$l#8at^5<^$%Q>)@;MkGZ2HS&TXtnEAwQ`eEiV2(oNuoiOXrON(6(Q2PIZ>Cou7sDJzEcIz=>@#!)cqD~kZp!rQ2CU{*yFefjIK|0!;!wm21;?3E-4M>Z-NXL#RWNs%~W})tm0W0y^`t!DSEY%G*}~^((6d2qE8OpGNw|ilO(WO0Gc}PecB^S?R1ZX9LZ=$P>SA+Og$xX(`<A&E!F(Z4mT0z+OQ;?1MT_n*LOx)yD=zhtg}iBwHl?O?P&$3CkCd{>ZtUV(-1F8UMrPEP5IjIO{ch@ti@z37DT$ng_4qT?MN@0CLbujWAf6(rjuPlo2?$k^CdJ&sxe-De2GBaDo=jyy<x$laoIClL=OOb0z2zUoub7n0;%<8cu0Ox<hxX&9EDsnn%)zob6d&BD-v<hPg2G6vQng|pk7lHhwl-_>L_Dtv`4W4fV*;ba!B<~l3f`u4F!uX@DP3U@)eiaJ_@(=cv?)j&f<>>8b+sUoF%x-DRfTzqN!DtzHS#%IN%Ii+4!SN1z}MvP5{{S)na?Kf>t3Xx+$@@2uPVF!-eLTkrsYd2|5at+PZPP%C1rqI+ZLI*s!AU1qYbOo}W^zYS0CbQ8VjA%35kLka%yA)+Y%NxV+>@ngTS$oWX9U*T_JhhV(Lp5#(4S-%BZ<K^7eAF<CA3TxxrL_aNEx(7s0H^}mI<8NNE7j{#Pp0?r|SNjwI-s6MCf8_>TLovK-@b#ZnW3y70^>ZO=r(F?G7gH+f`7GuPn*!7yDCBf1t5<aV!Ws*ugQLC0b65}{JVPj3idj?G`0x(7zJ>wQge84oIjg@N#!FHTct8s)t%)|x|?d<#xs*Uymz|P_ZFh~M31jm+-S#M-P*T}T|ji!_7o1a92F4Y~A0>_H`=l61ut?V2T41!)IXn@JE^ikmy&qC@{j3B1CevClYfa7{GZ?@^oR>-+m!3&~$xggHvF=)>_t6ieOQS{2V3WS}*F<{UWY2AJndDFoO3U6PPK5ESaM%X$b3ybT(Sf+xaUf$1ShJuUU={6Bgpf?(66TL|Ma~{1tz_BX*8#gn#TiH3q771K@&}&?v!V&3_m4B}yRP`#2#U=MkP`>yTxOdfLQUQO)Q|neKzMNK!nANqter8hFMavRL30_e)ERcTf$`G5q6mYI*pmpJ0?F(X=h}4WwmN2zq$1p@QtqKG;OZdnKgySEbmJ(`4!jMjsl%jufm&R=1VnErcYv2xwW!QrO85+$X0u@Qc-(1W>M{SI?eB}B<9HOc)e8w6iHl@hTSOVn&No3anipBfeS$@08)Qk?H<d7^k;WHiI`gubY>~pm`%F*{uQ!j*=+B7i5>kU{(bc`G9eb>r(`wCB@S__Pg28%k>yUA$t14tpK7^8{+M^e!hEE})L%&-KIL;+jK*9Ygafm(;A*eej62|P&y3XAuymXHOYSvsne!Gc7}fYPWz$Gy23uXN*bk+l9r+>EJSNDVI&#|wq%5)42n@6GG*!B8}?4XfRMg|r0&qt|d1RlwJy^4lw*qluBh(r%CBjX{rsH!gQb^mdIDru-C!IBBt4q*-rxs)bc9*yZ_8a0Vev;Y-{Hk`4_O5*BI|DT`SxVEHF~^nf=h`Z;XzsP$Amg{xo*hbO>34irO@(7@!PGwU2a5Fd--6Yz$7kDS&1$yFPdjv~w^7h)~_8<9owb<~Lv7%L42b8FYx4oB4qdxtvv_zvXu)$4dzDBf|)6ZbnNJ6vxI#>xpiHE$KB&^xz|Rj@uitR(=QYfJco=7Vm>h^Qu=#gQnfy{3<wlzQ*EGI$iDZb=K3`qLmMx5_Hem{o4eUb9p?Ih4sJ<%46v(~Y<HVC04-mNllyLcw)5fY^e90b*Pq%3dH?Nd;13CW$4R2`z>SP}2$)1sYR^2@$n8G#u9r4k>pAl+{4nh!h%*B3QV~)`$zTDn+y)8F)vtO~qyisLdH3OhoM%h&9BMWP(+?-{WE5Q!6f_&s_T3ENV>b85jv+GDio>&!`zqKN}L=w+V#u%0a!n6eYd}QvwdCGMfVP>g>ZMaFZCIOBzmIF=aOQa!T=E7RI0=Ey7wPat`sEMoie~r|Y-1Q#(>N18V8=O!i=98za93-FVFIFNd!tz|$GSOJLL=*Qj@HEAx~zPNg~ovmYaD-7Zk$-TipxO`_#DP2~_8=>s=|wlvoJ79z|}otEnbCI39cC0$axtT4b?Lr#0JDhl#G<4EZBwwU-a)g!2!0V<KGOT)SS2^Wk#B+6Q(e%I`w)Ce!C7PDlzBLLxh;9NO_)gQrLxe#Lzq9_Mc#Ch9n60&U-Qw1zfuY)jwg|PfJ)h|K4y7Cd$j!#$F#g`)#6%s}}Q0W*jnHX`E%ES(tVjBiQR4m%IDF!zb|B{vYd)r%JOou|&%@^JS15=q`w{aWAZNS?@Ki8~|Go2jicp+74UxUUK0hNOIB>|x&U;qHK*iLlg%I&BCnPDBAlF2wG)iK|?Y#Bi>iO1eEsZyJ2Sv*fel>x#@o>cV|URoUIJhnxHnu#9x2d+pl5mZONm~cQ;p@c&>C=~J2PCO;SA78}IQkguYSV|S)3^Er?Px#JFcTHnvG{Tk@GK0a4V2AT5p=)2YdJ0Uyi=U-&-0rK1Y3<4Dm3T4H9JNL>h2jp3HYBzG8eHVJ%`Bu}nI+?ho;kRut|oBjD^Rfr9*Mck1IkWc;}#`XE<pvWudV5W{7A6IU?-gc4#jA6_*6~*X(>Akp34s<fTyJIR1z3S)&6b@neQT4%|^v{pwFWKA$YPEWALpqSJ4K@`5+<x*gOJm&o|&ae%bGN4Y(h`pduOq{++c;(Y5llNLw+qN9?*9EJnr=*g7!?RJyLFQ9c2eoAo$uT}2OKmobI~BRUbS!f&sBR7ngGoe>gQ6Or5OgWM3;Xh&Rcg?&AihLJPx>;D031HEt')))
_PLAN_IMPL=make_agent({0:_SCHEDULE},**{'hand_align': True, 'weed_repair': True, 'sell_lead': False, 'budget_guard': False, 'room_guard': False, 'clamp_sells': False, 'dead_stock': False, 'terminal_liquidation': True, 'front_run': False})
def standalone_plan_agent(observation,configuration=None):
    return _PLAN_IMPL(observation,configuration)
standalone_plan_agent.telemetry=_PLAN_IMPL.chassis.diagnostics
agent=standalone_plan_agent
kaggle_submission_agent=standalone_plan_agent
