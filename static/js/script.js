/*
* Title: Rempeflix
* Author: 011h
* Template: Netflix
* Version: 0.1
* Copyright 2022 011h
* Url: https://www.rompeflix.ml



Content table
--------------
1. Custom scripts
2. Bootstrap scripts

/* ----- 1. Custom scripts ----- */

function correo(usuario,dominio) {
	return usuario + "@" + dominio
}

function enlace_correo(a, b) {
	document.write("<a href='mailto:" + correo(a,b) + "'>")
}