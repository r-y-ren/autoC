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
_SCHEDULE=json.loads(zlib.decompress(base64.b85decode('c-q}v(T*HPa{QNlo(JvBkdpnzqvj;yD6K#)Jva*sL4eONV4NRhzZw2_Q{0`Np3caK$n2UWbx*gqTy<AhWmRQHMn?Ypzc>H>>u-Pm+iy4j{PWFEuin4EdDz_i$FKkOZ~y)A7axE8`>((K=imP4<Ig|e{OQAAfBEU%-M1fJ-`{L*j^7_%ef-}S51Yq-dG+I)A6~uv_z$n|jyIdzhll^$Ts->C>%V;X>HN>xOWq&ezCAzvHhcQ=*YCeS96mmM_xnG5|K{D{hW)S@+MhnWdHd}zAHV(n!>2!+Mm8Ju)AK*QnE&!T!1#CkQ<pRL_SNgd(*rLC_2b>U`|m$}4*KbMcz=KMU`=XR%zV|J{$O`8kjGbTW<Q*Vv6xiDlETaXd^mi2`Q^)%f^R;}+vBW{nu(_u&28iIJsUK<rw#S<&Ffe8EIbYA{qJADx%uJn_U^}<%~ns&<1033V2g#C4?}+D`@0VpmbJ;3A%0%@BbEkti`VvXPfY(pKImyyl6m^^ej454MV}U~G*PoH`0D=fj=!QjRm&&MUi>tRcm(QwPxBn!cX|T+!1!5{ZJhq;@wwjayBx}k@ac<NX>QMCrl0;zefh0^9W#{jOdIbzKQo@NbbfnpOCAk>118m;zVMVy{M6EpJO9V$Ln<06n5krMod$Tl$pO1+cD{mHk>}9qKSyIeKRWzWdm?#|^~l$EZ{HqX-~aOG!@K)8Z{Pgu<s4kvaMgSJ_TAl275}JnWt^?xbe~VZK^ObeF*o~K;%RIjDmP0!50rth3ow2SSg6vLgex7UYk<+r4e;>l>FLuCCqLnG2|7;b(<9+~)yFQKnQg&NF5LlRSoo7KCgrr;=}lz>1o$n)gWKloF(1>T6Ekdn;w?0JNz*I&e1Mm4$tL!^b}%{gm?6_6w_@#s3x`nWdBD>TPE|aP7JpOnI>=<Mabm!57vruyHaz6~!-|h5kL`T?(jU3FQ1wY39~jRh|3b5d2i&##bI&LJa`yfRjuZ&Cq;ECI+XAQz1E|*fU&_Nv?h<JM%=1eBtz=`<_`!#O&6WWz+O6bQkL|ai$k&K_4rMQDIwEpo8Ure-_h(ZBg7j7M5WU#c=BgKM@V$gnmi+^a+Z!JZQNFmhvmfNn-Y?v-_xJB!9shKA_wKJ2vI}+~K%D4RP<VZW1SZdoo}=HtdiO8HF8mRkAH+{SV_JFxI9=AWKT^kkyzwazr{^3zaX!KDmn~N+cT0owaxovLbD{J$=Cp&En?7#*OJ=?l__|>}^XZ548QSsnjTfxB^PT5M<6G;xj<d6_V_Wo}S@Q82TwQ=S6W1^C5<IUo^Vv$+U3zO*a>LtEHz)I#tpPFAhmI;v+WCEQm5`sSHaJPeDkn0(Wy$*@_Ln?eLxRYysekV5uvu)`z3^wD+pyLE?D;t(WW*CjCuHr$JS{SuF|=c1WTEcN^^;bJ8>nko2@J^17{N<0=N;&_cdoe?H8q!}bKJoUSJ`U^POKQ~5dUZ$m|J;42jBb*FVJ3iEg)h`t?aGgu+oSj8^NeGL7r+S^G?Eq2GG62%?=KC!Oh+eOU-NGXIJp1JD?}^1p(kH)5Zl47<^V-au1j$h<Li~dk*XQaf=kqibTB+pvqUVY`hA^)=bNJtp2pvZm5pn^l2y4@?f5b!FXm_@EOtF(R?d#r)vb6#6i>_$9x{}7T3e0A7q^(J{O?HF=O5VWZu;W2%c9Npy9ArhG%`Rf8G*b<a(aRm-Rd_ZG{K=NMO#+xdtG(#+|8QK0_Rt8mvX|&+L@#VS7I4DKAiG6!M%0J`i;&YVQMX!Lo3}pzu{-7CYq~vnMfX8Az@G1T{$$Tn8^%S&?ges+w?$t6b|tm(+tQA1+}PIN#KGA)zy(ZD<0^+mbWpSWO4balY+Z*hlVpt;LHBoaKriaiv)r;`M#T=Z|&^sU02GB$5Z&QP|MEg3zuHDZNU_zDY|6Zqr}Zc$lS1WL9HjzSf~~NvbJG{A_Uf<LR$1*g6J@?09$g@qb>{%AjL@Q#z~>P8wH&Gd*&em}C?vbbp$3epiR-dfGH^U;X&)jmA-?cWB4gU?L&|bjpA5Cjh+W8&lyR#w|b-z;*<uRfJ{59;UT>@QnrVP}x`vF77m4-`(B4KQ!z6(RFZ|)#<rT;<G|L0xP+wJJ*5Al7NP%QNV_&3Pv`i3W~>bmm448Bv*})4Bp#UF<?GhDEyqb>mKdu_1)9CLwRp)RM%aj_&oq{h-ca3<8aY?YV~n~+6-NhUsz1>^dWIegRe!WIl6WXYXR|FoWW2hdfL~P;gbuom@Zk$rA*Vu*|LTSFAb@;?C~HBGk2a;u<u~Dfv5qj8Y~J|#4OQ`2M+G}Dm5$A*t?VA;=i2Fey{c}73<k>F%vPHt+L9+GcWA_^5!KK8LLKu&Y;M)b;j%N*CwJ@Bv==*#Gz6ReiW=Pn7q($Q)2k8%e6!osmi@=z{`!yl&t6TLqZzrmp%dlE4zob?!%d$QRcvJkQX`6;x*_UddZF9NyI>LnXj-Sb<u~NQ`i|w$a(Fb>2~EJ4f}@z^Nsp~a`&K9n8GnbXfV?o{DB%42^J?Ucr<o5)ngO;CoeSE1y=<>YEfD_!ii^E267ni3gZ*9Vh8LhMud+=Z7)O{t#x&jq!07FT-+SMgIs@jR${3123iD9fQFdcO)q#NAWIrkW~T%Q`m$iYU75n;Bo-U+Ih2X%I8o;ZMiT>Biaf*byx!sgG3+s=IrKi>#vvHDgrEdwyhIDSQ`|KvGH|NY^f^jZ_yFuq-rp$+1e^#CGqTmt1E4i-nJ<?dAiXjMDy_KYr%L7kBy+D(sceVSKfHPSmrvO(9!NvYwt7r0F3@Q(+10trzlVD2`G@Rl8Nx=itM`El#izY+QAr5>Tas6AlhuerJKb5+58wog-%+R~2GIbXttgX(hN6OG$`5P95DHY8^4-+yXR{WzP~rNCVlrxq$qmrtn~uo%%O%Y{yb&B^jnGu2vV=lOlFi>(3eU=L!HhBIv^v2$E2D5BCbp92^DWZ^qp92pu{^zQevU>r=GJnxBE>AB+q-OxCG9-o`<pPcjr}#XA}w)RHFphCGqL%&aNIfVW~F<B0@glvU)Ib?S}F+NA2V-D$<OPp43Wcojyd3A%Nimvi%N;aDnFe&ly7Sw<Ym{EzNcl2y)k%vW#|}yCP|->u?!j^T}XnPwR4&*2Vidb4Pd1gLM{{QAjh|9*>Uxojq2`4uIgTJ;b!!kgH{v;^SpFm32$~!slQxub_xnWiVR%1kjgDZS{2oM|FAxQXA-^?iWTJMvft>{<KN=-Z&202at*8bgej58Q=%a?AhYMenPcVGqU8o5vJ=~B8ZPocBfu;p`-9+AK7D{w6$ji>^?HLdv+yWP5$3WKT44t<w)uIWx+w_DM8!b78#=~~1QT-y0>7tc26~d%Mr6~h;!vv%CF!*1l><A=T=TpHX_!4?PV16*OC0e?k>ZKkB}%YvIgPJDQ;l3`bqT}Z*b`^H20n8z!c%Y%B!vp-oT0GS>ZJnf!n&gQWjAI;1Nvgqx!8)^x@oD4rQyBjco4{WO4}7{dVlxBtNXj|LBfoc`W@_Sq>W-~3s|ZiR+fo`l^Xv|*H^zVC$m{1Kf1-=xvc`!p?5MD-mg;eLLiv(^xr%gG0QRzXnScId$EEAOvO4mb+oEr7J)C>qfxjFhWUnlk*4&&c^-npPLq)>JZ7sQ9GmoDeuy0!vNHD?S-(iw*cIA^`&Ar(td?i2>Gv%jVD+po)%Ry%tsvqvC!A@0ug}G?LPJnJAyeB}cL4%&zNhWeWTzPgy;l_2hEB*~jdO_3qEdjEk3r?b=YI==n|0I-HBfM!fC&e86LN+f^>LdL1Yl!e003nMu%PFpo|=tr9SkF8CCVs<VI=Vw6=XQHjCfzAMII8JvHF6r3Tpu277EskC44y`MvQxjU0i3Q3)dXPK+uUzGRo=$n=l(K)(Jq`)5_$=$F4-#25_;Z`PUDZs75ymaZd;tq9)6bxmt0L;cJ3dXwdY@>;j&ztdYlG*ha>-;=wkGUtq;2dJH(@qmy^-6M|MHF!Vp0n*-1x5Z`EZ4_)((Ru3pv$^>{j5g=sfHEJDx&6T52^N~5IB>f(Xw{!|l2}hWS5Wq7Iwce-Q${apG&Yz`#q->XN)~k3En5||_7Iei-AxJi|qZC85-jQ!#L5Xhn*8+o(<_~f|{9g(ux~Qu-!%<vRC^%j*vh;8uBQDsfVxV3?$)YkPO^Bk%u*uf8OK&4P7jaqG>8$v3;r!PQC?qUzlQ1rQI4AY%TuP*Ps5ZA0Ho%c;6Im%i51{aA{`^?k!>^7sSuH(L-lel!3NqWPbL-&xdcaO_=n)Tq%u|zrXn~c-U_Mh3Bj@%+CKIo@&lU!J4}?>JU3sN2sua!EAju+X=J#J(6G6Z65=E#4+M%^|D$UlFqqK~=i2s}hWLqD)wG0VzvEz(WImv^;M_XJUQV2#TlWE8I0v<!TY{kHH_LbKTCly*#yv7T~+Efj$i9Lx>?Ldo#=vw-E;h<j)<>(Ls$k`$apxU8DOh8c|JL2a)G&Ti~G&aAc3q~LOzw;PqqoC|^;Bl=(d1!WL<ku(7dO<j}rq_|oTY}?Y6?;Y~#`cn@QM<4NyZRW<8FAP1%)*-Ty&5rwcF3zWVe#s?fR8`NOkO@~4VQ(F?Cf9e>#{aHXJvjHYgfT)b;wW~lK>^jdFtWt-FLrJreq(C$O&S~Qx&R#cbKUfDnX|aj01(f$V6cPVn7rx@fW*k8bf7hDN;oANHSnC<&_S>&G|Io6^MgL*WKU(^<cY2P)-IL*n{ZSkx0S(i3r&+F`LbxPO)l1p$rlXPobASJ$?}ecM?~`^hIC*DnFN!GUv#)2>;c|QH+xb9JK{5VlrAraHZmGi3(dv2`Wm8dv3U2>O;acaFJEme#J27ay=>G%|hT^A;c@y{Fn(yoc(a5Ud8tA^`Z?)a9)IBTx)vr*A{;u;;3&N2^ME3&aXfMVcLrbEI}hoau77j%_!23m-}|*{mKfj>91%;tI#8nBfJ?ZVYJq1=+G6qfSQyI6UB%KNa?U}r9MSI0z^l=9|*Ba56NdFSqfB`>rkp!rcvq;`BhKjsM2b86=CJ8YoRa49`xe>@`b_wwhC+O)D=RD2JSNWmF@mze5Rhr4r@D~q<vw6)__}bZuj$ZS%B=%+6Ay1T@>O3=ya-x_Xz$A=sGPHxJP(7QdoquwGt<Y$3#6QizQN@%oFyKV`8BwkR0||94sOyxgs+1Xki_0XLYQ@>qTl?HcnFsp^|QuRzwa))l6bL9&xshtP(O?0T+1pDvVEL9MY7l>SVAqwHGG0ixeNy6Gm2GXjEf8gMdJ7UUcOJ3ALoGji%B0<t!(~fJl<@D+&iwWI^GR>>xGOm%Cgzp9Fezk2hB`w@KMpq0wQUhArs^QAg-it#D$MC1079gK0L4O)_OHgEmeVSK4ZeMCsMz1=WktiPEi|@D2zrb%ji*XbIDGCM|?Y@_)din<E+@qkV%%;3ypX#qufMk<$aV4+8{Su7_+eT^8BjL=>htDkp<L49;K(-E~AEEtjqxg=eTHAsTerVXy-qytUwkqWBJ9E(MjE^aikoux6Xn@_iaTUK0X3F*XVB4rB+$D$u+dQ^Qttx%3JIH=tmVO%#fuIi4eeVge_mUBOKNw=B3^;gVEz>j?vi)$f~5)1@IS30*ax1fWam(1NqGzG-t*vM4M&B01qEvRcX!{dcqsG#73(fwOiaFk2>sra&!$`LTr&<m6)IgLruhOhy6}Eq7J^|6Eod0oyB8rI2m|FksaB4eblL6Z0Z~A~jxi!;4fzQgXr*^iBMN@uM+zjEBVVPwqbr9C%xwv#vPd>WmbugcrRC<_w7>)D9C+5l4YcY6tc0dT^0sK1EOl);T$_sE)9<#!B-!O%#^O#f`Lu#VoCGfp=_m5Ab8H>L~Nuv!tdMy?+|**Ods}6Joux;>gZw>B`w0q03V&NSXi1-f&&c3gMga8nqBPbO|0!<p>fB7m93HS{l9~Qb7vIBD$*^p`eHWSz=J8Xw_#edWWv<U2h8m8a$g~Z>z4=*X)(znR(*Qa>t8MM?CO}noY(HsS`Lma3ASOT}iLfo!3*R1(Lt4#?VTt0^lL7(l*%x1)>Tu3%^Jsvl8tK_^qA_ve(dBC}c;ST+&gic#6a}uj(F*TY(2#HIfhIXH_J35)l~8F>ngr;r3kGzuP1`ffz)S!3aRO>3&KWzrJWho&cu&0Jw=u7YZ~@g6e}#+xWa_<<65;_m1bDa7Eg~yil`JZT7=x3j*w5Y(Ap`X0@PQN<KSODGnu}5HexevgZa3^qym98<R@Y#l@J?#wuc6t@cWu4;egzwi3-usl!2Ye0Lp$WO1Fv1RE{Hp=+|>y}+T*{kS;(K4t<Qe|!7f8YMAtQGozD43m^1*J|x!`J=pCwxBs7oJB4{($2;OrxkoyDjDGi$m^wE4P~`u99L;@Lj(#M2|B;ybQ8VNr6-YmZyZ2!1HkA@Xx7M>Q;|qI+yzqU)yP0Ix3Z=p;#LRvf~j5fN|4&}V$%`A9C&Mb;h9m})H42!s_<1ulxTRR2I{3kV?bsp0Z{OqmoEEvnAI#-!+l**QeNK_q0v+aFflblBxV5PM5y;TH3nv%1?@6!AKJGx?Ni6}C9S#zIrNtg#f&-Mku#xisq>MwdaI9_8#HZDqW(}_)#i}*@@xSY8P|*D(#xtJU>+M+v>eI+3`<M!`k;kacHKyX6uByg%wZ5#)4_Dd<R>`91=ePXy9aUDsiRs#LP2Z^3Fjb(ZtBvuz<rspiRCv{*&7FXDJaWOz$dK{f`7EU6$?rtyHdT)_VX!;^mr&cEnd%dL)I{OkdVk2p2_gSo0?({Yp&=qPO1gp*H;^1QZG&2R|7G+hTsShr6?++Qb7trN9kfLcK(<-)`(cW8b268wu!tW5#~^DG2XyEg&^KlJN^}eOQkY@sS_yETq<<g5XvvE>$ZDnYW^^zm6F6J6w#<i5U4oylo~=cc{`I46oO)NEk+LJ;9!jmMnxIDG76)8XhqZlhE<yZ{dx-MK%w<Zri@-oh}+cxHee~fwiw6Q0zR!yc$H#h4u`U~h^p#~N=GP$;AIHCQMvl$$YTdF>8O)-rge)Uyie*Kd;<S+j0a6ZR;{9#GEN;vzs4!W7l-yR5<ONJ-jz{8te#NHs#)!u;+&W*g8&4P4^ya=+-@}~g|UBl*^p3p(D@BjX0g8>1LZ`1+yCRRPk3?9t_1RKLc@>-d1rP0l4oVuNwkj6qO^)hva%R6I4X=QpHL)gua$vK)5|31#yJcP2~~v^*%)4O2QP#3N^+;Z4FtiZLRT1rwm=UxCF~ozCbBTMs&@j^L?jU9_L8xkY`p=GmfoIPY;gX4`{uiX)^f#s<Msogu;01^*K^E>&bdTHouILn<EIuv8O%{sFbvvqM}k`b$Nx|}T?X)C(A+8QXwEG;**o2Q>xv>Qy#of_#bYlPj?4^S)LpG9Q=&|w(41bY3{Y-dol+13SW+0KkWSH}jM6DQg#^ki;QSK~cnY%QMUtozG$tpzgBz$`Ck$6O?a^th(!wu;*_Q)r^CGkAG`fPokJUfy8kmTw1Y|19=5;S69I%$X=6f8h53FgXnsfM;;UK47cm!}qu=p_xOlc^x*PN(0@>quyJjH|Y8tWkbRvuPgqr9lW8u=30GkfeVTnpEE9<EJ{Yin48kMfw{nFLgK)c}GMa6m?%HZ&hu-ejYZlz~%|>@D~EX+S>~;RfQ=9YsR3mScQ14U-TMzF7-BTnWDc+W`qjm*m9z1GN=H%Z#CDSd~(mO7q@wJI8`dGO!>E6M&++DR^|b9X8!EG^eSW*%?cani#lLQ6k`i9?DS#i(^1V-XWAANTId8A-R#YL9;6xJ8BOFwwagRPQD@$V{r5wM{syl@dP(DeF}*y_Av}br#qWeAFDov*}f2VIdt{~KuaBu1$~0#EXH;SqLn~pmDPo3F~Gc8tZbrfz}2UJ-zH#cib6=FI0f&#6GSD`?6ry_dsMb{K7HWne;07Zh<03}_Er!|xSI&P->8b;<f?JW8+J$wZ`Z|nLY&W;JRWAq0Wx4zvrg7eHX<|+1IcD9;lS%i%X|X}Kie;#=i^trLqzB{iI2{J&u1d+NMHwqizaMC^GPMX4!dy*a+B*7XPQhLBEzCoVRX`4x{vJiXF?lEr)D1lGohL7LqjSyBK)E_!1#vM4Vlw;yux}?3oy1@?lG^dQDH+y<!u5cqBD;?sCblL=h{#cEq0X3Xmx~4E+uOU9H7!JF!XhZbJ%ZC!DD=-1$fN)jioK@!4v{pI{4vvLjgqWZQ;7xT|G!7UI)79esO!-MLh);^Lqxds`3la^h-)koCYI;EQM)|t*1$7ZNNLE`GuAiOO3#zY0uGjFcejr5*%8U&sD!at`hwAJ5Yhr=E&qbR)qfzm`79ydkv~g39fR(pTa%Jy1w~s=@tb;0cO~1e9vQtBvq=bI}^QJj(DrUg>4Eh{PFlBTdntD@JC$vh=f4$55W@I7P?j@iY#4v$hJWb;pqRD%?PPzvPj6G!0I1E5wQeW#%bR6<!(%cei^v7xgrF3BMpKQzPX@CbC!tfCxmRckacE-402wLO&T49QcG+R{pS-5+p(JP#irp>OK~T_d!l7;BA-42*n+GYQL<`x9nW<o>Hv}eLn>u%vbqzw(Qd%#Hy-xV!Yq(wWr-Cfj2$rdRb>hVdoX*kDCJ=nXxaB8dUrRPS^`E_>}HOFnT$%V`_!*;oyF}so1)?kRiX$vflE}t+HR3B5$`huybXiU#@4A|R6w%F>9XcYrFK=AJpG+)j+1#@kI@&ZKb6Kb2!Iz7v=yv|u*z&Mwkvs-(=pr@%_;NZ_GOJVf}mtnzsIY9E^7pxRiM<DZ~6#NN*{S1d}lTb9{k`$Wk47EGa)={Wnbm^rRI~7Bq-fdm;JFD#1cvvYY<ClZvWZnCTPGiHV|<8YH%S5eS@R#NeFp5xGQD-k*X^4l^yYnJl!8Q&j?&lh3w@XER@)s#$;F1DpmCQ_<d$8!LFEt#jT1Vvic53U~i?BH~CO@{FEF>gH%?cmJZsXbQ(bwyJ*`9<8R+3wQ~5vh@GY=JJtVXZ0!T>IfNisVlnWD98muNwyD-cL}@EzWrcoxj=hV$Drp3hUCZsuXjEOD7`j{4u_wJ1knU>pV0iG-+r~$NJ>zs1KeoE^PISXoQht8r+jJrisI?+J$7QMDY($rBlrCbLoICRAJ4Q@6(w&J=w?**Aieg|97T-0D5N2_BvI<n%dzD52=~i1w7ULCpr8b!$Scp5J!}0m1Qo{#;ocSPww?rFREO=iXjpG-RvGj*Qhx{%|*P#J1+ZoCBX*3o2taP8tnzAnI2WSI7yAI4X6o0<}Sr}L4koS*XD-Y9i3Vm*<-PT(O2X=*GR9VQe(zSy1u_!CU4ABiB2No!?QYc+pi}`AmgLv7|-Oa*|5sENllrm(QfE7J4PDxj1I8^%38gZJrHhZP!?TdyjhSf(&iDRdGf$_VJSO1X0X<rcY5yy4C)G1yYdzV$j*^9syWyqV#0yHYNI1I&`bBWenoZVtp7p@}Zc*@a^axT?HfkD`~?rtQVgIeTTrHv%`&R%y#iV>~!Dr@Qbjgbc~5<v*e4*=u4jOfe5#0A*FXLU@#Q{2IR4i&~;rz+Lq@>+Wa_7`vARG82(jC_YLdqon+oPj(MO!JTd8QKT((^mxs$AoT0j4j*JI=f?Yj0YiErxktq+1p&nA~t11SK~HS1cJH>IiTbC$Bq2@Fq!YmYS+}JfNTTt+O4Lw5jCHhK#&a{F;|p+ThKooR~2`(r~(UsgunpgMuKTS0S}F+Gow_Y7Am$`of7N!g{M5Rcn_<s*G;ej<p&v@iTqc!MfU(KjrDIh+DUmDhmKV%Le--9+PCVA5*MekHCoV<g*gg^PF7QtC}q~886whjY|vj^2L5wEXA}YOZ9moXtq{xl8F<eOSoMwD<!A&DCNL$$&=h5}X@f&nA~U386gyxjvC3y0jI<xh2+|dRN0Cku&{wYh%C_#u<$QN{Z#5%hK0qDCu*Gq~qdi}qZ=79Ue~On0QLH12l$jjSu;ZA13N0m}JSzg^h_-~i<_HxL188yCB9t2bwcJCn0#@flpUX}dkR^pCT4W-!>(cI%QaP~GRWB{4st>3$QG6TkMNrVU{6~sJX-sYvUF&6p0iP56s^~dCJBKUNEf~t}V$v)|C|;<9<MX#bd9K&%%Wm1kNM2kvWT2W8D3YkPJ&q@WLdaIv^_ln*zOskFS_|T8L(9Zwb75bI%lkx+^vRtq7*sQmO>Q=*AB3F=uVsz33p5c>Hi7rMzsAlWpivl1@;KQwhKy0wQ(yu0Ft8Cv458UTVzAO!k#eKWhFPwTjo{Y69Sc?|XLt3BTZHlx7zHiD)nGB+;=MYTFgl}=Q(nRf_b!)HTn<2GpVvYoHhj<NPlhgR;Y$j@2x{L^;Bb(tu8PKXlj#fV8%-Pr9Jxlj#dtywV44C_E^GTx<R%|W*i3RU*hzB<R4_dqNArsJ5q0>lw$+Hb;|^`9*64x=k|-f1Qp#AF(G;Fj)o4=HjQ_+5q6Hpuv!WV=Tu$0X0AS&WrMFbB2NmI$M}UVLQS4{GRCSvF$^{g2fXmUeT*?1I)sd%Z+mFGEE-61-3s+nv2}O?OePP@<B{ln$eZp~)$xR#Ck^s(&e*D2XOD$1kyZ&tmRl#IbfWw0ha!ehepi$IjuhYY<l@zN5QY~7A(Y{43L*A|T=yrW$=@wu-1|JQ@Yc`8ci*<CV(5LhLtB00MCXDha*kbj)w$YUVH4Ik6SWY826oqTI{oe11*XN(hyuE32$Caq?yor}z#8eTa?sJkv^&!YBbNIx!kpi3Z=*`&Vi>NZhzH;%3#$ArZ@Ma-J4Zw0OTZ;OKD3d}V;tt?CE&61450-FgDu9!f`ctH_f{L))(`+;0X?1g!-J+3jQ!Wf7<ha~IzyT{w(qk4r$0;&WOhn5poR0<HE1G?|{aFdpRIxp#EJ+i_l#XqZp3*>E>iWpL_=G4^REG*np}!(DoG-s#3x)DuuIf<6Sn1SiG5rE2NTkb5Yq2V;m6AuY(ZAZ!8!A*N*+o8vZb`^iG_{B71uwCyWVajhns(RC;yoTR%x<H#<yU?Ko_L#cf82@`N^0PP!%ET{j*pnB&XyQl6oqKoi$mywE-$+jWnm&aX<<LmaQG6<OnR61;lHMCj5tt1<gh;X+K?*oT7pR@`REE=vBa!-8r{~Y*hP5}CIrPUl`Dz0y4};0n8i}`9&IE^QGrPQv<i{B3@)!{kJtao*a?LHLX)#CQ6Y9+=o|yO$s(cAjV@QhjqKdVz7M6ac`7l-mD=d)@Cmv*MeP?Aa3-NV+_RuoJpwemd&Qxm9#mp?n{|s6`9fb|UXznni~-kZ#IJO!12YKqGa5|J+=!C_s_F_lch(u42{h-Vlf5RLprImHV?z3;ADHjTTig{uN0)zc0q88|<;Ar?o=bAZ?)p5Fwmi?Q26ZI`WjBt366I>v788x)qWEYG*ugf}Ly;k#gP4*yD+75c<z@&?l+R;g)V*_G^_sSE$YMQ1c(&#|5#{Gpb<{6hDYR-G*5Rzwvr2j2YyDBfo|VE{uK`=HI_T)351ziT+Xv5~2klBF8-BZb0Z@azpfN)i#li8Qi^-01?{y+Y1$(l8Q@w|pN@-gy=Ms=0my#HS#b{k^t&2+OVZ99_nmRkRW5AJvJ{z3y3U`1+d5njDBz;WtW`B)?a~?OGNIAE=n#Qi`Zq5@iX+v%JHK#G|$}}iO6;bSmVsmNR7JN-d;kaHzTGJ2@@9$kvn6Dq|-P6HMFxe&#ujzc#b^p51UyZ4wits<LVH$%_{8Pybn8pvpQKo;R_wu4thEDNb6JsbcF$8f4be-)!5t)A3mJIGjTzL_AhDNB5b1u0P91(0S{ReguTbGa3>#ZQK(M>pe!(MLRI@v{)IO-6HqVd>O^_3Fzjc4LcPM^|Byf-3X>s7!=wJdrnGK(=3#oEHZrj=;#pkpI-)ia%zl2%djCq>6DnjN9ph!J)g{SCi4QTY#@xr_tSNOU1)_A0(g<5MEKBInI9gy`T@`e&QE?-Jb@fh06c5qt<!1@qf#*u<wihGZmgu?^T~k#n6DHa>dIv;rvhT=vGXh(GLl`9va;gK#l4u!a`@$OMk|(RtlzOO4YFLNYI=iL0{w??n8Fqlm9z)K+P~%zvWx8coi<u=YY=pqe!-lpKTQLf@7zwB18GyP>HsPe0BTMx<8ieb96uf>PDnuLM>QTMyCtsUhE7{E294h?YsGnfZO`9{wK%X=iH')))
_PLAN_IMPL=make_agent({0:_SCHEDULE},**{'hand_align': True, 'weed_repair': True, 'sell_lead': False, 'budget_guard': False, 'room_guard': False, 'clamp_sells': False, 'dead_stock': False, 'terminal_liquidation': True, 'front_run': False})
def standalone_plan_agent(observation,configuration=None):
    return _PLAN_IMPL(observation,configuration)
standalone_plan_agent.telemetry=_PLAN_IMPL.chassis.diagnostics
agent=standalone_plan_agent
kaggle_submission_agent=standalone_plan_agent
