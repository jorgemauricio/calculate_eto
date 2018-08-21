#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#######################################
# Script para calcular la variable ETO
# Author: Jorge Mauricio
# Email: jorge.ernesto.mauricio@gmail.com
# Date: Created on Thu Sep 28 08:38:15 2017
# Version: 1.0
#######################################
"""

# librerías
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from math impor exp
import math
matplotlib.style.use('seaborn')

def main():
    pass


def latitud_en_radianes(latitud):
    """
    calcula la latitud en radianes
    param: latitud: latitud de la estación
    """
    return (math.pi * latitud)/180

def presion_atmosferica(altitud):
    """
    calcula la presión atmosferica en base a la altitud kPa
    param: altitud: altitud de la estación
    """
    return 101.3*((293-0.0065*altitud)/293)**(5.26)

def calor_latente(tmed):
    """
    calcula el calor latente en base a la temperatura media MJ/kg
    param: tmed: temperatura media
    """
    return 2.501-(2.361*tmed/1000)

def constante_sicrometrica(p_atmosferica, c_latente):
    """
    calcula la constante sicrométrica en kPa/ºC
    param: p_atmosferica : presión atmosferica
    param: c_latente     : calor latente
    """
    return (1.0113/(1000*0.622))*p_atmosferica/c_latente

def presion_vapor_tmin(tmin):
    """
    calcula la presión del vapor en saturación a la temperatura mínima kPa
    param: tmin : temperatura mínima
    """
    return 0.6108*math.exp(17.27*tmin/(tmin+237.3))

def presion_vapor_tmax(tmax):
    """
    calcula la presión del vapor en saturación a la temperatura máxima kPa
    param: tmax : temperatura máxima
    """
    return 0.6108*math.exp(17.27*tmax/(tmax+237.3))

def presion_vapor_tmed(tmed):
    """
    calcula la presión del vapor en saturación a la temperatura media kPa
    param: tmed : temperatura media
    """
    return 0.6108*math.exp(17.27*tmed/(tmed+237.3))

def presion_media_vapor(presion_tmax, presion_tmin):
    """
    calcula la presion media del vapor en saturación kPa
    param: presion_tmax : presión del vapor en saturación a la tmax
    param: presion_tmin : presión del vapor en saturación a la tmin
    """
    return (presion_tmax+presion_tmin)/2

def pendiente_curva_presion_vapor(tmed, presion_tmed):
    """
    calcula la prendiente de la curva de la presión de vapor en saturación en
    kPa/ºC
    param: presion_tmed : presion del vapor en saturación a la tmed
    param: tmed         : temperatura media
    """
    return 4098*presion_tmed/(tmed+237.3)**2

def constante_sicrometrica_modificada(c_sicometrica, vv_promedio):
    """
    calcula la constante sicrométrica modificada en kPa/ºC
    param: c_sicometrica :  constante sicrométrica
    param: vv_promedio   :  velocicad del viento promedio
    """
    return c_sicometrica*(1+0.34*vv_promedio)

def presion_vapor_real(hr_max, hr_min, presion_tmax, presion_tmin):
    """
    calcula la presión de vapor real en kPa
    param: hr_max          : humedad relativa máxima
    param: hr_min          : humedad relativa mínima
    param: presion_tmax    : presión del vapor en saturación a la tmax
    param: presion_tmin    : presión del vapor en saturación a la tmin
    """
    return (0.5*presion_tmin*hr_max/100)+(0.5*presion_tmax*hr_min/100)

def termino_aerodinamico(tmed, vv_promedio, c_sicometrica, p_media_vapor, pendiente_curva, c_sicometrica_modificada, p_vapor_real):
    """
    calcula el término aerodinámico de la ecuación de PM en mm/día
    param: tmed                     : temperatura media
    param: vv_promedio              :  velocidad del viento promedio
    param: c_sicometrica            :  constante sicométrica
    param: p_media_vapor            :  presión media del vapor en saturación
    param: pendiente_curva          : pendiente de la curva de la presión de vapor en saturación
    param: c_sicometrica_modificada : constante sicométrica modificada
    param: p_vapor_real             : presion de vapor real
    """
    return (c_sicometrica*900*vv_promedio*(p_media_vapor-p_vapor_real))/((pendiente_curva+c_sicometrica_modificada)*(tmed+273.16))

def numero_calendario_juliano(anio, mes, dia):
    """
    calcular el día en calendario juliano
    param: anio : año
    param: mes  : mes
    param: dia  : día
    """
    return int(275*mes/9)-(int((9+mes)/12))*(1-int((anio+2-4*int(anio/4))/3))+dia-30

def distancia_relativa_tierra_sol(dia_juliano):
    """
    calcula la distancia relativa inversa entre la tierra y el sol en radianes
    param: dia_juliano : Número del día del año en el calendario juliano
    """
    return 1+0.033*math.cos(2*math.pi*dia_juliano/365)

def declinacion_solar(dia_juliano):
    """
    calcula la declinación solar en radianes
    param: dia_juliano : Número dle día del año en el calendario juliano
    """
    return 0.409*math.sin(2*math.pi*dia_juliano/365-1.39)

def angulo_declinacion_solar(d_solar, latitud_radianes):
    """
    calcula el angulo de declinación solar en radianes
    param: d_solar          : declinación solar
    param: latitud_radianes : latitud en radianes
    """
    return math.acos(-math.tan(latitud_radianes)*math.tan(d_solar))

def radiacion_extraterrestre(latitud_radianes, dist_tierra_sol, d_solar, a_declinacion_solar):
    """
    calcula la radiación extraterrestre en MJ/m2 y día
    param: d_solar             : declinación solar
    param: latitud_radianes    : latitud en radianes
    param: dist_tierra_sol     : distancia relativa inversa entre la tierra y el sol
    param: a_declinacion_solar : angulo de declinación solar
    """
    return (118.08/math.pi)*dist_tierra_sol*(a_declinacion_solar*math.sin(latitud_radianes)*math.sin(d_solar)+math.cos(d_solar)*math.cos(d_solar)*math.sin(a_declinacion_solar))

def radiacion_solar(radiacion):
    """
    calcula la radiación solar o de onda corta en MJ/m2 y día
    param: radiacion: radiación global
    """
    return radiacion*0.0864

def radiacion_solar_neta(r_solar):
    """
    calcula la radiación neta solar o de onda corta en MJ/m2 y día
    param: r_solar: radiación solar o de onda corta
    """
    return (1-0.23)*r_solar

def radiacion_solar_cielo_despejado(altitud, r_extraterrestre):
    """
    calcula la radiación solar con cielo despejado en MJ/m2 y día
    param: altitud          : altitud
    param: r_extraterrestre : radiación extraterrestre
    """
    return(0.75+2*10**-5*altitud)*r_extraterrestre

def radiacion_solar_onda_larga(tmax, tmin, p_vapor_real, r_solar, r_solar_cielo_despejado):
    """
    calcula la radiación neta de onda larga saliente en MJ/m2 y día
    param: tmax                    : temperatura máxima
    param: tmin                    : temperatura mínima
    param: p_vapor_real            : presión de vapor real
    param: r_solar                 : radiación solar o de onda corta
    param: r_solar_cielo_despejado : radiación solar con cielo despejado
    """
    return 4.903*(10**-9)*((tmin+273.16)**4)*(0.34-0.14*math.sqrt(p_vapor_real))*(1.35*(r_solar/r_solar_cielo_despejado)-0.35)/2

def radiacion_neta(r_onda_corta,r_onda_larga):
    """
    calcula la radiación neta en MJ/m2 y día
    param: r_onda_corta : radiación neta solar o de onda corta
    param: r_onda_larga : radiación neta de onda larga saliente
    """
    return r_onda_corta - r_onda_larga

def termino_radiacion(pendiente_curva, c_sicometrica_modificada, r_neta):
    """
    calcular término de radiación de la ecuación de PM en mm/día
    param: pendiente_curva          : pendiente de la curva de la presión de vapor en saturación
    param: c_sicometrica_modificada : constante sicrométrica modificada
    param: r_neta                   : radiación neta
    """
    return 0.408*pendiente_curva*r_neta/(pendiente_curva+c_sicometrica_modificada)

def evapotranspiracion(aerodinamico, radiacion_ecuacion):
    """
    calcula la evapotranspiración de referencia según PM FAO
    param: aerodinamico       : término aerodinámico de la ecuación de PM en mm/día
    param: radiacion_ecuacion : término de radiación de la ecuación de PM en mm/día
    """
    return radiacion_ecuacion + aerodinamico

if __name__ == '__main__':
    main()
