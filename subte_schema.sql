--
-- PostgreSQL database dump
--

-- Dumped from database version 11.8 (Ubuntu 11.8-1.pgdg18.04+1)
-- Dumped by pg_dump version 11.8 (Ubuntu 11.8-1.pgdg18.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: estaciones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.estaciones (
    id smallint NOT NULL,
    nombre character varying(100),
    linea character(1),
    long real,
    lat real
);


ALTER TABLE public.estaciones OWNER TO postgres;

--
-- Name: pases; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pases (
    estacion character varying(50) COLLATE pg_catalog."es_AR",
    linea character(1),
    total integer,
    fecha date,
    hora integer,
    anio smallint,
    mes smallint,
    dia_mes smallint,
    dia_semana smallint,
    dia_anio smallint
);


ALTER TABLE public.pases OWNER TO postgres;

--
-- Name: estaciones estaciones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estaciones
    ADD CONSTRAINT estaciones_pkey PRIMARY KEY (id);


--
-- Name: ix_station; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_station ON public.pases USING btree (estacion);


--
-- Name: ix_time; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_time ON public.pases USING btree (anio, mes, dia_mes, dia_semana, hora);


--
-- PostgreSQL database dump complete
--

