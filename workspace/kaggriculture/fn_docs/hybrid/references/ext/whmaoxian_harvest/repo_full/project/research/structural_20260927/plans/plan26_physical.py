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
_SCHEDULE=json.loads(zlib.decompress(base64.b85decode('c-q}vU2h~ua{MoRo(GXbu2z1dR&&zgR-!;s9>~JtaDdM+V4NS$elz^vy|+6bJ)Myek=fOx&QGF-%jvGFtg6h&$jIOR=jz}7{I|dU<!@L2^xM_X_fJn(A2(P3{^$Sv*Z=zT!KWYp`scs>$6x;Y)6c(Mef!I=f4cwa{g3w_t~OWi9`;w8>yMi+AOHOL@ZB%(o<DuQ|6zCk>A!a$KmPCL;;Y}k`{OS^PyR4@$kXn_hx6Bbe!vg!A9q*c2l8&GkDq?n?LNK1cK&ML{__6AcYpdc_UB(df7|KJCU1TC+s|LhKRiD?{yRR@`HX$If44&u_S@A@50B43d>%LYX}^1VzWOMq6|UQLx^9Pmu)TPZFOS+xemK9zY+47s&mVTX?=IJ9zI^ayj+1FFh5b5*M@>y;{-h0h#luef?dsiqoSeTu`swfE++6**`|$A7)#hf&1bunL2EW>D1*b0}hx+vJ%Z15p^2N{tl*5=?;x%63^Zq;hjtuEAGs#^2^n7~1*`q!$UTLZ(yYv2e_sAbno~-#dO&)xhNBjord54(}&pUnt9AF&Q$vTd|`trTr9=v>&c(2T^tf@tlnLhkZjr>|aju}dMrj6&FzcU`bbbfnJOTHR@GJaCScW>eZlphy&=lLtoM_M%K_N>kZ^U~7`cI)Ki2J?FOZTUgRZ$$$<KQa774pQ)q<cqAYeE0C-!|vVlpZ>6We18Ao{l8pJ&E=RK&r|*|d;WKi4?kbI-W(an@!z7!KHXx(6`YKJ=4L}bBisRe9>Y77Tn(`7=c&oQn0#NH^Y|rX&V);RbNS6^Ueb?u_s7SB-+SxkEf+AC^RA(9ar*rL9}Yb7^h4881Oq#|f?=u}zX-10An*0&B0`*gc)k<Bvw;z8XP#2(B!*k|<Qtx%5&G;(SmG?x`C(`pW(G3CE>7cZ97)8*&SuYw6qqNSy>BV<i2mv6?M_oHU(*@=>4!?76o((bFB?Ja0+~bur}bj)dBHUf>#wcJ__p&|NgU9MzZ7Q{c$B{{2ds$(Vti0zC!TKx;3WpWNz5U0L8hNj&oJ=~q|JdLfw3*I>eKs!fq;)P7eHSxEuV}{bBK$Y$e8l`a%1XD0|5UTe&+_G3?lqIT*OAWt-U}nG3Dn19}IYTH$A@)!V$wJ2tu9NHN&?kJR5FjF5}bl<Nf~I-Q(l0*6YnL_zeWzd^~|aKDr3eFG45r5BHD%?Aj20gYy^hv(uQC-U}S>|H(g6o=DNzS+pGBVbi&XAL>KZaglOg@nWiE48dog+?(W0&a-kF_lrJ1x{uR28TBe`DMFaBY!kGeO;5&kA3Zg9XadW8_qxefo_AU^<m1zmy^ud%!`IhXKk;ytpU8ag6erDdjM3ju{f$a?|E6+-Gtb|8D2+MT;PG4+;{)mQo&Q+5ysc>N@TJ<}PFME)S|@8Lz!D5%oo~Hc;b_C-nW4_k*=bME8H`MQ?&xDW=PE_MsT&uvbNLOrbeamm3fjAkXr$=#pRSt-8pDgOfK=R6CW_p}%s<3;<XR31d6O00!jeDq+D_pMuZZQSkB(EFr&o|uvMU|;dk`A0ei%Lg|NCnOkXYc(oi5-&t1kyex9EAqC+EI<!DGK2NslN)U)!3i9{;=q#Z&K7Ip-zAr|!lqlQz`vX3uN**V37ePl=S*BDI9Gm(I@-lnUvoYELwU{7Q3p#xvP)eD}OKogS1a@dPk`1Rb7VfIRt(JYm7E1=xvx6pa-Cmu-6915+_v-$DRO$7Yg6t_!S?^OLRT72M<6K>RO87vA769_y9-qkZqoIcKl^wPoVN95Ee&i4G(?+^p_<F_^UDc`ZXleGd%q=p&VB1q2je?AC*q`()sHuP|6__l!QV!mud#W^sC>8=?&~KJauc)(F1daLv0KkC|Tpi>84D>=*e(MxGrrcIFuA7f9!2sKaD|Oyi#GrJ<K(+?|mHFLC%?T{$Qa8@z<V$uMUz&evIp+7njtndXtuYd(NtZ?B2A4y$e=KyKw3VMDA$ur<BVw-&i7tqizMKdcdTOX+h~)@DAoQE(8s$RM}2!3Dl38|QEY_YV)B{_{qWYrna8t(Z|(IsW-&sA7xKCOv(na@dfYdYE+czCKRZ!Pr0C|McCJ_FGQR2zB`#`YCj=eK2Y^gtoj#40C`WhQjQDbjJCk)4IY^`q{rXil%%+${7{;aU>Qf{E1dtY3N{p7hh|Njp|@vB0;jji1gFCY&?LhkS(!vH3kv-7UvlN|A@j{HSX(dJ8Ned*ywbE<`(7z+uCq?YXKbbSWXa4EG?_*On%|*H!J>Y30}mNW2f8sVZbiugt`@%GcFzw(jnUm7^Nn`kD79(OatvSv&H$LR=z6YyG6GP6ymTWiE2BIoJBA%&bdTPAUhg{s9i+I*0SOJB0GPh5Q_4}PQWF}Y&ELroL`d$qTLlwfhAT`FhswERjLt{F$TI8K$$od5n_ec7|VXncX1&rb^Vn>4RQ&QfqE%%QSzeLGCFTcuOzR=Flpc!)uTLyGPKmqR2^)U8Baf|vmY9TwEnxtyN)SIwfNcB-h%5volku^Dv2huT<efQ0A5Tv-H|Ja+*V_-^Q+VP2Xws@=Dls>%u`g5mCr>i49lo9-|9iI^B`T3Z9;`*Tnek!LTRez8B|b?ll#bgJ#I{|L{B#e)XjIemd-s|5|!Jn!)x*Uj37vK?oPkb;fa63xESYcCptM}x+E?Im0oeAi}AKN<sdvE0Vwcc5h<Dyt`}i#<lc(Y1*Q^3V>z33ahM-HKJRz4%BlhD>;a?Ec9k=d^OOdF!C(PF%oUfEa*T#8bIfg}dczwoUn-HF5&E9Q0?3X>NsD1yhr%Tcl+C4RY?gOZg%*~HQmI(1JU$zcj@-JcTW<A_#T)>c`PV}Mj=Sy0_aFZFIbX@~0H`P^K>`~MIE?)CGE!)4`>{}D#RhU)%lR$`5rFHdBJtCaaiIc(1~LLfxbC=`k`h1=@&amLBQP=8K(8_s74U1UBn|t_Xi)EEO=8$z1u4<!7)k*)03g$e>{?;ueQ1zHPAJe+T28<hGZuj2YoU5CHGm9N+ipf4yaEU#XqSY_yn>rsD)14FM4%RcJdZZVuxNLVMh21W?<nVs%0HTN(b|UKC#pxi1bRYE4qQnXc%?c*Aa#6_@yz3`$dVdH2M1u)D^57gV}J|cY)KcMOqK>+@y!u4D+5c5;ndJL3AV8iM$W6bX?elo_hpC}n$86mT4j}iQ3e_>9Ym)T17;3(N-b)(ISP{EWLYeMSY~yFiC7S8pFFy9JCznmKe$IDnfii5WYY8j?Qt6KiD(v~C*dz>fvjHJ*-4&4c=WC?UUX~9${$|g3lIBNBr+$g9OHzD|7PxC5=!_jWwmqo0_=<EY2))FzVl4%m%j3H?1DMtEZ4wY%`uq1QpMZ3lHR0ZLp-JwQQ|l;g8Cr%q7@k(^aEM9#hkuu<G45+4JwC|>WKUKd;sJd_3Sa4J<axXIyznGf%epWs5ekBmqKUajo#X6YpgJ7?Q_u&mXIY28+1nh1iNKG>J7RtJHnIcGn>RFEiKID$IlNx-akJywj`~a$?XtODA4*JUJGAoKE}Q2=GairR~8g9bqeI%&bbWhuO}KLS^*Tt`y@de`}g{zRYzEXy{sq*sSQT^WJi|m$hbp{D@L~@Guap;GU5P9;FgtYN0=_^$qZhRlom|?H0fVTxoN`|6%6lm)I~c*CnIA7O#XdNU%M+Hw=1k>XdlhtPm7C@BR=J;pLDvn84h$Ksqm@`IR;Co-C(H2;6w`g6Hg$$<uY1!!Z;+A2FYGmw!AGFKaQwf1L~koO?QYVU$3rQaed7>DO(!*-lm5YIl;2u7OPeUGjS;NLo=$H?cx4pkf^WUR6^J2_C`v9_x>b**cEP59TSi@PVo9P<<;a1P=0Xo?l_MLkwEUVFQB;Cv>=DjkerSSsaEGVqnY5ydcn7xmnZgbFJ+j(GQiaUlAG1uNjA}ny;1Tf0L=!VWGyRvYz25zN94A5#r|}ph$2s4+$GWg)7Qh?qclysWQaDb8ey`@E<gP3<yJVa<<2gJU~Bru#A@hmB;ZqEe`jEMwvum>jX#^9wT2|Op{L`2m(){0!$duwE~jq9Xld(i6gr{%T1^jFID5w87KFLHSaf^2Q^<BW%_>jfF@#k&|E(_r4^HYS2M9+I=%t}V(1#poAq<M!L$2=vdfMf8gj=8FqnsBLUNAuB%lgi8ax-*=Hat6oJLU2Pc)i^*=$sr@)%xD%f-!*#hGfaRN4nU%Q8&~On*$v49M0h+&0Sq=Rse9Zw6ws2MF&SmD0NJ+63sx>RrcSM3Yl)!s$@b6#j`j48r|plhq)L3bwdT!F6WXV7;(xiwEz*FuwPS=+ignz@FU+iHlGy4$h`YH8@d=O)i5Rlz9B*h$oIX(ENXBFA;`*zVs^<(;T3R@s=igEvy(CfD!mC&9cN`~TDqiF1&NJMu_#(%?ACycmK#`KZsoUwSXsW$2x*?cR?yvyAPMYIpP-WOA0D1|KL3LXda^Rv>2nHl$rMdfyM@7>VA6O{Q%FYAYDI2<zBCyMDO3gfbn8Y`il$a8zH#c`181|VPsOTgh@|7RTAKtClgTZIX#y+--shL-|J_4?+>l!ej*Rt4GzhslrQfFZ7g(p${mu(FS!HrtXAu}$cHOE?1AM6Y*pvSoAP?!6NwSES)Ey70qGUqJ$ZNgN#a4J790=XVNpVu+G@K!e@K!Hfw&)*c3lxkSNB7O(eRyi=YXGh|ugi}Z_Kvfp&Embl08~mFx_lA3i@8^lw0*yjJh&-|=Oo}_^6DbnE^0ZapRgeN*035A{o$RhtpzBcM0W}$0@27tJpR?o3E}#DBKV=GC3oQ0GuLLbKo6)8MhE;QkgyE$38F(ge66kh;mz1ik#YP&;0SCZbuusSjQ1kQ6YZ64CxKF$S_$T6n+B#v+2M-3n(%{2!96`c-tWKNJwE>Gp_yWq>Q!2We5-VIC<&q(L(!RuJ1?!6HPl%Ioe7bnT3NdSoD#W=NZ{|Vnv<z=d@^9Slv=WItxA|YJuJB6tSC4G<=1W657hv|fwCM>5)c>8KB;fC<nS;H5}U|M(b5<^iCu5VV@%Ev23w4)^|XMN`k8<`4K4vOD(834@u(N8%AdY_|9zI0O5(l>{8yL~()NXi;BX;LJRvb<8aA#p{seR3>}g@`06Cid%PHQ6aSMD*ECz-vmXWIkQ)rAPx!hYdnKzGL`#Hk<rdqUDm>MK3={vMUsz`#=F*`Dwq0vM_jY;M)%k0(oierP%!JQFsBoA)|7f+6o7A|y00ZV7Go6Ty!A#@2-QS6SMe_K~Q%WECR@jbXkFx;Z5FG*t!m<{C02Rlm^fzN)S-Fz9Jj4ZapFQ!M|&Fg`bZ_*-#g&*#-dMDNR_?56s4MvIbJ+lyCYb$?s;Yn2Xms9=<ZnqW`aw!~iXz&!M!B(v22aRTla<!J+vbB%nQxr1|V+|}uO}H-|U{zrU%<`(Zg3J-5lz|=>jhqO6FFRL7&ybVv5dt$V+Xl*kNuSCG`$u*xAjn~XG>?!tTo@%~>8?v1CVOZimwAQeWFvUJQe6`fFK_^pD0`>4Xs-m#Fvd+vfY@1-oV|{{cpATZs2SIaI>b~=oZ(GwaUt-F@239XVM{JlpUZPg1Y;rph6hfxCWxxOPV&er8NRK@VCpTn$_w(E834`tE{)UNkjj3EtYb@GCqHM{*`!336sBTr&m$uW2eQ}wV(rphmz>9pJH`Qm%kL>zV1@EeRjn4lxcdbV_7Y>H2Lt&*-xLyup$0_xv0Uel(%g#d9G^Ux$OM+CrB=sK;;~UeS!oPF4#RDO=iZ^?+T~48uM}!}p+0)sTpHhI5jtEl=Y-#`4aG4e6*L&+xSUPJfOD3%(z>&D_?vzKD`T1AF&U0L={O)L8a?1q$G|G#4_2F%n?ROF{IJr*PC3I|QH3=~0b}Fkx|w=`X@P$81wfm*2=a0wZ<Y)5n;6&C<k*l8=hIj1@R(IjLI9sO`oqXT+J>WKr(yT0ZjX6Z)N{1~$_YL~G|+O}NI26;ie4EOWAxhiVuce5(|V2c6SJJmaaQ9<9o=Q7=e0@{-1tJZm0Tq$Vlb8y?^jo`62x2-iVP%*|Df#+j7l&h0nz|rjiQzTp$Q|goRs)D3Ena;XKe}DhVY@oqL>A~Zj<UR1Qw*>_KM<C0C_?-&!T;>A2Ls3NntSQI1M{sQ3MIyA3WQU2JXgvv1!tXsj!?|&@6+f#pJMPRjJgPPXR^}(Gbj&8J*I3%bV4*k2L<M8xf2JChY_rYj5X}t(r3|j(<DT$UBE7uA>mIYE}0;;yW8#^Pfibt=^Usa_@`cVP;>;tZbHx_ov~y34?{B8o^`L5sRLfr)!GnIzhNQ4PS3nM^C}~{(>*Obuq8Qd(&b*PLUJEe4u-x2!fo^39xco3c(u+bWBouUxd7pG1(*m08&OTPZEP!rIYS|`nKW&+4HRyj-Uxmy|><AJt47-7q}Ol9rA8u$oVCT-AfIvOgnSX0m{-N-E94aJXF(-q5(kUCw9KAMcUL<)W)c)GWU->?GGZX488#X5G1ytfFxQRTC)<HR9UC>@dnM2PB~Eh$+CSTCdT)H;!?Jyw{}hxXDOE2(t*I6Z|@1{9%EY-tRQcZ64^SVYixNTK#1qk2n#*YfD<yhl&{<X!DRIKcI1+rX{y4KS4rx^Oge|<cr;bf<WBLrJ`$7z?{Vf>4Uu*e%?jL-H+CR<#R=UyN(vakaAKKl83iwKnxzBH7+8p5CMdD92h<=Zsz%33gp}Dz!d`~n6Idk^q;vUNG5a4FT)#V_mdq1YG~NI`>%jO}nS`~4LT{78O`%!=fYv%0>-6CiblMIhvVAp5M6IBNT1a{*m;!%oyLSPH9Xyl`Q;FaklNO)zz?80c7k-dJ`K*C^5}bmu&jZ)WSS-}bBykCipsq2h`pj%(1p;1!qeU7e(Dtz&VKP5yTuNG@O44Q*n3RW%M`?BwHHx^F*Gco$-}ks5tWI9%2x_Ng5H+GTfh^%#U`{#BWTEa14VdAg7`V6KAT2BYpf?|nFiGJAJ}eC|i@CmcZjDrmk+>xxZE!1xNz7!ES-1G<Igby|sFeo;QNV>9i}zG)<1;0XvwnElL0AOkg+%B!;fDxmrQO2teLi$uuZLTPTjs=xJ2XOG*mWTcQxp)&^nm~&O)&$tzn0WrT0pp0+DdQ$YLxa$_RkCizwC?-I7*$2j_b4N<VvXtQ|`({Td^)AI_I1d&7>_6sbg>hGY-77O`70*N<emHY?Axbg2?h{V*1(c`|mH$0UF9P0aE5!`f70Sh=7qa9Q5bmTq}I)c1StrE6T0i+T9IqHA2?F4c{1iwpUVF^Rro9)iwAbjr68b{3unn_=D2dvPFO^1=26l9->gY!%kSce}s;Bor92s6?PACQqQ|gaf&MVDZQ*{JSyp5TW=mKHM@m6m?zIfDGmS%o-3qkwU?~+#Ch;T!@al(^xj8kV<BS!Mgc-7bkt)C8Kw19_lHa6oV=+#n-E3G?(9yHhN_dz6_iuKbE|$&(5gG^H=reF7sQZ8vy9xd<jTX6nXafKJy^1wl6PWq?Xz}cOhOE~*vNP`Sikh44Kv9uK)CGW)zx+F{G12-Yp5&nZSD70xAmlUOO%$}x+Dz{5t=|T^M)@9K$5{$bnF>o7Pc9;c7=;16Ef@`+xw=hhr)2WR?VA7L*rU|JKe2!2uDpR>4{^7&vSN5%gTxz^)0qrF&BUhT!7stE4_bul6<xRYW2Drs4`HMBUA{N9?L*h+Z1Ma`x>k^r-w7bQ|M(ik7R7a7%n%qO|F7iXKAFi@v%=J8>oq*IS02k4mB3ssl<kMURC}}Kk%@~>VC*$H>YV(WEMBEmty>F37cM#qt9k@7&8@9a-4UXw*f^=<EqtklPS`Uigl(?2GZFsjMiOu6&pd83`61s+w}vLF1SZ)K1KmmCLpb;p}H+;%5mc0HznM7JE|Q~5Nfg+H6H5MtZ)xnb^k@YnW4FPRWm9G&X$nxatI|0D;+Wf?H=i*x`~32@B};JNUUf|oeE3XI<(>M2)Q0l#fFQ4P=>Rp8!T!$@xUJ{a%D&gqluc(uPr$5G+JV<W{>~HS}caLP?nWH`cRvJ_T#}X)*qT*MXt_MMeSFS`Es{l^YaeDpbEgGQJwyjXz*!`D@vTS%T5Jjxj;M0Fo><za^okC<O;E!jaQ0!EEF({`|8HnK%txTekY{Eaw^mWaF~DVoat5t&s;`W+$yO~ym58%{X>4DXTePc#-ZQz_VqYl+Z6Gske7O_ugN|bNZtZ6n$7-<J~|U8P!=?{B#iS$O=IiiUYenWwrU?Ms`f@)3f=*Wv$7f4sY~PkK?E(zA6XcF@R9VINCFte@33Kodo@ZDOZ%~UI=d1wk2sJp|Da}~NbefAz9JnkvR-v&%dQ%q#HP)3sq`gzb-p#mP%<>bUDxCTFX%)q$mxdV_mBJ8DtZ)&4NA)$*KG`JdJl<Krcr9sSt8BXwhq>_Wx%z%!c^lCEBT>A3S(?vtXb}w7Agb@Ig91T=ko#Agi4HaV#o1KSv^yi17}fe03MiIPq{~TyXaRU2Mr-2UbSR}NUc|8cd+u2EM~nFX&qN#4tO=B{#iG5V&_@}JY+@r!Vxeret6KZ4WW)@Z*y?SDN1Dv@mNXAHDe4V*>Xl>2-tM2%SFoQ;UNCZq!P_LX|lj)by+l03Y|$1>c$13(n7KqM5j#5>BjyrL8mxbI(k!Wc#4(6#8YQquO%#FP$S9)6%#8cL;!`OaL}>_Ld)@}F0Mq%i5!na@vsJ@`-AZ)5|&Wk^)xRGFsj?{5M5`4l2Dh&Kb-LX*Kt~Hw^9%QZ?bZNQrAg1Jlk$?K*vk+8dUe+41!~nZK4%HS!)Pix*Fxptw*agRFuF{(8wK6gn>rwIxrRnZU~+CYO$Q%sc)UUIthV!x%9|(V_bNNS1?GmcVAs^Rk)(?#<E2V#MyahP^?Vk!fjMH2EeF7ZbV^xEmwf51>k_pN>QZMPD7|;szI7TVG|h%_hn5nCt~{u8&r5Or8P<B=m5+MSbl^Xfc_XH|MH`B5f<Fq6Fmufw07R6>ElIoZ_wsqOz9vJgVGx5p*;X9(7KRnkX=|S!jENU70m_k_K9pe3mPs#w@%PTkw>jP3C%U#6WI^G1WB1qAFf(ffwvx+swhfRq*LhzZ56=E)`mf@P9(eZ<gi4Zc@~|1(^r*~&FEy0r-}+#3vqf?#ueW3JoeMQkatf~YpEhuO?kyCe)bw?H}tg`xdyeXgQ7z;r<h%QUW;fLZG!zEl$01iO;S5uYE_4F#=5^HLd8ZUEb78Tb;6|s@9N-JBt<J{pq;nM)VFDeU#BP)dMjRkJNTl^E00^x@a9({LQp*;mJbHa1(tU4V%v}BYN`ELtLRX~)3(-2p`A$F@ikHeEL1uE;JHk2d}=XHSy!Q>*-Dro^OR_COT(|R2oJ44Nw7>!dElV#xyB}Hbo;wuR6!oS$+}!e?v%BA7$jFoK^krX{2U9M=n~bcQO$-C@knwz^lATgNag&V$*PyBXNC?~w3U2se6jeuuq$dZ>)xcYFoOM#P?)L2BE&pUKpdz-?fjo9yq+uHH=NkxFmD%wM5veE`P+Y&bfyYEB(4<Co!a6Hq)l}q!qhKO)RnedTaO2oL`HEUmeuGDWI=UXEoE0JWpCNUr%ugXA=iz)4vX(>GM<!Q*42du67NhS!z0}rRun9~4hsn=n2}ASflwljv62wFDWsw8BCn30>H@D!VwEOn0Z*`R*&~!Mb~P1zH-+0}wh&rHwo;{P39UnBFkFU#QJ(7y;RcTxAVQ_)l5`YFoE;N=d@#De;d`yEvs7fTSdB3ZUJ=~`VjxWI5M(5o`nzBX6blVm7eZltHo^dctc*{W4~!`oU9Y8JwAZBa*n+0OQ5lVknf7Zkfkme~FCjp*3u<#Qi67TkYA&!;<+#<nKS>^SI}$3z#!f>5A_Y=u^P+~s&wPI9DOtCQD1D{!Pq+(S5pWI(ULZa*)a<T<nkkAfwWyB1Bgt?4KY_>~zLokiBdhzS<6ka6b-JUYM!SS6dfG*UaIS4dhpJaP*GUz>o<tR+I2sEGAh8#cp+YE%QvzUw;=`#>W~|?+OB|;-<xpMKwazZCJR}%VZ^-M5GFz~ut6cP;S!V}@cY*~OBt%}RL$y@wD$pYIYs*zJ7?ARSSlykqttWw^MI!Y36H4xWMnDvh*<yO3*^<1_*UW^9db^?4$-w6_2{?R&{X-%pYxEA3i*O6Qa9SHZ#N~*FOKH(D&@@-V88(`j4=N>eVMCQGQsB0iG*NL^U4D!exoGNb-u|ph%Ay>!O6JN0Pq`TOu&pAQCp_)t*(I`r%gWrfs?3F6oZlL594lF<NSd?8PAT2U$n1}q?Hrrl&gYkqV)2cs!7Nvv>WzUn-9p7G?>ywPw}m<r%PZoJ<Er$nFF?l2fKyKUBE;q52iECNE@7A#FYdc+u=plPrGbA%UE?v;er0x6y;q%xE-Hw2v%qgmyF_@;6pK(zc^B5Uqfx$DL^Oz#O1fW|ykuKQa_L$x6}-*`z|2g)rC{o=ZqISDYEnSx<4LW;{aQ;XvbYk)H;_^$cxK%RRSlH0lZ!FaPXpn*B-3JWO8?&&{caX>W9%M_CHRnru^|7rw6Qk}PJyB%$gfn|lRAyRj>q@cLm34w|0r%VNhw_rJ}n_JWeh<fWDk`INYZ5Wib+Om%FY*X0G*jjgyaeGD=Mn$01u}93Du^Z?`%;Jw%(wX$$j&ZVloWQ6lUjUjRd1%W*1)ccNn>gzA0c1ZCK0m#}ws=hUgYRc{#w!JtSR<eW{hT%vOxhjZeHI#l@ycaIeg9sWzTjnCSLS<*(1PE+r8yBSb06zL~98<@Mtg8?H$NqkHMBL+pC0uHxlT0PY`KON$l0tStWSsb`f$rPiu~+}c%;E`h<WsH+mJM%GL2>vRTAAYm8cI64^XGa!RmzzgA7lOlhl$OvF;ADlU31&DU<&QgPJzsa22{Yrbby-tM{))$1T1SPwsAt?>nqk6g8>WWm+>rfc%x#!CH;)9f!Cc-4Q{->KZF3NLJUs^fh1@e0?Jfy-a*_F)X$qtkZOF}FijEOVHAl;4I0E7+YXt~k3c1X3USj&*AKYq-jh0tyHobsd9Dl$XAMC2TBU<Un`$}-y98iA0Gu+-j^7b>?tb>KQ0&2xEimge#*tQSjfT2yu=c3)1yHo?VebtTw?C!m^JaY?P|?UKWUiQUn{;TpYJ+VyQEGax$k?DFP$@rMlOB`yw0Qr!V25$G6Lp<tGBiBzP8*C{w{aTfzVr`}JmO}QE%ndK6XC>5*QcX<#uYXvbauhZUI>RGBW2dHUbQb#h=-C>_qdO=u$Q0D1s(dTh$T12SLhMiRa{-WwxtdSnuEwZ%;-5`x71q0gUq4q}gzPV<LwgFWmy;5fdk?G2&XkBs_xXliT32dmiL!%q>819C_`{gfKQqD7JH-(b2Rj8sgCC9@t`lmbtzm^2`-U2~AE(mu`d#P*@(pbSeg&305Z;1qQGn@p%Vk3`3KoS{RgVW@^jpb0e0Fd2FQ65HRYmCe(sWs)PT5%g?V1e{$h-nm>W}<`56)~^ujaGppBec~rs@~b>=y*GQl8c0-I83v{Mn^CxgSZCl8KY*LK(HuuV~xm15UNSJpT$?BHNqwdc3C^Z11#CVI#qqNK%SA+X!s1Y4YvyAqmh`sXRs4rkc(hAAyr8lTGM#97QO}`j0(>xhsU@Qmjke|TE`Fvjc#X%`Xjq)T{gvJxKx+Jol*QNLwwT+2sWa;vJ{D{Ld^~=Rs!c`9g`Du2M;a_R`3}NIZpyD>0~L#KnO;0%ElBkB8pS8kPkoxegiyT)~CeKv<uHh)&1oZ55G+lz!{76y@Oa%G%_?(o4Q4$l?CM>!A(s)pxRB!KmbI$MZGtqk_5J&Q>xq)YH4U?IVsPt`bHM3(kQaV!jw7>Zw#BtR4fy(4vulJP%TS=-n2!GL>$S8R0jLDqm;d%c^-)%MJZvaZAu+`URIj#))w*NHr~p7x!9W2UiSMHx;)Re486}|rTB@cPOxB^CilwZDS6HZ!Bb20mk3^|OAR!DJpEwM=i|jUraTr*rGh++eyI%^JEt0%`8r^J#odIj*e`!=mog!&3Ms%-sK>*plhTA^iC;D}-Yufgs|1Y1LEmhw>Jo@p39q^oo4Rpe0)^7}4dcUZD)kw?F3eR$;&s1kVlb9G>X@QH#w6|$LHKn}1~FIz9$aBE3bQNpD_X_z8HJjgHH3YoGvjq-t_ndgl~&87D;e#4sa2(hnY-&s{@X`^U}E<a8BS#3t&#DevMVU=wzL_D+~qpfTvGcfR>@Vw_FBhCA-)l%GE9iST9#VbL#({PH~mr&!8l}<yra?qHuy>@1EVKTp+wS1;|oMxaNoOGLr2J6({Ms*<}})hsU2#kq2Wtfp-gRI-FVRFp9_3|x{O6$H@641%L=ICJQgkAakmTnV#Pe8cOz?S$!@<3o&i8Pdj%YL%0VSv=Cjfm%(J(e$QyGlVp2eCZ{lro%QtvGf<LSHl~nVl%*RHw1XODGnFM6-4RGGta*6x=8ldt5B~uEU_xA;rAnr%A9t@p6`QCg*ROAQ`g>OoK!F(BtvCLhbF+d3m>YQAOE^puObTHh0MZ?n;sIHN59U<2Q+y;1>b4Ec^9;4g=sZ>8~=cSp?S`F1`&Z!gZ2=2MzoA1g=d9S%|zYDQ?lWyBCH;`5NY_Ff2iYHPOR$e6F5-y^(3?wo;zmQ_$0X?VDw@XMPX2kSN#hg@faKtZ187I2GeYwQ9PW0Ev*@En$S6EOR1dI7pR*~l2NC^nc|FN+FPuCfnSdLp=dEmYBp4{}&;z<Cm>}P8P6nd`28|Nz_-}wy}A?e3Pdxx{YM(&Me+-BIcm8jXWna5ah1<M}2w^Zig%l`d<bE}Q-uq{$N4N7-Nf{yI-3Zi`y2l2+BrPurnb8I=1HYtP*(ZI+517$K}d;')))
_PLAN_IMPL=make_agent({0:_SCHEDULE},**{'hand_align': True, 'weed_repair': True, 'sell_lead': False, 'budget_guard': False, 'room_guard': False, 'clamp_sells': False, 'dead_stock': False, 'terminal_liquidation': True, 'front_run': False})
def standalone_plan_agent(observation,configuration=None):
    return _PLAN_IMPL(observation,configuration)
standalone_plan_agent.telemetry=_PLAN_IMPL.chassis.diagnostics
agent=standalone_plan_agent
kaggle_submission_agent=standalone_plan_agent
