#!/usr/bin/python
# -*- coding: UTF-8 -*-

#Estas duas linhas permitem escrever
#em português dentro do código, colocando 
#acentos e letras não disponíveis em inglês.
#para isso usamos a formatação UTF-8

#######

###############
#Bibliotecas  e Funcões do python 

import numpy as np

from   netCDF4 import Dataset,num2date,date2num

import datetime as dt

import matplotlib.pyplot as plt

#Funções do metpy
#Calculo
import metpy.calc  as calc
#Plotes
from   metpy.plots import  SkewT,add_metpy_logo
#Unidades 
from   metpy.units import units
#Constantes
#import metpy.constants as mc 
from metpy.constants import * 


############################
#1) Definir o arquivo a ser lido  
#Nome do arquivo a ser carregado.
nomedoarquivo  = './ncfiles/LES_BOMEX.nc'

#letura do arquivo netcdf
nc_fid = Dataset(nomedoarquivo, 'r')

#2) Extrair as varíaveis a ser usadas. 
############################
#Independentes 
time    = nc_fid.variables['time'][:]
lat     = nc_fid.variables[ 'lat'][:]  
lon     = nc_fid.variables[ 'lon'][:]
z       = nc_fid.variables[ 'z'  ][:]  

#Dependentes 
press   = nc_fid.variables[ 'lev' ][:]
T       = nc_fid.variables[ 'TABS'][:]
rh      = nc_fid.variables[ 'RELH'][:]
q       = nc_fid.variables[ 'QT'  ][:]
mse     = nc_fid.variables[ 'MSE' ][:]  
massflux= nc_fid.variables[ 'MCUP'][:]  

############################
#3)Criação do vetor temporal. 
data_units   ='days  since 2013-12-31T00:00:00 +00:00:00'
data_calendar='gregorian'
data_calendar='standard'

#datas        = num2date(time,units=data_units, calendar=data_calendar)

offset = dt.timedelta(hours=0)
datas  = [dt.datetime(2013, 12, 31,0,0,0) + dt.timedelta(hours=t*24) - offset\
           for t in time]

#Minha data  
#2014, 6, 21, 1, 40, 30, 17578
my_date=dt.datetime(2014, 6, 21, 1, 1,30,87891)

index=datas.index(my_date)
#exit()

#index=0
#for i in range(0,len(datas)): 
#    #print('index=%s'%(i),my_date)
#    if(my_date==datas[i]):
#        print(' A data procurada está no index=%s'%(i),my_date)
#        index=i
#        break
#    if(i==len(datas)-1 and index==0):
#        print('A data procurada não se encontra nos dados')
#        exit()


############################
#Definindo variavel com unidades.
g=9.81*units("m/s^2")

#3) Colocar as unidades as variaveis que serão usadas. 

pu  = units.Quantity(press,"mbar")
Tu  = units.Quantity(T,"K")
rhu = units.Quantity(rh,"percent")
qu  = units.Quantity(q,"g/kg")


############################
#4)Definir constantes a ser usadas.

#Constante dos gases ideias  
R=dry_air_gas_constant

#Calor específico ar  
cp=dry_air_spec_heat_press

#Massa específica
rho=dry_air_density_stp

rho=rho.to('g/m^3')


############################

p_0=1000
c_p=1004
R_0=287.04
theta_u=T*(p_0/press)**(R_0/c_p)

theta = calc.potential_temperature(pu, Tu)


#print(theta_u[0,:])
#print(theta[0,:])

#exit()

#5)Usar funcões do metpy para calcular diferentes propriedades. 

#Potential temperature
theta = calc.potential_temperature(pu, Tu)

#Temperatura de ponto de horvalio 
Td    = calc.dewpoint_from_relative_humidity(Tu, rhu)

# Temperatura da parcela, esfriamento adiabatico. 
Ta    = calc.parcel_profile(pu, Tu[index,0], Td[index,0]).to('degC')

cape,cin=calc.cape_cin(pu, Tu[index,:],Td[index,:], Ta, which_lfc='bottom', which_el='top')


#4) Fazer o grafico.
fig = plt.figure(figsize=(9,9))
skew = SkewT(fig, rotation=45)

# Plot the data using normal plotting functions, in this case using
# log scaling in Y, as dictated by the typical meteorological plot.
skew.plot(pu, Tu[index,:], 'r')
skew.plot(pu, Td[index,:], 'g')

lcl_p, lcl_t = calc.lcl(pu[0] , Tu[index,0], Td[index,0])

skew.plot(pu   , Ta[:], 'b')
skew.plot(lcl_p, lcl_t, 'ko', markerfacecolor='black')

# Shade areas of CAPE and CIN
skew.shade_cin(pu , Tu[index,:], Ta, Td[index,:], color='green')
skew.shade_cape(pu, Tu[index,:], Ta)

skew.ax.set_ylim(1000, 700)
skew.ax.set_xlim(0, 30)
skew.ax.set_xlabel(f'Temperature ({Ta.units:~P})')
skew.ax.set_ylabel(f'Pressure ({pu.units:~P})')

# Add the relevant special lines
skew.plot_dry_adiabats()
skew.plot_moist_adiabats()
skew.plot_mixing_lines()
#add_metpy_logo(fig, 115, 100)


plt.show()


exit()





