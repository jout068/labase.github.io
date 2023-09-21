#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""Game criado usando a interface declarativa Teclemmino.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    23.09
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
LOG_LEVEL = 1
IMGSIZE, IMG_HEIGHT = f"{32 * W}px", f"{4 * H}px"
class Log:
    def __init__(self, min_level=LOG_LEVEL):
        self.min_level =  min_level
    def log(self, level, *args):
        print(*args) if level > self.min_level else None
LG = Log(3)

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
                LG.log(2,"Folha", dimensions)
                # dimensions = [4,4]
                self.dim = d = ntp("Dimensions", "dx dy")(*dimensions)
                self.img = img
                # self.style = {"max-width": f"{d.dx * 100}%", "max-height": f"{d.dy * 100}%"}
                self.style = {"background-size": f"{d.dx * 100}% {d.dy * 100}%"}

            def get_image(self, index):
                index = int(index)
                position = f"{index % self.dim.dx * 100}% {index // self.dim.dx * 100}%"
                # self.style["background-position"] = position
                self.style.update(**{"backgroundPosition": position})
                return dict(img_=self.img, style_=self.style, dim_=self.dim)

        class Sprite(vito.Elemento):
            def __init__(self, img="", vai=None, style=NDCT, tit="", alt="",
                         x=0, y=0, w=100, h=100, o=1, texto='', foi=None, sw=100, sh=100, b=0, s=1,
                         cena="", score=NDCT, drag=False, drop=NDCT, tipo="100% 100%", **kwargs):
                _style = style
                foi = foi() if  callable(foi) else foi
                _ = score, drag, drop, tipo
                img_, _style, _dim = [v for v in img.values()] if isinstance(img, dict) else (img, {}, D11)
                style = dict(width=f"{w}px", height=f"{h}px", overflow="hidden", filter=f"blur({b}px)", scale=s)
                style.update(**_style)
                style.update(**{"background-image": f"url({img_})"})
                # noinspection PyCallingNonCallable
                cena = cena() if callable(cena) else cena
                LG.log(3,"Sprite(vito.Elemento) ⇒", img, foi, cena)

                super().__init__(img=img, vai=vai, tit=tit, alt=alt,
                                 x=x, y=y, w=w, h=h, o=o, texto=texto, foi=foi,
                                 style=style, cena=cena, tipo=f"{sw}px {sh}px",
                                 **kwargs)

                if img_.startswith("*"):
                    icon = teclemmino.I(Class=img[1:], style={"position": "relative", "color": "grey"})
                    _ = self.elt <= icon
                self._texto = Texto(texto, foi=self._foi) if texto else None
                self.vai = self._texto.vai if texto else self.vai
                self.o = o

            def _do_foi(self):
                _texto = self.texto if self.tit else self.title  # else CORRECT.format(self.tit)
                self.vai = Texto(_texto, self.cena).vai
                LG.log(3,_texto, self.vai)

        class CenaSprite(vito.Cena):
            def __init__(self, img, index=-1, **kwargs):
                style_ = {"background-size": f"{8 * 100}% {8 * 100}%"}

                img_, _style, _dim = [v for v in img.values()] if isinstance(img, dict) else (img, style_, D11)
                # style = dict(width=f"{W}px", height=f"{H}px", overflow="hidden", backgroundImage=f"url({img_})")
                style = dict(width=f"{W}px", height=f"{H}px", overflow="hidden")
                position = f"{index % _dim.dx * 100}% {index // _dim.dx * 100}%"
                _style.update(backgroundPosition=position) if index > 0 else None
                style.update(**_style)
                style.update(**{"background-image": f"url({img_})"})

                super().__init__("", **kwargs)
                self.nome = kwargs["nome"] if "nome" in kwargs else img_

                self.elt.html =""
                self.elt.style = style

        class SpriteLabirinto:
            def __init__(self, img, index=(), **kwargs):
                # from random import sample
                img = img["img_"] if isinstance(img, dict) else img
                dx, dy = self.index= Dim(*index)
                xdx = dx+2
                all_images = list(range(32))
                all_images = all_images*8
                # _index = enumerate([sample(all_images, 4)  for _ in range(dx*dy)])
                _index = enumerate([all_images[ix*4:ix*4+4]  for ix in range(dx*dy)])
                # self.salas = salas if salas else self.build_rooms
                _name = kwargs["nome"]
                _salas = [teclemmino.sprite_sala(f"{_name}zz{ii}",img=img, index=ix) for ii, ix in _index]
                self.matrix : List[SpriteSala]
                self.matrix = [None]* xdx
                _matrix = [[None]+ _salas[ix:ix+self.index.dx]+[None] for ix in range(0,dx*dy,dx)]+[[None]*xdx]
                _ = [self.matrix.extend(row) for row in _matrix]
                LG.log(4, "SpriteLabirinto", img, self.matrix)
                self.lb()

            # noinspection PyUnresolvedReferences
            def lb(self):
                dx, dy = self.index
                xdx = dx+2
                winds = [-xdx,1,xdx,-1]
                for index_sala in range(xdx+1,xdx+xdx*dy-1):
                    for wind, winder in enumerate(winds):
                        print("for wind, winder ", index_sala+winder, len(self.matrix))
                        origin , destination = self.matrix[index_sala], self.matrix[index_sala+winder]
                        if origin and destination:
                            origin.cenas[wind].portal(N=destination.cenas[wind])
                            counter_wind = (wind + 2) % 4
                            destination.cenas[counter_wind].portal(N=origin.cenas[counter_wind])

        class SpriteSala(vito.Salao):
            def __init__(self, n=NADA, l=NADA, s=NADA, o=NADA, img=None, index=(), sid=None, **kwargs):
                # _salas = [vito.CenaSprite(img, ix) for ix in index]
                _name = kwargs["nome"]
                _salas = [teclemmino.cena(f"{_name}zz{ii}",img=img, index=ix) for ii, ix in enumerate(index)]


                self.cenas = _salas if _salas else [n, l, s, o]
                self.nome = sid
                _ = kwargs
                self.p()

                LG.log(4, sid, kwargs, _salas, self.norte, teclemmino.assets)
            def vai(self, *_):
                self.norte.vai()

        class Texto:
            DOIT = True

            def __init__(self, tit="", txt="", cena=NADA, foi=None, nome=None, **kwargs):
                def dom(exi=None, mod=None):
                    d, f, a, i, s, h, h1 = list(teclemmino.tag_one)
                    p, b, hd, sc, fm, fs, ip, lg, lb, ft = list(teclemmino.tag_two)
                    card = d(
                        d(hd(p(tit, Class="modal-card-title") +
                             (closer := b(Class="delete", id=exi, ariaLabel="close")), Class="modal-card-head") +
                          sc(d(fm(
                              fs(lg(txt)),
                              Class="form-horizontal"), Class="content"), Class="modal-card-body"),
                          Class="modal-card"),
                        Class="modal", id=mod)
                    closer.bind("click", self.close_modal)
                    return card

                self.cena = cena
                self.kwargs = kwargs
                self.esconde = foi if foi else self.esconde
                self.tit, self.txt, self.nome = tit, txt, nome
                self.modal = dom("modal_closer_", "modal_popup_")
                self.deploy()

            def deploy(self, document=None):
                #print("deploy", document)
                document = document or teclemmino.vito.document
                _ = document <= self.modal
                # noinspection PyAttributeOutsideInit
                self.deploy = lambda *_: None

            def close_modal(self, ev):
                ev.stopPropagation()
                ev.preventDefault()
                self.esconde()
                self.modal.classList.remove('is-active')

            def esconde(self):
                ...

            def mostra(self):  # , tit="", txt="", act=None, **kwargs):
                self.deploy()
                self.modal.classList.add('is-active')

            def vai(self, ev=NoEv()):
                ev.stopPropagation()
                ev.stopPropagation()
                self.mostra()  # self.tit, self.txt, act=self.esconde)
                return False

        self.vito = vito
        self.assets = {}
        self.last = {}
        self.classes = (CenaSprite, Sprite, SpriteSala, Texto, Folha, SpriteLabirinto)
        self.cmd = self.vito_element_builder(vito, self.classes)

    def vito_element_builder(self, v, classes):
        v.CenaSprite, v.Sprite, v.SpriteSala, v.Textor, self.vito.Folha, v.SpriteLabirinto = classes
        builder = [self.cena, self.elemento, self.texto,
                   self.sprite_sala, self.folha, self.valor, self.icon, self.sprite_labirinto]
        return {k: v for k, v in zip(['c', 'e', 't', 's', 'f', 'v', "i", "l"], builder)}

    def cena(self, asset, **kwargs):
        self.assets[asset] = result = self.vito.CenaSprite(nome=asset, **kwargs)
        self.last = asset
        LG.log(3,"Vito ⇒ cena", asset, kwargs)
        return result

    def sprite_labirinto(self, asset, **kwargs):
        self.assets[asset] = self.vito.SpriteLabirinto(nome=asset, **kwargs)

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
        self.assets[asset] = t = self.vito.Textor(nome=asset, one=self.tag_one, two=self.tag_two, **kwargs)
        t.deploy(self.vito.document.body)
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
        LG.log(4,"icon:->", asset, item, index, value)
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

    def load_(self, cfile=str('view/_core/avantar.toml')):
        import toml
        with open(cfile, "r") as avt:
            tom_obj = dict(toml.loads(avt.read()))
            self.parse_(tom_obj)
            # print("self.assets", self.assets)
        self.start_game_from_root_element()
        return True

    def start_game_from_root_element(self):
        self.assets["ROOT"].vai() if "ROOT" in self.assets else None


class Main:
    def __init__(self, br):
        # from pathlib import PurePath
        # y = [[l for l in k] for k in x]
        # y= dict(x)
        br.template("_tt_").render(titulo="A V A N T A R 🐧")
        self.teclemmino = Teclemmino(br)
        self.br = br

    def load(self, cfile=str('view/_core/avantar.toml')):
        _ = cfile
        self.teclemmino.load_()


def main(br):
    Main(br).load()


if __name__ == '__main__':
    unittest.main()
