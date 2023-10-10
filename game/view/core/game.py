#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""Game criado usando a interface declarativa Teclemmino.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    23.10
        🏭 Reformata puzzle com cena automática (05).
        🔨 fix lançamento do texto, not yet (04).
        ⛲ Desiste de Missões (03).
        🏅 Inclui medalhas no inventário (02).
        ⁉️ Incluir Questões de texto (01).

.. versionadded::    23.09
        🧩 Incluir side games Puzzle de troca (24).
        🎱 Pool central de missões (23).
        Sprite Labirinto working (18).
        Sprite foi working, SpriteSala & Elemento.cena (16).
        Cena as Background (14).
        Declaration and retrieve for sprite element (13).
        Fix Texto popup with new class (10).
        Spike for Teclemmino (09).
        Spike for game test (08).

|   **Open Source Notification:** This file is part of open source program **Alite**
|   **Copyright © 2023  Carlo Oliveira** <carlo@nce.ufrj.br>,
|   **SPDX-License-Identifier:** `GNU General Public License v3.0 or later <https://is.gd/3Udt>`_.
|   `Labase <http://labase.selfip.org/>`_ - `NCE <https://portal.nce.ufrj.br>`_ - `UFRJ <https://ufrj.br/>`_.
"""
import unittest
from collections import namedtuple as ntp
from typing import List

Dim = ntp("Dimensions", "dx dy")
D11 = ntp("Dimensions", "dx dy")(1, 1)
SEP = "_"
One = ntp("One", "d f a i s h h1")
Two = ntp("Two", "p b hd sc fm fs ip lg lb ft")
W, H = 1350, 650
LOG_LEVEL = 7
IMGSIZE, IMG_HEIGHT = f"{32 * W}px", f"{4 * H}px"
# noinspection SpellCheckingInspection
A2J = "abcdefghij".upper()


class Log:
    def __init__(self, min_level=LOG_LEVEL):
        self.min_level = min_level

    def log(self, level, *args):
        print(*args) if level > self.min_level else None


LG = Log(LOG_LEVEL)


class Teclemmino:
    def __init__(self, vito):
        # noinspection SpellCheckingInspection
        STYLE, NADA, NDCT, NoEv = vito.STYLE, vito.NADA, vito.NDCT, vito.NoEv
        STYLE['width'] = 1350
        html = vito.html
        self.I = html.I
        self.tag_one = One(html.DIV, html.FIGURE, html.A, html.IMG, html.SPAN, html.H4, html.H1)
        self.tag_two = Two(html.P, html.BUTTON, html.HEADER, html.SECTION, html.FORM,
                           html.FIELDSET, html.INPUT, html.LEGEND, html.LABEL, html.FOOTER)
        teclemmino = self

        class Folha:
            # def __init__(self, img, nome=None, **kwargs):
            def __init__(self, img, dimensions: list, nome=None, **kwargs):
                _ = nome, kwargs
                LG.log(2, "Folha", dimensions)
                # dimensions = [4,4]
                self.dim = d = ntp("Dimensions", "dx dy")(*dimensions)
                self.img = img
                # self.style = {"max-width": f"{d.dx * 100}%", "max-height": f"{d.dy * 100}%"}
                self.style = {"background-size": f"{d.dx * 100}% {d.dy * 100}%"}

            def get_image(self, index):
                index = int(index)
                # position = f"{index % self.dim.dx * (100/ self.dim.dx)}% {index // self.dim.dx * (100/self.dim.dy)}%"
                position = f"{index % self.dim.dx * 100}% {index // self.dim.dx * 100}%"
                # self.style["background-position"] = position
                self.style.update(**{"backgroundPosition": position})
                return dict(img_=self.img, style_=self.style, dim_=self.dim)

        class Sprite(vito.Elemento):
            def __init__(self, img="", vai=NADA.vai, style=NDCT, tit="", alt="",
                         x=0, y=0, w=100, h=100, o=1, texto='', foi=None, sw=100, sh=100, b=0, s=1,
                         cena=NADA, score=NDCT, drag=False, drop=NDCT, tipo="100% 100%", **kwargs):
                _style = style
                from copy import deepcopy
                self.img_ = deepcopy(img) if isinstance(img, dict) else img
                style_ = {}
                # txt = _kwa["texto"] if "texto" in _kwa else {}

                LG.log(8, "Vito ⇒ Sprite texto⇒", type(texto), isinstance(texto, dict))

                def to_int(key):
                    LG.log(4, _style)
                    return [int(cdd[:-1]) for cdd in _style[key].split()]

                gone = foi() if callable(foi) else foi
                _ = score, drag, drop, tipo
                img_, _style, _dim = [v for v in img.values()] if isinstance(img, dict) else (img, {}, D11)
                if _style:
                    (ox, oy), (dx, dy) = to_int("backgroundPosition"), to_int("background-size")
                    style_["backgroundPosition"] = f"{-ox / 100 * w}px {-oy / 100 * h}px"
                    style_["background-size"] = f"{dx / 100 * w}px {dy / 100 * h}px"

                style = dict(width=f"{w}px", height=f"{h}px", overflow="hidden", filter=f"blur({b}px)", scale=s)
                LG.log(4, style)
                style.update(**style_)
                style.update(**{"background-image": f"url({img_})"})
                # noinspection PyCallingNonCallable
                cena = cena() if callable(cena) else cena
                LG.log(3, "Sprite(vito.Elemento) ⇒", img, foi, cena, style)

                super().__init__(img=img, vai=vai, tit=tit, alt=alt,
                                 x=x, y=y, w=w, h=h, o=o, texto=texto, foi=foi,
                                 style=style, cena=cena, tipo=f"{sw}px {sh}px",
                                 **kwargs)

                if img_.startswith("*"):
                    icon = teclemmino.I(Class=img[1:], style={"position": "relative", "color": "grey"})
                    _ = self.elt <= icon
                # self._texto = Texto(texto, foi=self._foi) if texto else None
                if isinstance(texto, dict):
                    self._texto = Texto(foi=gone, **texto)
                else:
                    self._texto = Texto(texto, foi=gone) if texto else None
                self.vai = self._texto.vai if texto else self.vai
                self.o = self.o_ = o

            def copy(self):
                s = self
                attr = "img vai tit alt texto foi x y w h o".split()
                mtd = [s.img_, s.vai, s.tit, s.alt, s.texto, s.foi, s.x, s.y, s.w, s.h, s.o_]
                return {atn: atv for atn, atv in zip(attr, mtd)}

            def _do_foi(self):
                _texto = self.texto if self.tit else self.title  # else CORRECT.format(self.tit)
                self.vai = Texto(_texto, self.cena).vai
                LG.log(3, _texto, self.vai)

        class CenaSprite(vito.Cena):
            def __init__(self, img, index=-1, direita="", **kwargs):
                style_ = {"background-size": f"{8 * 100}% {8 * 100}%"}
                self.foi_evs = []

                img_, _style, _dim = [v for v in img.values()] if isinstance(img, dict) else (img, style_, D11)
                # style = dict(width=f"{W}px", height=f"{H}px", overflow="hidden", backgroundImage=f"url({img_})")
                style = dict(width=f"{W}px", height=f"{H}px", overflow="hidden")
                position = f"{index % _dim.dx * 100}% {index // _dim.dx * 100}%"
                _style.update(backgroundPosition=position) if index > 0 else None
                style.update(**_style)
                style.update(**{"background-image": f"url({img_})"})

                super().__init__("", **kwargs)
                self.nome = kwargs["nome"] if "nome" in kwargs else img_

                self.elt.html = ""
                self.elt.style = style
                if direita:
                    ptl = self.portal(L=teclemmino.parser(direita)())
                    LG.log(4, "CenaSprite direita", direita, self.nome, ptl)

            def bind(self, ev=None):
                self.foi_evs.append(ev) if ev not in self.foi_evs else None

            def vai(self, ev=NoEv):
                super().vai(ev)
                teclemmino.mark(".".join(self.nome.split("zz")[-2:]))
                LG.log(4, "CenaSprite vai", self.nome, teclemmino.vito.INV.cena.nome)
                [foi(ev) for foi in self.foi_evs if callable(foi)]
                ...

            def __call__(self, *args, **kwargs):
                return self

            def parse(self, ref, *_):
                _ = self
                return teclemmino.assets[f"{ref}"]

        class SpriteLabirinto:
            def __init__(self, img, index=(), **kwargs):
                # from random import sample
                dx, dy = self.index = Dim(*index)
                xdx = dx + 2
                all_images = list(range(32))
                all_images = all_images * 8
                # _index = enumerate([sample(all_images, 4)  for _ in range(dx*dy)])
                _index = enumerate([all_images[ix * 4:ix * 4 + 4] for ix in range(dx * dy)])
                # self.salas = salas if salas else self.build_rooms
                self.nome = _name = kwargs["nome"]
                self.salas = _salas = [
                    teclemmino.sprite_sala(f"{_name}zz{ii}", img=img, index=ix) for ii, ix in _index]
                self.matrix: List[SpriteSala]
                self.matrix = [None] * xdx
                _matrix = [[None] + _salas[ix:ix + self.index.dx] + [None] for ix in range(0, dx * dy, dx)] + [
                    [None] * xdx]
                _ = [self.matrix.extend(row) for row in _matrix]
                LG.log(4, "SpriteLabirinto", img, self.matrix)
                self.lb()

            def vai(self, *_):
                self.salas[0].norte.vai()

            def get(self, jj, kk=-1):
                result = f"{self.nome}zz{jj}" if kk < 0 else f"{self.nome}zz{jj}zz{kk}"
                return teclemmino.assets[result]

            # noinspection PyUnresolvedReferences
            def lb(self):
                dx, dy = self.index
                xdx = dx + 2
                winds = [-xdx, 1, xdx, -1]
                for index_sala in range(xdx + 1, xdx + xdx * dy - 1):
                    for wind, winder in enumerate(winds):
                        LG.log(3, "for wind, winder ", index_sala + winder, len(self.matrix))
                        origin, destination = self.matrix[index_sala], self.matrix[index_sala + winder]
                        if origin and destination:
                            origin.cenas[wind].portal(N=destination.cenas[wind])
                            counter_wind = (wind + 2) % 4
                            destination.cenas[counter_wind].portal(N=origin.cenas[counter_wind])

        class SpriteSala(vito.Salao):
            def __init__(self, n=NADA, l=NADA, s=NADA, o=NADA, img=None, index=(), sid=None, **kwargs):
                # _salas = [vito.CenaSprite(img, ix) for ix in index]
                _name = kwargs["nome"]
                _salas = [teclemmino.cena(f"{_name}zz{ii}", img=img, index=ix) for ii, ix in enumerate(index)]

                self.cenas = _salas if _salas else [n, l, s, o]
                self.nome = sid
                _ = kwargs
                self.p()

                LG.log(4, sid, kwargs, _salas, self.norte, teclemmino.assets)

            def vai(self, *_):
                self.norte.vai()

            def parse(self, ref, ix, *_):
                _ = self
                return teclemmino.assets[f"{ref}zz{ix}"]

        class Texto:
            DOIT = True
            modal = None

            def __init__(self, tit="", txt="", cena=NADA, foi=None, nome=None, pr=-1, **kwargs):

                class TextModal:
                    def __init__(self):
                        self.answer = None
                        self.radios = []
                        self.textual, self.questions = tit, kwargs
                        self.engage = self.dismiss = self.close = lambda *_: None
                        self.modal, self.texter = self.dom("aaa", "bbb")
                        LG.log(4, "Teclemmino ⇒ TextModal__init__ ", super_text.kwargs, super_text.question)

                        _ = teclemmino.vito.document <= self.modal

                    def bind(self, e, d, c, t, q, a):
                        self.engage, self.dismiss, self.close = e, d, c
                        self.textual, self.questions, self.answer = t, q, a
                        LG.log(4, "Teclemmino ⇒ TextModal bind", t, q, a, super_text.kwargs)

                    def unbind(self):
                        self.engage = self.dismiss = self.close = lambda *_: None

                    def option(self, _txt):
                        rd, qu, ct, fi, it = "radio question control field is-info".split()
                        d, f, a, i, s, h, h1 = list(teclemmino.tag_one)
                        p, b, hd, sc, fm, fs, ip, lg, lb, ft = list(teclemmino.tag_two)
                        if _txt:
                            k, v = _txt.pop(0)
                        else:
                            return ""
                        circled = {k: v for k, v in zip(A2J, "ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿ")}
                        res = d(d(lb(i_rad := ip(id=f"_radio_{k}", type=rd, name=qu), Class=rd) +
                                  f"\n{circled[k]} {v}", Class=ct), Class=fi)
                        self.radios.append(i_rad)
                        return res + self.option(_txt) if _txt else res

                    def dom(self, exi=None, mod=None):

                        d, f, a, i, s, h, h1 = list(teclemmino.tag_one)
                        p, b, hd, sc, fm, fs, ip, lg, lb, ft = list(teclemmino.tag_two)
                        ii, iw, ig = "button is-info", "button is-warning", "button mr-0 is-danger"
                        eng, dis, clo = "modal_eng modal_dis modal_clo".split()
                        card = d(
                            d(hd(p("A V A N T A R 🐧", Class="modal-card-title") +
                                 (closer := b(Class="delete", id=exi, ariaLabel="close")), Class="modal-card-head") +
                              sc(d(fm(
                                  fs(texter := lg(self.get_text())),
                                  Class="form-horizontal"), Class="content"), Class="modal-card-body") +
                              # ft((eng := b("Entrar Aqui", Class=ii, id=eng)), Class="modal-card-foot"), "modal-card"),
                              ft(
                                  d(d(engage := b("Entrar Aqui", Class=ii, id=eng), Class="control") +
                                    d(disengage := b("Cancela", Class=ig, id=dis), Class="control"),
                                    Class="field is-grouped"), Class="modal-card-foot mb-5"),
                              Class="modal-card"),
                            Class="modal", id=mod)
                        closer.bind("click", self.close_modal)
                        disengage.bind("click", self.close_modal)
                        engage.bind("click", self.engage_modal)
                        # cancel.bind("click", self.cancel_modal)
                        return card, texter

                    def template_modal(self, ev, template=None):
                        ev.stopPropagation()
                        ev.preventDefault()
                        template = teclemmino.parser(template)
                        LG.log(5, "Teclemmino lModal ⇒ template_modal", template)
                        template()
                        self.unbind()
                        self.modal.classList.remove('is-active')

                    def get_text(self):
                        return self.textual

                    def close_modal(self, ev):
                        self.template_modal(ev, template=self.close)

                    def engage_modal(self, ev):
                        ok = [rd.checked for rd in self.radios if rd.id[-1] == self.answer] if self.questions else [
                            True]
                        na = [(rd.checked, rd.id[-1]) for rd in self.radios]
                        LG.log(4, "Teclemmino lModal ⇒ engage_modal", na, self.questions, self.answer, ok)
                        self.template_modal(ev, template=(self.engage if ok[-1] else self.dismiss))

                    def cancel_modal(self, ev):
                        self.template_modal(ev, template=self.dismiss)

                    def mostra(self):  # , tit="", txt="", act=None, **kwargs):
                        modal = teclemmino.vito.document["bbb"]
                        modal.classList.add('is-active')
                        self.modal.classList.add('is-active')
                        self.texter.text = self.textual
                        options = self.option(self.questions[:])
                        _ = (self.texter <= options) if options else None
                        LG.log(5, "Teclemmino Modal ⇒ mostra", self.textual, self.questions, self.answer, kwargs)

                self.cena = cena
                cena.bind(self.vai_vai) if hasattr(cena, "bind") else None
                self.pr = pr
                super_text = self
                self.kwargs = [(k, v) for k, v in kwargs.items()]
                self.question = sorted(list({k: v for k, v in kwargs.items() if k in A2J}.items()))
                self.answer = kwargs["Z"] if "Z" in kwargs else False

                self.esconder = foi if foi else self.nop
                self.tit, self.txt, self.nome = tit, txt, nome
                LG.log(4, "Teclemmino ⇒ Texto", kwargs, self.tit, self.txt, self.nome, self.question, foi)
                self.modal = Texto.modal if Texto.modal else TextModal()
                Texto.modal = self.modal  # dom("modal_closer_", "modal_popup_")
                # self.deploy()

            def nop(self):
                pass

            def vai_vai(self, ev=NoEv):
                LG.log(5, " Modal ⇒ vai_vai", self.cena.nome, teclemmino.vito.INV.cena.nome, ev)
                self.vai()  # if self.cena == teclemmino.vito.INV.cena else None
                # self.mostra()

            def deploy(self, *_):
                pass

            def esconde(self):
                LG.log(5, "Teclemmino ⇒ Texto esconde", self.esconder, callable(self.esconder) and self.esconder())
                self.esconder.vai() if hasattr(self.esconder, "vai") else None
                # noinspection PyTypeChecker
                _vai = self.esconder() if callable(self.esconder) else teclemmino.parser(self.esconder)
                #
                _vai.vai() if hasattr(_vai, "vai") else None
                teclemmino.premiar(self.pr, vito=vito, tit=self.txt) if self.pr >= 0 else None
                pass

            def mostra(self):  # , tit="", txt="", act=None, **kwargs):
                self.modal.bind(self.esconde, self.nop, self.nop, self.tit, self.question, self.answer)
                self.modal.mostra()  # classList.add('is-active')
                LG.log(5, "Teclemmino Texto ⇒ mostra", self.question, self.tit)

            def vai(self, ev=NoEv()):
                ev.stopPropagation()
                ev.stopPropagation()
                self.mostra()  # self.tit, self.txt, act=self.esconde)
                return False

        class Puzzle(Sprite):
            def __init__(self, img="", x=100, y=100, w=900, h=500, foi="", pr=-1, **kwargs):
                self.pr = pr
                swap = self
                cena = kwargs["cena"]
                self.cena = kwargs["cena"] = cena = (
                    CenaSprite(img=cena, direita=foi) if "dim" in kwargs else cena)
                self.cena.nome = self.nome = str(foi)
                was = foi
                foi = teclemmino.parser(foi)
                img_, _style, _dim = [v for v in img.values()] if isinstance(img, dict) else (img, {}, D11)
                dim = kwargs["dim"] if "dim" in kwargs else [_dim.dx, _dim.dy]
                dw, dh = dim
                LG.log(4, f"Puzzle(Sprite) foi {foi()}:", cena, cena() if callable(cena) else "#", was, dim, dw, dh)
                super().__init__(img="", x=x, y=y, w=w, h=h, foi=foi, **kwargs)

                class Peca(vito.Elemento):
                    def __init__(self, local, index):
                        self.local, self.index = local, index,

                        pw, ph = w // dw, h // dh
                        """largura e altura da peça"""
                        lx, ly = x + local % dw * pw, y + local // dw * ph
                        """posição horizontal e vertical em pixels onde a peça será desenhada"""
                        px, py = index % dw * pw, index // dw * ph
                        """posição horizontal e vertical em pixels onde o desenho da peça está na imagem"""
                        super().__init__(img_, x=lx, y=ly, w=pw, h=ph, drag=True, cena=cena())  # , **kwargs)
                        """chama o construtor do Elemento Vitollino passando as informações necessárias"""
                        self.siz = (w, h)
                        """redimensiona a figura da imagem para o tamanho fornecido"""
                        self.elt.id = f"_swap_{local}"
                        """rotula o elemento da peça com a posição onde foi alocada"""
                        self.pos = (-px, -py)
                        """reposiciona a figura da imagem para o pedaço que vai aparecer na peça"""
                        self.elt.ondrop = lambda ev: self.drop(ev)
                        """captura o evento drop da peça para ser tratado pelo método self.drop"""

                    def drop(self, ev):
                        ev.preventDefault()
                        ev.stopPropagation()
                        src_id = ev.data['text']
                        local = int(src_id.split('_')[-1])
                        print(f"local -> {local}: {src_id}| índice -> {self.index}")
                        self.dropped(local)

                    def dropped(self, local):
                        # o_outro = swap.pecas[local].pra_la(self, self.x, self.y, local)
                        # o_local = swap.pecas[local].local
                        m, u = self, swap.pecas[local]
                        u.x, u.y, u.local, m.x, m.y, m.local = m.x, m.y, m.local, u.x, u.y, u.local
                        print(f"índice, o outro -> {self.index} @ {self.local} <-> {u} @ {u.local}")
                        swap.montou()

                    def certo(self):
                        return self.index == self.local

                    def __repr__(self):
                        return str(self.index)

                from random import shuffle
                pecas = list(range(dw * dh))
                # pecas = list(range(_dim.dx * _dim.dy))
                shuffle(pecas)
                # Peca(0, 0)
                self.pecas = [Peca(local, index) for local, index in enumerate(pecas)]
                # self.venceu = venceu or j.n(cena, "Voce venceu!")

            def parse(self, nome, *args):
                puz = teclemmino.assets[nome]
                LG.log(5, "Puzzle parse", nome, puz, *args)
                return puz.cena

            def limpa(self):
                [peca.elt.remove() for peca in self.pecas]

            def montou(self):
                resultado = all([peca.certo() for peca in self.pecas])
                print(resultado)
                self.vai() if resultado else None
                teclemmino.premiar(self.pr, vito, tit=self.tit) if resultado and self.pr >= 0 else None
                return resultado

        class Quiz:
            def __init__(self, nome=None, **kwargs):
                self.quiz = kwargs
                self.nome = nome

        class Mapa:
            def __init__(self, nome=None, **kwargs):
                def deploy(actor, local=(0, 0), **kwa):
                    _kwa = actor.copy()
                    local_ = mapa.get(*local)
                    _kwa.update(kwa)
                    kwa_ = dict(x=kwa["x"] if "x" in kwa else 100, y=100)
                    _kwa.update(**kwa_)
                    _kwa.update(**dict(img=self.parser(kwa["img"]))) if "img" in kwa else None
                    txt = _kwa["texto"] if "texto" in _kwa else {}

                    LG.log(4, "Vito ⇒ Mapa deploy⇒", txt, _kwa["img"] if "img" in _kwa else 9999)
                    # LG.log(8, "Vito ⇒ Mapa deploy⇒", actor.img_, type(txt), local, local_, _kwa)
                    sprite = Sprite(cena=local_, **_kwa)
                    # sprite.o = 0.5
                    return sprite

                self.mapa = mapa = teclemmino.assets[nome]
                pool = 'bio atm xpr cli fri geo per enc sup des res cai jor kpa'.split()
                act_pool = {k[0]: teclemmino.assets[f"m{k}"] for k in pool}
                act_pool["w"] = teclemmino.assets["mcli"]
                self.acts = [deploy(act_pool[key.lower()[0]], **ka) for key, ka in kwargs.items()]
                LG.log(5, "Vito ⇒ Mapa ⇒", nome, mapa, kwargs)

            def vai(self, *_):
                self.mapa.vai()

            def parser(self, ref: str):
                if isinstance(ref, str) and ref.startswith("."):
                    _, _, repo, folha, ix, *_ = ref.split(".")
                    LG.log(4, "Vito ⇒ Mapa parser⇒", repo, folha, ix, teclemmino.assets[repo][folha].get_image(ix))
                    return teclemmino.assets[repo][folha].get_image(ix)
                else:
                    return ref

        self.vito = vito
        self.rosa: Sprite
        self.assets = {}
        self.last = {}
        self.classes = (CenaSprite, Sprite, SpriteSala, Texto, Folha, SpriteLabirinto, Mapa, Puzzle, Quiz)
        self.cmd = self.vito_element_builder(vito, self.classes)

    def parser(self, ref: str):
        if isinstance(ref, str) and ref.startswith("."):
            _, _, cls, *ix = ref.split(".")
            return self.assets[cls].parse(cls, *ix)
        else:
            return ref

    def vito_element_builder(self, v, classes):
        (v.CenaSprite, v.Sprite, v.SpriteSala, v.Textor, v.Folha,
         v.SpriteLabirinto, v.Mapa, v.Puzzle, v.Quiz) = classes
        builder = [self.cena, self.elemento, self.texto, self.sprite_sala, self.folha, self.valor,
                   self.icon, self.sprite_labirinto, self.mapa, self.puzzle, self.quiz]
        return {k: v for k, v in zip(['c', 'e', 't', 's', 'f', 'v', "i", "l", "m", "p", "q"], builder)}

    def premiar(self, asset, vito, tit="premiado"):
        mdl = vito.Sprite(self.assets["CN"]["_BADGES"].get_image(asset), w=30, h=30, tit=tit, cena=vito.INV.cena)
        vito.INV.bota(mdl)

    def cena(self, asset, **kwargs):
        self.assets[asset] = result = self.vito.CenaSprite(nome=asset, **kwargs)
        self.last = asset
        LG.log(3, "Vito ⇒ cena", asset, kwargs)
        return result

    def quiz(self, asset, **kwargs):
        kwargs.update(cena=self.assets[self.last]) if self.last and "cena" not in kwargs else None
        self.assets[asset] = result = self.vito.Quiz(nome=asset, **kwargs)
        return result

    def puzzle(self, asset, **kwargs):
        kwargs.update(cena=self.assets[self.last]) if self.last and "cena" not in kwargs else None
        self.assets[asset] = result = self.vito.Puzzle(nome=asset, **kwargs)
        return result

    def mapa(self, asset, **kwargs):
        self.assets[asset] = result = self.vito.Mapa(nome=asset, **kwargs)
        return result

    def sprite_labirinto(self, asset, **kwargs):
        self.assets[asset] = self.vito.SpriteLabirinto(nome=asset, **kwargs)
        LG.log(4, "Vito ⇒ sprite_labirinto", asset, kwargs)

    def sprite_sala(self, asset, **kwargs):
        self.assets[asset] = sala = self.vito.SpriteSala(nome=asset, **kwargs)
        # logging.debug("Vito -> cena", asset, kwargs)
        return sala

    def elemento(self, asset, **kwargs):
        # kwargs.update(**asset) if isinstance(asset, dict) else None
        kwargs.update(cena=self.assets[self.last]) if self.last and "cena" not in kwargs else None
        self.assets[asset] = self.vito.Sprite(nome=asset, **kwargs)

    def texto(self, asset, **kwargs):
        kwargs.update(cena=self.assets[self.last]) if self.last and "cena" not in kwargs else None
        # self.assets[asset] = t = self.vito.Textor(nome=asset, one=self.tag_one, two=self.tag_two, **kwargs)
        self.assets[asset] = t = self.vito.Textor(nome=asset, **kwargs)
        t.deploy(self.vito.document.body)
        LG.log(5, "Vito ⇒ texto", asset, t.kwargs, kwargs)
        # logging.debug("Vito -> texto", asset, kwargs)

    def valor(self, asset, **value):
        self.assets[asset] = dict(**value)
        self.folha(asset, **value) if "*" in str(value) else None
        # print("Vito asset, value, self.assets[asset] -> valor: ", asset, value, self.assets[asset])

    def folha(self, asset, **kwargs):
        img = self.assets[asset]
        for at, fl in kwargs.items():
            img[f"_{at}"] = (self.vito.Folha(img[at], fl, nome=at) if at in img else self.vito.Icon(at))

    def icon(self, asset, item="", index=None):
        self.assets[asset] = self.vito.CenaSprite("") if asset not in self.assets else self.assets[asset]
        element = self.assets[asset][item] if isinstance(self.assets[asset], dict) else lambda at=asset: self.assets[at]
        value = element.get_image(index=index) if hasattr(element, "get_image") else element
        LG.log(4, "icon:->", asset, item, index, value)
        return value

    def parse_(self, toml_obj):
        DOT = "."

        def parse_key(key: str, dot=DOT):
            # print("parse_key key: ->", key)

            def get_parts(key_, sep=SEP):
                tag_, *parts = key_.split(sep)
                # print("parse_key get_parts: ->", key, tag, SEP.join(parts))
                return tag_[0], sep.join(parts)

            if key.startswith(dot):
                """O identificador é uma referência para uma folha de sprite ou um ćine da fonte awesome"""
                key = key[1:]  # remove o ponto inicial
                cmd, name, tag, *index = key.split(dot)
                index = dict(index=index[0]) if index else {}
                result = self.cmd[cmd](name, item=tag, **index)
                # LG.log(4,"parse_key é uma referência: ⇒", cmd, name, index, f">{result}<")

                return result
            else:
                return list(get_parts(key)) if SEP in key else key

        def go(cmd, name, **value_):
            # @@ FIX
            val = {k: parse_key(v) if isinstance(v, str) else v for k, v in value_.items() if SEP not in k}
            # val = {k:v for k,v in value_.items() if SEP not in k}
            LG.log(2, "cmd, name, value,: ⇒", cmd, name, value_, val)
            self.cmd[cmd](name, **val)
            [self.parse_({sub: v}) for sub, v in value_.items() if SEP in sub]  # self.last=name
            # self.last = None

        # toml_it = [key.split(SEP) + [value] for key, value in toml_obj.items() if SEP in key]
        toml_it = [parse_key(key) + [value] for key, value in toml_obj.items() if SEP in key]
        [go(cmd, name, **value) for cmd, name, value in toml_it]
        return True

    def load_(self, cfile=str('view/core/avantar.toml')):
        import tomlib
        with open(cfile, "r") as avt:
            tom_obj = dict(tomlib.loads(avt.read()))
            self.parse_(tom_obj)
            # print("self.assets", self.assets)
        self.start_game_from_root_element()
        return True

    def mark(self, coord):
        self.rosa.elt.text = coord
    def start_game_from_root_element(self):
        self.rosa = self.vito.Sprite("https://imgur.com/odmJe4Z.jpg", w=30, h=30, cena=self.vito.INV.cena)
        self.vito.INV.bota(self.rosa)
        self.assets["ROOT"].vai() if "ROOT" in self.assets else None
        self.mark("0.0")


class Main:
    def __init__(self, br):
        # from pathlib import PurePath
        # y = [[l for l in k] for k in x]
        # y= dict(x)
        br.template("_tt_").render(titulo="A V A N T A R 🐧")
        self.teclemmino = Teclemmino(br)
        self.br = br

    def load(self, cfile=str('avantar.toml')):
        _ = cfile
        self.teclemmino.load_()


def main(br):
    Main(br).load()


if __name__ == '__main__':
    unittest.main()