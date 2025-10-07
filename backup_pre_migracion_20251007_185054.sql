--
-- PostgreSQL database dump
--

\restrict wAikh5DCMGMzufow2VaWtLTA0pQdPcw36hepsRDH8POWVjtIBC5fcUZagFHdK7v

-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: condiciones_diente; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.condiciones_diente (
    id uuid DEFAULT extensions.uuid_generate_v4() NOT NULL,
    odontograma_id uuid,
    diente_id uuid NOT NULL,
    tipo_condicion character varying(50) NOT NULL,
    caras_afectadas text[] DEFAULT ARRAY[]::text[],
    severidad character varying(20) DEFAULT 'leve'::character varying,
    descripcion text,
    observaciones text,
    hallazgos_clinicos text,
    material_utilizado character varying(100),
    color_material character varying(50),
    fecha_tratamiento date,
    tecnica_utilizada character varying(100),
    tiempo_tratamiento interval,
    estado character varying(20) DEFAULT 'actual'::character varying,
    requiere_seguimiento boolean DEFAULT false,
    fecha_proximo_control date,
    fecha_registro timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    registrado_por uuid,
    intervencion_origen_id uuid,
    posicion_x numeric(5,2),
    posicion_y numeric(5,2),
    color_hex character varying(7) DEFAULT '#FFFFFF'::character varying,
    forma_renderizado character varying(20) DEFAULT 'default'::character varying,
    anotaciones_detalladas jsonb DEFAULT '{}'::jsonb,
    imagenes_referencia text[],
    documentos_adjuntos text[],
    CONSTRAINT condiciones_diente_estado_check CHECK (((estado)::text = ANY ((ARRAY['planificado'::character varying, 'en_tratamiento'::character varying, 'actual'::character varying, 'historico'::character varying])::text[]))),
    CONSTRAINT condiciones_diente_severidad_check CHECK (((severidad)::text = ANY ((ARRAY['leve'::character varying, 'moderada'::character varying, 'severa'::character varying])::text[]))),
    CONSTRAINT condiciones_diente_tipo_condicion_check CHECK (((tipo_condicion)::text = ANY ((ARRAY['sano'::character varying, 'caries'::character varying, 'obturacion'::character varying, 'corona'::character varying, 'puente'::character varying, 'implante'::character varying, 'ausente'::character varying, 'extraccion_indicada'::character varying, 'endodoncia'::character varying, 'protesis'::character varying, 'fractura'::character varying, 'mancha'::character varying, 'desgaste'::character varying, 'sensibilidad'::character varying, 'movilidad'::character varying, 'impactado'::character varying, 'en_erupcion'::character varying, 'retenido'::character varying, 'supernumerario'::character varying, 'otro'::character varying])::text[])))
);


ALTER TABLE public.condiciones_diente OWNER TO postgres;

--
-- Name: odontograma; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.odontograma (
    id uuid DEFAULT extensions.uuid_generate_v4() NOT NULL,
    paciente_id uuid NOT NULL,
    fecha_creacion timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    odontologo_id uuid NOT NULL,
    version integer DEFAULT 1,
    es_version_actual boolean DEFAULT true,
    version_anterior_id uuid,
    motivo_nueva_version text,
    tipo_odontograma character varying(20) DEFAULT 'adulto'::character varying,
    notas_generales text,
    observaciones_clinicas text,
    template_usado character varying(50) DEFAULT 'universal'::character varying,
    configuracion jsonb DEFAULT '{}'::jsonb,
    estadisticas_condiciones jsonb DEFAULT '{}'::jsonb,
    CONSTRAINT chk_odontograma_version CHECK ((version > 0)),
    CONSTRAINT odontograma_tipo_odontograma_check CHECK (((tipo_odontograma)::text = ANY ((ARRAY['adulto'::character varying, 'pediatrico'::character varying, 'mixto'::character varying])::text[])))
);


ALTER TABLE public.odontograma OWNER TO postgres;

--
-- Name: pacientes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pacientes (
    id uuid DEFAULT extensions.uuid_generate_v4() NOT NULL,
    numero_historia character varying(20) NOT NULL,
    primer_nombre character varying(50) NOT NULL,
    segundo_nombre character varying(50),
    primer_apellido character varying(50) NOT NULL,
    segundo_apellido character varying(50),
    tipo_documento character varying(20) DEFAULT 'CI'::character varying,
    numero_documento character varying(20) NOT NULL,
    fecha_nacimiento date,
    edad integer,
    genero character varying(10),
    celular_1 character varying(20),
    celular_2 character varying(20),
    email character varying(100),
    direccion text,
    ciudad character varying(100),
    departamento character varying(100),
    ocupacion character varying(100),
    estado_civil character varying(20),
    contacto_emergencia jsonb DEFAULT '{}'::jsonb,
    alergias text[],
    medicamentos_actuales text[],
    condiciones_medicas text[],
    antecedentes_familiares text[],
    fecha_registro timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    registrado_por uuid,
    activo boolean DEFAULT true,
    observaciones text,
    CONSTRAINT chk_pacientes_celular1 CHECK (((celular_1 IS NULL) OR ((celular_1)::text ~ '^[\+]?[\d\s\-\(\)]{7,20}$'::text))),
    CONSTRAINT chk_pacientes_celular2 CHECK (((celular_2 IS NULL) OR ((celular_2)::text ~ '^[\+]?[\d\s\-\(\)]{7,20}$'::text))),
    CONSTRAINT chk_pacientes_documento CHECK (((numero_documento)::text ~ '^\d{6,20}$'::text)),
    CONSTRAINT chk_pacientes_edad CHECK (((edad IS NULL) OR ((edad >= 0) AND (edad <= 150)))),
    CONSTRAINT chk_pacientes_email CHECK (((email IS NULL) OR ((email)::text ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'::text))),
    CONSTRAINT pacientes_genero_check CHECK (((genero)::text = ANY ((ARRAY['masculino'::character varying, 'femenino'::character varying, 'otro'::character varying])::text[]))),
    CONSTRAINT pacientes_tipo_documento_check CHECK (((tipo_documento)::text = ANY ((ARRAY['CI'::character varying, 'Pasaporte'::character varying])::text[])))
);


ALTER TABLE public.pacientes OWNER TO postgres;

--
-- Data for Name: condiciones_diente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.condiciones_diente (id, odontograma_id, diente_id, tipo_condicion, caras_afectadas, severidad, descripcion, observaciones, hallazgos_clinicos, material_utilizado, color_material, fecha_tratamiento, tecnica_utilizada, tiempo_tratamiento, estado, requiere_seguimiento, fecha_proximo_control, fecha_registro, registrado_por, intervencion_origen_id, posicion_x, posicion_y, color_hex, forma_renderizado, anotaciones_detalladas, imagenes_referencia, documentos_adjuntos) FROM stdin;
\.


--
-- Data for Name: odontograma; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.odontograma (id, paciente_id, fecha_creacion, fecha_actualizacion, odontologo_id, version, es_version_actual, version_anterior_id, motivo_nueva_version, tipo_odontograma, notas_generales, observaciones_clinicas, template_usado, configuracion, estadisticas_condiciones) FROM stdin;
4f109e88-9074-4d8d-806d-f411d0984414	dcc1c80b-e21f-4f76-b0b9-9c2f52635305	2025-09-25 10:15:48.882134+00	2025-09-25 10:15:48.882134+00	3208d456-85fa-4adf-96d6-4b3962844527	1	t	\N	Odontograma inicial	adulto	Odontograma inicial con 32 dientes marcados como sanos	Estado inicial del paciente	universal	{}	{}
9d64b963-c23a-4a39-b8a0-1cdc03632014	05f72d6b-db89-428f-87ae-41f4abffe460	2025-10-01 18:53:17.394017+00	2025-10-01 18:53:17.394017+00	3208d456-85fa-4adf-96d6-4b3962844527	1	t	\N	Odontograma inicial	adulto	Odontograma inicial con 32 dientes marcados como sanos	Estado inicial del paciente	universal	{}	{}
8d0f49ee-b1ec-4af8-afae-e484e56e93b1	546bb212-d549-492c-a5c1-803d43f69f00	2025-09-21 00:00:00+00	2025-09-25 00:53:32.5093+00	c801c016-ada5-4533-96ef-a7ddeb911334	1	f	\N	Odontograma inicial del paciente	adulto	Odontograma versión 1 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-21	universal	{}	{}
2fd97641-5a52-4dff-8165-f86d94bababe	546bb212-d549-492c-a5c1-803d43f69f00	2025-09-24 00:00:00+00	2025-09-25 00:53:32.5093+00	c801c016-ada5-4533-96ef-a7ddeb911334	2	f	8d0f49ee-b1ec-4af8-afae-e484e56e93b1	Seguimiento post-tratamiento	adulto	Odontograma versión 2 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-24	universal	{}	{}
fa53d36a-dc8d-47b5-9400-d842a459aef8	546bb212-d549-492c-a5c1-803d43f69f00	2025-09-23 15:22:43.501645+00	2025-09-25 00:53:32.5093+00	3208d456-85fa-4adf-96d6-4b3962844527	1	f	\N	Odontograma inicial	adulto	Odontograma inicial con 32 dientes marcados como sanos	Estado inicial del paciente	universal	{}	{}
b69a27ba-75d6-488b-902e-b3a3785460c6	546bb212-d549-492c-a5c1-803d43f69f00	2025-09-14 00:00:00+00	2025-09-14 00:00:00+00	c801c016-ada5-4533-96ef-a7ddeb911334	3	t	2fd97641-5a52-4dff-8165-f86d94bababe	Actualización tras intervención odontológica	adulto	Odontograma versión 3 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-14	universal	{}	{"total_condiciones": 0, "condiciones_por_tipo": null}
0aad9fba-7bd5-4617-a01d-403382f94f9d	6948e9de-290c-4781-813e-0d42ecbc88c7	2025-09-17 00:00:00+00	2025-09-25 00:53:32.744828+00	c801c016-ada5-4533-96ef-a7ddeb911334	1	f	\N	Odontograma inicial del paciente	adulto	Odontograma versión 1 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-17	universal	{}	{}
20f65a56-7e7d-4eff-8d27-8402e995976b	6948e9de-290c-4781-813e-0d42ecbc88c7	2025-09-23 15:22:43.599134+00	2025-09-25 00:53:32.744828+00	3208d456-85fa-4adf-96d6-4b3962844527	1	f	\N	Odontograma inicial	adulto	Odontograma inicial con 32 dientes marcados como sanos	Estado inicial del paciente	universal	{}	{}
fad4de97-d4f0-41f1-8ef7-88c960b2f5ef	6948e9de-290c-4781-813e-0d42ecbc88c7	2025-09-11 00:00:00+00	2025-09-11 00:00:00+00	c801c016-ada5-4533-96ef-a7ddeb911334	2	t	0aad9fba-7bd5-4617-a01d-403382f94f9d	Control de rutina - Actualización condiciones	adulto	Odontograma versión 2 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-11	universal	{}	{"total_condiciones": 0, "condiciones_por_tipo": null}
83bde86f-44c4-4a70-8cf5-e6bd8b15a864	cbe19a5c-dfc8-4c4b-9342-7f1b2168ad50	2025-09-14 00:00:00+00	2025-09-25 00:53:33.23579+00	c801c016-ada5-4533-96ef-a7ddeb911334	1	f	\N	Odontograma inicial del paciente	adulto	Odontograma versión 1 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-14	universal	{}	{}
165ecbc0-2d15-4b05-b31e-93b1257144d3	cbe19a5c-dfc8-4c4b-9342-7f1b2168ad50	2025-09-22 00:00:00+00	2025-09-25 00:53:33.23579+00	c801c016-ada5-4533-96ef-a7ddeb911334	2	f	83bde86f-44c4-4a70-8cf5-e6bd8b15a864	Control de rutina - Actualización condiciones	adulto	Odontograma versión 2 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-22	universal	{}	{}
2ae0a590-c747-4f7b-8d2c-1e3b404d9dc3	cbe19a5c-dfc8-4c4b-9342-7f1b2168ad50	2025-10-04 00:00:00+00	2025-09-25 00:53:33.23579+00	c801c016-ada5-4533-96ef-a7ddeb911334	3	f	165ecbc0-2d15-4b05-b31e-93b1257144d3	Registro de nuevas condiciones detectadas	adulto	Odontograma versión 3 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-10-04	universal	{}	{}
1d52d9a5-3d62-4b7c-8e5e-16f9db9990bb	50b055af-40e4-4378-bb97-7d332af58e9c	2025-09-23 15:22:43.785804+00	2025-09-25 00:53:33.45919+00	3208d456-85fa-4adf-96d6-4b3962844527	1	f	\N	Odontograma inicial	adulto	Odontograma inicial con 32 dientes marcados como sanos	Estado inicial del paciente	universal	{}	{}
b8fbc05a-a6a2-4ea3-aa25-70c62e2a5af7	e04e892e-5e91-422a-99c9-3987302ee7b5	2025-09-23 15:22:43.871459+00	2025-09-25 00:53:33.691986+00	3208d456-85fa-4adf-96d6-4b3962844527	1	f	\N	Odontograma inicial	adulto	Odontograma inicial con 32 dientes marcados como sanos	Estado inicial del paciente	universal	{}	{}
5fe50cc0-c0af-4ff8-ad0a-b9cb21145ad1	491abeaf-7449-455e-9484-707626c1aca6	2025-09-23 15:22:43.948413+00	2025-09-25 00:53:33.945565+00	e192130f-9c34-4eb1-9fa4-77f59eef4597	1	f	\N	Odontograma inicial	adulto	Odontograma inicial con 32 dientes marcados como sanos	Estado inicial del paciente	universal	{}	{}
e3c4227c-e985-4e7b-b179-a5a6db6b3489	97cd0017-61a1-406f-afaa-b1906156931b	2025-09-23 15:22:44.02984+00	2025-09-25 00:53:34.211797+00	e192130f-9c34-4eb1-9fa4-77f59eef4597	1	f	\N	Odontograma inicial	adulto	Odontograma inicial con 32 dientes marcados como sanos	Estado inicial del paciente	universal	{}	{}
505fdcf5-d634-4963-a464-4750b892cc14	17190193-78ea-46d2-8a25-bf87a3b86d0f	2025-09-23 15:22:44.10171+00	2025-09-25 00:53:34.562303+00	3208d456-85fa-4adf-96d6-4b3962844527	1	f	\N	Odontograma inicial	adulto	Odontograma inicial con 32 dientes marcados como sanos	Estado inicial del paciente	universal	{}	{}
abea3363-9a17-4fa7-808a-67341692c053	af9a7d81-65d3-4066-8704-99560f29eb4b	2025-09-23 15:22:44.179778+00	2025-09-25 00:53:35.083986+00	e192130f-9c34-4eb1-9fa4-77f59eef4597	1	f	\N	Odontograma inicial	adulto	Odontograma inicial con 32 dientes marcados como sanos	Estado inicial del paciente	universal	{}	{}
f7ab45e4-dd07-4f87-a1ec-f96238699b0a	eaaa81ae-6f30-4a22-a417-a48351f2e92e	2025-09-23 15:22:44.248658+00	2025-09-25 00:53:35.585778+00	3208d456-85fa-4adf-96d6-4b3962844527	1	f	\N	Odontograma inicial	adulto	Odontograma inicial con 32 dientes marcados como sanos	Estado inicial del paciente	universal	{}	{}
c106dae1-6dd3-4531-a070-11baf2d1054d	08b0d19f-df0b-4107-ac85-7a14371759ca	2025-09-23 15:22:44.320225+00	2025-09-25 00:53:36.042097+00	e192130f-9c34-4eb1-9fa4-77f59eef4597	1	f	\N	Odontograma inicial	adulto	Odontograma inicial con 32 dientes marcados como sanos	Estado inicial del paciente	universal	{}	{}
1b1279b0-4b58-4b99-aa35-8fac782f821a	a38d7d6e-a7f8-4674-9686-c18b01e603a4	2025-09-23 15:22:44.399837+00	2025-09-25 00:53:36.473196+00	e192130f-9c34-4eb1-9fa4-77f59eef4597	1	f	\N	Odontograma inicial	adulto	Odontograma inicial con 32 dientes marcados como sanos	Estado inicial del paciente	universal	{}	{}
41212c11-cc4b-4091-830c-068e75fab832	5ca97b83-21de-44f8-a1b3-09870d85cfcf	2025-09-23 15:22:44.478984+00	2025-09-25 00:53:36.815612+00	3208d456-85fa-4adf-96d6-4b3962844527	1	f	\N	Odontograma inicial	adulto	Odontograma inicial con 32 dientes marcados como sanos	Estado inicial del paciente	universal	{}	{}
91fe7624-9414-4519-be57-b1c4b0b3088a	26798f99-329c-4bde-856f-09f08d40b915	2025-09-23 15:22:44.565932+00	2025-09-25 00:53:37.27964+00	3208d456-85fa-4adf-96d6-4b3962844527	1	f	\N	Odontograma inicial	adulto	Odontograma inicial con 32 dientes marcados como sanos	Estado inicial del paciente	universal	{}	{}
17904de6-c268-4d00-88f8-ecf15b3a90d5	377b3c4d-f9b8-4a70-aeb7-00258b9eb69b	2025-09-23 15:22:44.648405+00	2025-09-25 00:53:37.495116+00	e192130f-9c34-4eb1-9fa4-77f59eef4597	1	f	\N	Odontograma inicial	adulto	Odontograma inicial con 32 dientes marcados como sanos	Estado inicial del paciente	universal	{}	{}
1d5af8ab-2438-4508-87ea-45981b88e87a	9ca54413-12b4-4d52-a7fa-e02753992fcf	2025-09-23 15:22:44.709633+00	2025-09-25 00:53:37.922861+00	3208d456-85fa-4adf-96d6-4b3962844527	1	f	\N	Odontograma inicial	adulto	Odontograma inicial con 32 dientes marcados como sanos	Estado inicial del paciente	universal	{}	{}
3de35710-5514-4c2c-b67f-4bd53950420e	404cd152-f753-468e-9bc2-92afb4767ee4	2025-09-23 15:22:44.777357+00	2025-09-25 00:53:38.395033+00	3208d456-85fa-4adf-96d6-4b3962844527	1	f	\N	Odontograma inicial	adulto	Odontograma inicial con 32 dientes marcados como sanos	Estado inicial del paciente	universal	{}	{}
1257653e-dc29-4579-8fb6-f34449332735	cf404971-ef00-4a99-b8cc-f5975505fa19	2025-09-23 15:22:44.846595+00	2025-09-25 00:53:38.694516+00	e192130f-9c34-4eb1-9fa4-77f59eef4597	1	f	\N	Odontograma inicial	adulto	Odontograma inicial con 32 dientes marcados como sanos	Estado inicial del paciente	universal	{}	{}
6b0f96a7-dc3b-4a48-8e20-81bdc33514af	4155558d-98ed-4c03-9fbd-bfc3e2ea7ac7	2025-09-23 15:22:44.911566+00	2025-09-25 00:53:39.171119+00	e192130f-9c34-4eb1-9fa4-77f59eef4597	1	f	\N	Odontograma inicial	adulto	Odontograma inicial con 32 dientes marcados como sanos	Estado inicial del paciente	universal	{}	{}
4e71e8ce-3c84-4d20-bbd3-954a40e87988	5a32b59a-084e-4896-8ad1-516ef7fc57ce	2025-09-23 15:22:44.978575+00	2025-09-25 00:53:39.406593+00	e192130f-9c34-4eb1-9fa4-77f59eef4597	1	f	\N	Odontograma inicial	adulto	Odontograma inicial con 32 dientes marcados como sanos	Estado inicial del paciente	universal	{}	{}
bb1bd40f-b1ab-4bdb-a6cf-1d0591c607f7	cbe19a5c-dfc8-4c4b-9342-7f1b2168ad50	2025-09-23 15:22:43.694301+00	2025-09-25 00:53:33.23579+00	e192130f-9c34-4eb1-9fa4-77f59eef4597	1	f	\N	Odontograma inicial	adulto	Odontograma inicial con 32 dientes marcados como sanos	Estado inicial del paciente	universal	{}	{}
ef4d40f3-f40a-470b-a425-350a27fb81ce	cbe19a5c-dfc8-4c4b-9342-7f1b2168ad50	2025-10-15 00:00:00+00	2025-10-15 00:00:00+00	c801c016-ada5-4533-96ef-a7ddeb911334	4	t	2ae0a590-c747-4f7b-8d2c-1e3b404d9dc3	Evolución del estado dental del paciente	adulto	Odontograma versión 4 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-10-15	universal	{}	{"total_condiciones": 0, "condiciones_por_tipo": null}
d08bf7a9-ced8-4379-a5d7-a23430444c75	50b055af-40e4-4378-bb97-7d332af58e9c	2025-09-04 00:00:00+00	2025-09-25 00:53:33.45919+00	f110064a-846e-4e12-af1c-92ab081d3b94	1	f	\N	Odontograma inicial del paciente	adulto	Odontograma versión 1 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-04	universal	{}	{}
cfa98242-c824-4e91-b702-938307a829fc	50b055af-40e4-4378-bb97-7d332af58e9c	2025-09-12 00:00:00+00	2025-09-12 00:00:00+00	f110064a-846e-4e12-af1c-92ab081d3b94	2	t	d08bf7a9-ced8-4379-a5d7-a23430444c75	Control de rutina - Actualización condiciones	adulto	Odontograma versión 2 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-12	universal	{}	{"total_condiciones": 0, "condiciones_por_tipo": null}
20c4e7c0-12bb-4f3c-8250-efd74fcc5f08	e04e892e-5e91-422a-99c9-3987302ee7b5	2025-08-26 00:00:00+00	2025-09-25 00:53:33.691986+00	c801c016-ada5-4533-96ef-a7ddeb911334	1	f	\N	Odontograma inicial del paciente	adulto	Odontograma versión 1 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-08-26	universal	{}	{}
198c2749-d7fc-4f5d-84e9-849eb492d5e9	e04e892e-5e91-422a-99c9-3987302ee7b5	2025-09-13 00:00:00+00	2025-09-13 00:00:00+00	c801c016-ada5-4533-96ef-a7ddeb911334	2	t	20c4e7c0-12bb-4f3c-8250-efd74fcc5f08	Actualización tras intervención odontológica	adulto	Odontograma versión 2 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-13	universal	{}	{"total_condiciones": 0, "condiciones_por_tipo": null}
80ac2626-4328-41a3-b482-19e44c1a8206	491abeaf-7449-455e-9484-707626c1aca6	2025-09-22 00:00:00+00	2025-09-25 00:53:33.945565+00	f110064a-846e-4e12-af1c-92ab081d3b94	1	f	\N	Odontograma inicial del paciente	adulto	Odontograma versión 1 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-22	universal	{}	{}
7f768ebe-1b31-4d70-984c-4262aec68a16	491abeaf-7449-455e-9484-707626c1aca6	2025-09-02 00:00:00+00	2025-09-02 00:00:00+00	f110064a-846e-4e12-af1c-92ab081d3b94	2	t	80ac2626-4328-41a3-b482-19e44c1a8206	Control de rutina - Actualización condiciones	adulto	Odontograma versión 2 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-02	universal	{}	{"total_condiciones": 0, "condiciones_por_tipo": null}
be680f51-b649-4d0f-a2f4-51fcc5e368d0	97cd0017-61a1-406f-afaa-b1906156931b	2025-09-13 00:00:00+00	2025-09-25 00:53:34.211797+00	c801c016-ada5-4533-96ef-a7ddeb911334	1	f	\N	Odontograma inicial del paciente	adulto	Odontograma versión 1 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-13	universal	{}	{}
548c9b77-e210-408e-b230-698a35ba871d	97cd0017-61a1-406f-afaa-b1906156931b	2025-09-12 00:00:00+00	2025-09-12 00:00:00+00	c801c016-ada5-4533-96ef-a7ddeb911334	2	t	be680f51-b649-4d0f-a2f4-51fcc5e368d0	Seguimiento post-tratamiento	adulto	Odontograma versión 2 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-12	universal	{}	{"total_condiciones": 0, "condiciones_por_tipo": null}
694675ab-6c6d-46ac-a988-c9c060c3403d	17190193-78ea-46d2-8a25-bf87a3b86d0f	2025-08-26 00:00:00+00	2025-09-25 00:53:34.562303+00	c801c016-ada5-4533-96ef-a7ddeb911334	1	f	\N	Odontograma inicial del paciente	adulto	Odontograma versión 1 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-08-26	universal	{}	{}
6380885f-bd40-4e3d-8505-b25b62d6a6b4	17190193-78ea-46d2-8a25-bf87a3b86d0f	2025-09-26 00:00:00+00	2025-09-25 00:53:34.562303+00	c801c016-ada5-4533-96ef-a7ddeb911334	2	f	694675ab-6c6d-46ac-a988-c9c060c3403d	Seguimiento post-tratamiento	adulto	Odontograma versión 2 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-26	universal	{}	{}
2a383663-5fc5-46c4-bf3e-5ef362719b64	17190193-78ea-46d2-8a25-bf87a3b86d0f	2025-09-13 00:00:00+00	2025-09-13 00:00:00+00	c801c016-ada5-4533-96ef-a7ddeb911334	3	t	6380885f-bd40-4e3d-8505-b25b62d6a6b4	Registro de nuevas condiciones detectadas	adulto	Odontograma versión 3 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-13	universal	{}	{"total_condiciones": 0, "condiciones_por_tipo": null}
4f0906ee-2ad0-4b3c-b946-f9e932550382	af9a7d81-65d3-4066-8704-99560f29eb4b	2025-08-29 00:00:00+00	2025-09-25 00:53:35.083986+00	c801c016-ada5-4533-96ef-a7ddeb911334	1	f	\N	Odontograma inicial del paciente	adulto	Odontograma versión 1 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-08-29	universal	{}	{}
095e37cd-ef3b-443a-ad1c-2ce2b99af29a	af9a7d81-65d3-4066-8704-99560f29eb4b	2025-09-16 00:00:00+00	2025-09-25 00:53:35.083986+00	c801c016-ada5-4533-96ef-a7ddeb911334	2	f	4f0906ee-2ad0-4b3c-b946-f9e932550382	Seguimiento post-tratamiento	adulto	Odontograma versión 2 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-16	universal	{}	{}
639d4d2e-ad59-4af7-a5dd-a9dd5a937bbc	af9a7d81-65d3-4066-8704-99560f29eb4b	2025-10-05 00:00:00+00	2025-09-25 00:53:35.083986+00	c801c016-ada5-4533-96ef-a7ddeb911334	3	f	095e37cd-ef3b-443a-ad1c-2ce2b99af29a	Seguimiento post-tratamiento	adulto	Odontograma versión 3 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-10-05	universal	{}	{}
43388ef1-39ba-4dd8-93ff-6a636d96004b	af9a7d81-65d3-4066-8704-99560f29eb4b	2025-09-26 00:00:00+00	2025-09-26 00:00:00+00	c801c016-ada5-4533-96ef-a7ddeb911334	4	t	639d4d2e-ad59-4af7-a5dd-a9dd5a937bbc	Actualización tras intervención odontológica	adulto	Odontograma versión 4 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-26	universal	{}	{"total_condiciones": 0, "condiciones_por_tipo": null}
d70b931a-df3e-492b-aa7c-8b50e03c3072	eaaa81ae-6f30-4a22-a417-a48351f2e92e	2025-08-28 00:00:00+00	2025-09-25 00:53:35.585778+00	f110064a-846e-4e12-af1c-92ab081d3b94	1	f	\N	Odontograma inicial del paciente	adulto	Odontograma versión 1 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-08-28	universal	{}	{}
80eaaeaa-4e7a-4b75-9d42-6c449ca2596b	eaaa81ae-6f30-4a22-a417-a48351f2e92e	2025-09-09 00:00:00+00	2025-09-25 00:53:35.585778+00	f110064a-846e-4e12-af1c-92ab081d3b94	2	f	d70b931a-df3e-492b-aa7c-8b50e03c3072	Control de rutina - Actualización condiciones	adulto	Odontograma versión 2 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-09	universal	{}	{}
6cc617a6-ac28-4308-90d4-92c050d8af2e	eaaa81ae-6f30-4a22-a417-a48351f2e92e	2025-09-25 00:00:00+00	2025-09-25 00:53:35.585778+00	f110064a-846e-4e12-af1c-92ab081d3b94	3	f	80eaaeaa-4e7a-4b75-9d42-6c449ca2596b	Seguimiento post-tratamiento	adulto	Odontograma versión 3 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-25	universal	{}	{}
69a7a8ea-19c2-4896-b6f1-bb82351be859	eaaa81ae-6f30-4a22-a417-a48351f2e92e	2025-10-12 00:00:00+00	2025-10-12 00:00:00+00	f110064a-846e-4e12-af1c-92ab081d3b94	4	t	6cc617a6-ac28-4308-90d4-92c050d8af2e	Evolución del estado dental del paciente	adulto	Odontograma versión 4 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-10-12	universal	{}	{"total_condiciones": 0, "condiciones_por_tipo": null}
3567fd4f-82cc-4ce8-954d-a4ef3f722841	08b0d19f-df0b-4107-ac85-7a14371759ca	2025-09-16 00:00:00+00	2025-09-25 00:53:36.042097+00	f110064a-846e-4e12-af1c-92ab081d3b94	1	f	\N	Odontograma inicial del paciente	adulto	Odontograma versión 1 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-16	universal	{}	{}
fd1c4c95-85e9-45b1-b4d9-b543d010af1b	08b0d19f-df0b-4107-ac85-7a14371759ca	2025-09-07 00:00:00+00	2025-09-25 00:53:36.042097+00	f110064a-846e-4e12-af1c-92ab081d3b94	2	f	3567fd4f-82cc-4ce8-954d-a4ef3f722841	Seguimiento post-tratamiento	adulto	Odontograma versión 2 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-07	universal	{}	{}
27c8c6d2-2bb2-4412-9cc8-ffb0a2f98c7b	08b0d19f-df0b-4107-ac85-7a14371759ca	2025-09-22 00:00:00+00	2025-09-25 00:53:36.042097+00	f110064a-846e-4e12-af1c-92ab081d3b94	3	f	fd1c4c95-85e9-45b1-b4d9-b543d010af1b	Control de rutina - Actualización condiciones	adulto	Odontograma versión 3 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-22	universal	{}	{}
ac6b3991-8bec-47e5-b6cd-9629b8848657	08b0d19f-df0b-4107-ac85-7a14371759ca	2025-09-22 00:00:00+00	2025-09-22 00:00:00+00	f110064a-846e-4e12-af1c-92ab081d3b94	4	t	27c8c6d2-2bb2-4412-9cc8-ffb0a2f98c7b	Seguimiento post-tratamiento	adulto	Odontograma versión 4 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-22	universal	{}	{"total_condiciones": 0, "condiciones_por_tipo": null}
b9c410fc-2bf1-4f88-bb6a-4a970bd13b26	a38d7d6e-a7f8-4674-9686-c18b01e603a4	2025-09-09 00:00:00+00	2025-09-25 00:53:36.473196+00	f110064a-846e-4e12-af1c-92ab081d3b94	1	f	\N	Odontograma inicial del paciente	adulto	Odontograma versión 1 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-09	universal	{}	{}
7be9f8ce-84ae-4c12-8208-25976c30fc6e	a38d7d6e-a7f8-4674-9686-c18b01e603a4	2025-09-01 00:00:00+00	2025-09-25 00:53:36.473196+00	f110064a-846e-4e12-af1c-92ab081d3b94	2	f	b9c410fc-2bf1-4f88-bb6a-4a970bd13b26	Seguimiento post-tratamiento	adulto	Odontograma versión 2 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-01	universal	{}	{}
d1c30615-2945-4149-bbe3-3876dfdc7fe7	a38d7d6e-a7f8-4674-9686-c18b01e603a4	2025-09-24 00:00:00+00	2025-09-25 00:53:36.473196+00	f110064a-846e-4e12-af1c-92ab081d3b94	3	f	7be9f8ce-84ae-4c12-8208-25976c30fc6e	Actualización tras intervención odontológica	adulto	Odontograma versión 3 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-24	universal	{}	{}
12720901-8ed0-4065-a1de-86a067630787	a38d7d6e-a7f8-4674-9686-c18b01e603a4	2025-09-29 00:00:00+00	2025-09-29 00:00:00+00	f110064a-846e-4e12-af1c-92ab081d3b94	4	t	d1c30615-2945-4149-bbe3-3876dfdc7fe7	Seguimiento post-tratamiento	adulto	Odontograma versión 4 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-29	universal	{}	{"total_condiciones": 0, "condiciones_por_tipo": null}
10dc6149-3ac2-4dfe-bf39-21fe95f4c4a5	5ca97b83-21de-44f8-a1b3-09870d85cfcf	2025-08-27 00:00:00+00	2025-09-25 00:53:36.815612+00	c801c016-ada5-4533-96ef-a7ddeb911334	1	f	\N	Odontograma inicial del paciente	adulto	Odontograma versión 1 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-08-27	universal	{}	{}
dda5b49e-ee93-434c-a569-89b4d24b2d14	5ca97b83-21de-44f8-a1b3-09870d85cfcf	2025-09-27 00:00:00+00	2025-09-25 00:53:36.815612+00	c801c016-ada5-4533-96ef-a7ddeb911334	2	f	10dc6149-3ac2-4dfe-bf39-21fe95f4c4a5	Evolución del estado dental del paciente	adulto	Odontograma versión 2 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-27	universal	{}	{}
b4e9e4cf-1102-4ac2-ac03-637472927b94	5ca97b83-21de-44f8-a1b3-09870d85cfcf	2025-10-01 00:00:00+00	2025-10-01 00:00:00+00	c801c016-ada5-4533-96ef-a7ddeb911334	3	t	dda5b49e-ee93-434c-a569-89b4d24b2d14	Actualización tras intervención odontológica	adulto	Odontograma versión 3 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-10-01	universal	{}	{"total_condiciones": 0, "condiciones_por_tipo": null}
4214d3b7-207b-4561-a2b1-bd9b43fe636e	26798f99-329c-4bde-856f-09f08d40b915	2025-09-13 00:00:00+00	2025-09-25 00:53:37.27964+00	f110064a-846e-4e12-af1c-92ab081d3b94	1	f	\N	Odontograma inicial del paciente	adulto	Odontograma versión 1 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-13	universal	{}	{}
903772f4-0d49-437f-9d67-4c63030113d5	26798f99-329c-4bde-856f-09f08d40b915	2025-09-12 00:00:00+00	2025-09-25 00:53:37.27964+00	f110064a-846e-4e12-af1c-92ab081d3b94	2	f	4214d3b7-207b-4561-a2b1-bd9b43fe636e	Registro de nuevas condiciones detectadas	adulto	Odontograma versión 2 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-12	universal	{}	{}
b6beab48-b5c8-47f4-a735-3ddc1ee3eb65	26798f99-329c-4bde-856f-09f08d40b915	2025-09-25 00:00:00+00	2025-09-25 00:53:37.27964+00	f110064a-846e-4e12-af1c-92ab081d3b94	3	f	903772f4-0d49-437f-9d67-4c63030113d5	Seguimiento post-tratamiento	adulto	Odontograma versión 3 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-25	universal	{}	{}
1202fdba-7212-4151-bad9-ab05960ffe66	26798f99-329c-4bde-856f-09f08d40b915	2025-09-20 00:00:00+00	2025-09-20 00:00:00+00	f110064a-846e-4e12-af1c-92ab081d3b94	4	t	b6beab48-b5c8-47f4-a735-3ddc1ee3eb65	Actualización tras intervención odontológica	adulto	Odontograma versión 4 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-20	universal	{}	{"total_condiciones": 0, "condiciones_por_tipo": null}
96ba8a02-38f4-469c-9135-8d671328f549	377b3c4d-f9b8-4a70-aeb7-00258b9eb69b	2025-09-14 00:00:00+00	2025-09-25 00:53:37.495116+00	c801c016-ada5-4533-96ef-a7ddeb911334	1	f	\N	Odontograma inicial del paciente	adulto	Odontograma versión 1 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-14	universal	{}	{}
52a976e2-6e3d-4548-968e-891078713de4	377b3c4d-f9b8-4a70-aeb7-00258b9eb69b	2025-09-06 00:00:00+00	2025-09-06 00:00:00+00	c801c016-ada5-4533-96ef-a7ddeb911334	2	t	96ba8a02-38f4-469c-9135-8d671328f549	Seguimiento post-tratamiento	adulto	Odontograma versión 2 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-06	universal	{}	{"total_condiciones": 0, "condiciones_por_tipo": null}
0683dc49-e071-48fa-b901-fe05790bbd7c	9ca54413-12b4-4d52-a7fa-e02753992fcf	2025-08-29 00:00:00+00	2025-09-25 00:53:37.922861+00	f110064a-846e-4e12-af1c-92ab081d3b94	1	f	\N	Odontograma inicial del paciente	adulto	Odontograma versión 1 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-08-29	universal	{}	{}
7882b4a5-a2a7-4359-a09c-26c42a71f964	9ca54413-12b4-4d52-a7fa-e02753992fcf	2025-09-11 00:00:00+00	2025-09-25 00:53:37.922861+00	f110064a-846e-4e12-af1c-92ab081d3b94	2	f	0683dc49-e071-48fa-b901-fe05790bbd7c	Registro de nuevas condiciones detectadas	adulto	Odontograma versión 2 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-11	universal	{}	{}
5fb038dc-2428-4506-a6df-511d389c6cbd	9ca54413-12b4-4d52-a7fa-e02753992fcf	2025-10-06 00:00:00+00	2025-09-25 00:53:37.922861+00	f110064a-846e-4e12-af1c-92ab081d3b94	3	f	7882b4a5-a2a7-4359-a09c-26c42a71f964	Evolución del estado dental del paciente	adulto	Odontograma versión 3 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-10-06	universal	{}	{}
de0110cc-b0e1-4c74-8b16-8aa601ca947c	9ca54413-12b4-4d52-a7fa-e02753992fcf	2025-09-23 00:00:00+00	2025-09-23 00:00:00+00	f110064a-846e-4e12-af1c-92ab081d3b94	4	t	5fb038dc-2428-4506-a6df-511d389c6cbd	Evolución del estado dental del paciente	adulto	Odontograma versión 4 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-23	universal	{}	{"total_condiciones": 0, "condiciones_por_tipo": null}
793263bb-5f89-4447-ba62-7296e1602fdc	404cd152-f753-468e-9bc2-92afb4767ee4	2025-09-20 00:00:00+00	2025-09-25 00:53:38.395033+00	f110064a-846e-4e12-af1c-92ab081d3b94	1	f	\N	Odontograma inicial del paciente	adulto	Odontograma versión 1 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-20	universal	{}	{}
ae813da2-0a15-486d-8acf-8019e81ec491	404cd152-f753-468e-9bc2-92afb4767ee4	2025-09-20 00:00:00+00	2025-09-25 00:53:38.395033+00	f110064a-846e-4e12-af1c-92ab081d3b94	2	f	793263bb-5f89-4447-ba62-7296e1602fdc	Evolución del estado dental del paciente	adulto	Odontograma versión 2 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-20	universal	{}	{}
7ff94cf1-c50e-4ac1-ac88-d8f48f042939	404cd152-f753-468e-9bc2-92afb4767ee4	2025-09-27 00:00:00+00	2025-09-25 00:53:38.395033+00	f110064a-846e-4e12-af1c-92ab081d3b94	3	f	ae813da2-0a15-486d-8acf-8019e81ec491	Seguimiento post-tratamiento	adulto	Odontograma versión 3 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-27	universal	{}	{}
9675a988-c688-4221-9779-587e2f1671f4	404cd152-f753-468e-9bc2-92afb4767ee4	2025-09-24 00:00:00+00	2025-09-24 00:00:00+00	f110064a-846e-4e12-af1c-92ab081d3b94	4	t	7ff94cf1-c50e-4ac1-ac88-d8f48f042939	Actualización tras intervención odontológica	adulto	Odontograma versión 4 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-24	universal	{}	{"total_condiciones": 0, "condiciones_por_tipo": null}
9ec0440e-ea4a-460e-ba73-85a8d7b37e01	cf404971-ef00-4a99-b8cc-f5975505fa19	2025-09-10 00:00:00+00	2025-09-25 00:53:38.694516+00	c801c016-ada5-4533-96ef-a7ddeb911334	1	f	\N	Odontograma inicial del paciente	adulto	Odontograma versión 1 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-10	universal	{}	{}
69323ca8-7eba-45cd-9f48-24bdeb25cdfc	cf404971-ef00-4a99-b8cc-f5975505fa19	2025-09-29 00:00:00+00	2025-09-25 00:53:38.694516+00	c801c016-ada5-4533-96ef-a7ddeb911334	2	f	9ec0440e-ea4a-460e-ba73-85a8d7b37e01	Actualización tras intervención odontológica	adulto	Odontograma versión 2 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-29	universal	{}	{}
dbd8b2d8-d33e-4c5c-b61e-6e7e1f538393	cf404971-ef00-4a99-b8cc-f5975505fa19	2025-09-12 00:00:00+00	2025-09-12 00:00:00+00	c801c016-ada5-4533-96ef-a7ddeb911334	3	t	69323ca8-7eba-45cd-9f48-24bdeb25cdfc	Control de rutina - Actualización condiciones	adulto	Odontograma versión 3 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-12	universal	{}	{"total_condiciones": 0, "condiciones_por_tipo": null}
389d0135-95ba-4c22-bfe4-28b1532fec5c	4155558d-98ed-4c03-9fbd-bfc3e2ea7ac7	2025-09-10 00:00:00+00	2025-09-25 00:53:39.171119+00	c801c016-ada5-4533-96ef-a7ddeb911334	1	f	\N	Odontograma inicial del paciente	adulto	Odontograma versión 1 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-10	universal	{}	{}
b7f8a8c0-8cc1-4a1a-b8a7-db7f009a1f54	4155558d-98ed-4c03-9fbd-bfc3e2ea7ac7	2025-09-03 00:00:00+00	2025-09-25 00:53:39.171119+00	c801c016-ada5-4533-96ef-a7ddeb911334	2	f	389d0135-95ba-4c22-bfe4-28b1532fec5c	Actualización tras intervención odontológica	adulto	Odontograma versión 2 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-03	universal	{}	{}
07d9a8c2-2af9-4bc2-b5bb-8367d649c421	4155558d-98ed-4c03-9fbd-bfc3e2ea7ac7	2025-09-30 00:00:00+00	2025-09-25 00:53:39.171119+00	c801c016-ada5-4533-96ef-a7ddeb911334	3	f	b7f8a8c0-8cc1-4a1a-b8a7-db7f009a1f54	Actualización tras intervención odontológica	adulto	Odontograma versión 3 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-30	universal	{}	{}
4ee218a5-8ef4-44b0-a1f2-8877f2750ae2	4155558d-98ed-4c03-9fbd-bfc3e2ea7ac7	2025-10-08 00:00:00+00	2025-10-08 00:00:00+00	c801c016-ada5-4533-96ef-a7ddeb911334	4	t	07d9a8c2-2af9-4bc2-b5bb-8367d649c421	Registro de nuevas condiciones detectadas	adulto	Odontograma versión 4 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-10-08	universal	{}	{"total_condiciones": 0, "condiciones_por_tipo": null}
49ec9f3f-9403-4648-acff-278f50a1d90e	5a32b59a-084e-4896-8ad1-516ef7fc57ce	2025-09-15 00:00:00+00	2025-09-25 00:53:39.406593+00	c801c016-ada5-4533-96ef-a7ddeb911334	1	f	\N	Odontograma inicial del paciente	adulto	Odontograma versión 1 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-15	universal	{}	{}
c6240952-b22f-47c6-abf3-49e6c662a8b2	5a32b59a-084e-4896-8ad1-516ef7fc57ce	2025-09-08 00:00:00+00	2025-09-08 00:00:00+00	c801c016-ada5-4533-96ef-a7ddeb911334	2	t	49ec9f3f-9403-4648-acff-278f50a1d90e	Control de rutina - Actualización condiciones	adulto	Odontograma versión 2 - Estado dental del paciente actualizado	Evaluación clínica realizada el 2025-09-08	universal	{}	{"total_condiciones": 0, "condiciones_por_tipo": null}
\.


--
-- Data for Name: pacientes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pacientes (id, numero_historia, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, tipo_documento, numero_documento, fecha_nacimiento, edad, genero, celular_1, celular_2, email, direccion, ciudad, departamento, ocupacion, estado_civil, contacto_emergencia, alergias, medicamentos_actuales, condiciones_medicas, antecedentes_familiares, fecha_registro, fecha_actualizacion, registrado_por, activo, observaciones) FROM stdin;
546bb212-d549-492c-a5c1-803d43f69f00	HC000001	Gabriel	\N	Martínez	García	CI	19817915	1978-02-10	47	masculino	03074106386	03357957925	gabriel89@gmail.com	Calle 85, Caracas	Maracay	\N	Comerciante	viudo	{"nombre": "Rafael Sánchez", "relacion": "Hijo/a", "telefono": "03974714540", "direccion": ""}	{Penicilina}	\N	{Hipertensión}	\N	2025-09-23 15:22:43.462759+00	2025-09-23 15:22:43.462759+00	25356728-1a6e-4cb4-b466-b2b9a31e11ca	t	\N
6948e9de-290c-4781-813e-0d42ecbc88c7	HC000002	Rosa	Claudia	Álvarez	Rodríguez	CI	16424067	1976-02-13	49	femenino	04127014625	03841127665	rosa252@gmail.com	Calle 61, Caracas	Barcelona	\N	Estudiante	soltero	{"nombre": "Isabel Álvarez", "relacion": "Esposo/a", "telefono": "03888587744", "direccion": ""}	{"Ninguna conocida"}	\N	{"Ninguna conocida"}	\N	2025-09-23 15:22:43.5747+00	2025-09-23 15:22:43.5747+00	25356728-1a6e-4cb4-b466-b2b9a31e11ca	t	\N
cbe19a5c-dfc8-4c4b-9342-7f1b2168ad50	HC000003	José	José	Fernández	González	CI	18045797	1965-11-13	59	masculino	04213084549	\N	jose617@gmail.com	Calle 96, Barcelona	Barquisimeto	\N	Jubilado	soltero	{"nombre": "Rafael Romero", "relacion": "Padre/Madre", "telefono": "03086022134", "direccion": ""}	{"Ninguna conocida"}	\N	{Hipertensión}	\N	2025-09-23 15:22:43.666838+00	2025-09-23 15:22:43.666838+00	6214feee-9786-4d6d-8157-439b1d9e379a	t	\N
50b055af-40e4-4378-bb97-7d332af58e9c	HC000004	Teresa	\N	Sánchez	Martín	CI	26951658	1999-08-17	26	femenino	03096340992	03976065355	teresa72@gmail.com	Calle 73, Maturín	Valencia	\N	Profesional	casado	{"nombre": "Carmen Fernández", "relacion": "Hijo/a", "telefono": "03023618538", "direccion": ""}	{"Ninguna conocida"}	\N	{Asma}	\N	2025-09-23 15:22:43.76496+00	2025-09-23 15:22:43.76496+00	25356728-1a6e-4cb4-b466-b2b9a31e11ca	t	\N
e04e892e-5e91-422a-99c9-3987302ee7b5	HC000005	Rafael	Miguel	Díaz	Martínez	CI	20267881	1955-09-04	70	masculino	03582757190	03472480322	rafael315@gmail.com	Calle 54, Puerto La Cruz	San Cristóbal	\N	Empleado	casado	{"nombre": "Miguel Pérez", "relacion": "Hijo/a", "telefono": "04153055616", "direccion": ""}	{Lidocaína}	\N	{"Ninguna conocida"}	\N	2025-09-23 15:22:43.85389+00	2025-09-23 15:22:43.85389+00	25356728-1a6e-4cb4-b466-b2b9a31e11ca	t	\N
491abeaf-7449-455e-9484-707626c1aca6	HC000006	Isabella	Patricia	Ruiz	Gutiérrez	CI	12225416	1981-09-10	44	femenino	03299067144	\N	isabella679@gmail.com	Calle 61, Valencia	Caracas	\N	Comerciante	viudo	{"nombre": "Isabel Gutiérrez", "relacion": "Hijo/a", "telefono": "03312871662", "direccion": ""}	{"Ninguna conocida"}	\N	{"Ninguna conocida"}	\N	2025-09-23 15:22:43.93308+00	2025-09-23 15:22:43.93308+00	6214feee-9786-4d6d-8157-439b1d9e379a	t	\N
97cd0017-61a1-406f-afaa-b1906156931b	HC000007	Ricardo	Antonio	Gutiérrez	Sánchez	CI	26539869	2003-09-29	21	masculino	03403361185	03455896704	ricardo664@gmail.com	Calle 8, Caracas	Ciudad Guayana	\N	Jubilado	casado	{"nombre": "Rafael López", "relacion": "Padre/Madre", "telefono": "03353263453", "direccion": ""}	{"Ninguna conocida"}	\N	{"Ninguna conocida"}	\N	2025-09-23 15:22:44.002074+00	2025-09-23 15:22:44.002074+00	6214feee-9786-4d6d-8157-439b1d9e379a	t	\N
17190193-78ea-46d2-8a25-bf87a3b86d0f	HC000008	Antonio	Miguel	González	Díaz	CI	17771235	1973-10-24	51	masculino	03879431468	\N	antonio592@gmail.com	Calle 37, Maracaibo	Barquisimeto	\N	Comerciante	casado	{"nombre": "Antonio Rodríguez", "relacion": "Hijo/a", "telefono": "02865237615", "direccion": ""}	{"Ninguna conocida"}	\N	{"Ninguna conocida"}	\N	2025-09-23 15:22:44.083421+00	2025-09-23 15:22:44.083421+00	25356728-1a6e-4cb4-b466-b2b9a31e11ca	t	\N
af9a7d81-65d3-4066-8704-99560f29eb4b	HC000009	Diego	Antonio	Álvarez	Ruiz	CI	22329111	1977-05-20	48	masculino	03431809915	\N	diego41@gmail.com	Calle 31, Barquisimeto	Ciudad Guayana	\N	Empleado	soltero	{"nombre": "José Moreno", "relacion": "Esposo/a", "telefono": "03639584290", "direccion": ""}	{"Ninguna conocida"}	\N	{"Ninguna conocida"}	\N	2025-09-23 15:22:44.162062+00	2025-09-23 15:22:44.162062+00	6214feee-9786-4d6d-8157-439b1d9e379a	t	\N
eaaa81ae-6f30-4a22-a417-a48351f2e92e	HC000010	Claudia	\N	Alonso	Ruiz	CI	14163410	1989-01-11	36	femenino	04195734766	\N	claudia860@gmail.com	Calle 89, Puerto La Cruz	Maturín	\N	Comerciante	divorciado	{"nombre": "Carmen Romero", "relacion": "Padre/Madre", "telefono": "03872049328", "direccion": ""}	{"Ninguna conocida"}	\N	{"Ninguna conocida"}	\N	2025-09-23 15:22:44.229305+00	2025-09-23 15:22:44.229305+00	25356728-1a6e-4cb4-b466-b2b9a31e11ca	t	\N
08b0d19f-df0b-4107-ac85-7a14371759ca	HC000011	Alejandro	\N	Sánchez	Ruiz	CI	22064242	1971-04-10	54	masculino	03332235330	04104805759	alejandro203@gmail.com	Calle 92, Valencia	Barcelona	\N	Estudiante	divorciado	{"nombre": "Jesús López", "relacion": "Hijo/a", "telefono": "03903293245", "direccion": ""}	{"Ninguna conocida"}	\N	{"Ninguna conocida"}	\N	2025-09-23 15:22:44.303371+00	2025-09-23 15:22:44.303371+00	6214feee-9786-4d6d-8157-439b1d9e379a	t	\N
a38d7d6e-a7f8-4674-9686-c18b01e603a4	HC000012	Patricia	\N	Martínez	Romero	CI	12357703	1966-09-09	59	femenino	04151600819	\N	patricia352@gmail.com	Calle 49, Valencia	San Cristóbal	\N	Comerciante	divorciado	{"nombre": "Carmen Martínez", "relacion": "Padre/Madre", "telefono": "02998211604", "direccion": ""}	{Penicilina}	\N	{"Ninguna conocida"}	\N	2025-09-23 15:22:44.380495+00	2025-09-23 15:22:44.380495+00	6214feee-9786-4d6d-8157-439b1d9e379a	t	\N
5ca97b83-21de-44f8-a1b3-09870d85cfcf	HC000013	Isabel	Carolina	Pérez	López	CI	20361217	1961-01-03	64	femenino	03555321285	\N	isabel215@gmail.com	Calle 21, Maturín	Maracaibo	\N	Jubilado	divorciado	{"nombre": "Carmen Ruiz", "relacion": "Esposo/a", "telefono": "03611859718", "direccion": ""}	{"Ninguna conocida"}	\N	{Hipertensión}	\N	2025-09-23 15:22:44.458199+00	2025-09-23 15:22:44.458199+00	25356728-1a6e-4cb4-b466-b2b9a31e11ca	t	\N
26798f99-329c-4bde-856f-09f08d40b915	HC000014	Francisco	\N	López	Sánchez	CI	19714710	1991-11-17	33	masculino	03374281856	03535281858	francisco891@gmail.com	Calle 25, Maturín	Maturín	\N	Jubilado	divorciado	{"nombre": "Rafael Moreno", "relacion": "Hijo/a", "telefono": "03777736022", "direccion": ""}	{"Ninguna conocida"}	\N	{"Ninguna conocida"}	\N	2025-09-23 15:22:44.547423+00	2025-09-23 15:22:44.547423+00	25356728-1a6e-4cb4-b466-b2b9a31e11ca	t	\N
377b3c4d-f9b8-4a70-aeb7-00258b9eb69b	HC000015	Fernando	Francisco	Martín	López	CI	13334871	1955-06-21	70	masculino	02896810036	03576418195	fernando884@gmail.com	Calle 6, Maturín	Maracay	\N	Comerciante	casado	{"nombre": "Carlos Romero", "relacion": "Esposo/a", "telefono": "03887614646", "direccion": ""}	{Penicilina}	\N	{"Ninguna conocida"}	\N	2025-09-23 15:22:44.630253+00	2025-09-23 15:22:44.630253+00	6214feee-9786-4d6d-8157-439b1d9e379a	t	\N
9ca54413-12b4-4d52-a7fa-e02753992fcf	HC000016	José	Rafael	López	Sánchez	CI	17122490	1965-10-07	59	masculino	02965331359	\N	jose551@gmail.com	Calle 51, Maturín	Barquisimeto	\N	Estudiante	viudo	{"nombre": "Ricardo Moreno", "relacion": "Esposo/a", "telefono": "03057441329", "direccion": ""}	{"Ninguna conocida"}	\N	{"Ninguna conocida"}	\N	2025-09-23 15:22:44.694685+00	2025-09-23 15:22:44.694685+00	25356728-1a6e-4cb4-b466-b2b9a31e11ca	t	\N
404cd152-f753-468e-9bc2-92afb4767ee4	HC000017	Daniel	Miguel	Jiménez	Rodríguez	CI	10336217	1996-03-27	29	masculino	04042015945	03733560262	daniel288@gmail.com	Calle 43, Caracas	Puerto La Cruz	\N	Empleado	casado	{"nombre": "Carlos Ruiz", "relacion": "Hijo/a", "telefono": "03916894966", "direccion": ""}	{Penicilina}	\N	{"Ninguna conocida"}	\N	2025-09-23 15:22:44.759008+00	2025-09-23 15:22:44.759008+00	25356728-1a6e-4cb4-b466-b2b9a31e11ca	t	\N
cf404971-ef00-4a99-b8cc-f5975505fa19	HC000018	Daniela	\N	López	Sánchez	CI	11444533	1966-07-02	59	femenino	03964058689	\N	daniela785@gmail.com	Calle 66, Caracas	Barcelona	\N	Estudiante	casado	{"nombre": "Natalia López", "relacion": "Esposo/a", "telefono": "04101946343", "direccion": ""}	{Penicilina}	\N	{Diabetes}	\N	2025-09-23 15:22:44.825877+00	2025-09-23 15:22:44.825877+00	6214feee-9786-4d6d-8157-439b1d9e379a	t	\N
4155558d-98ed-4c03-9fbd-bfc3e2ea7ac7	HC000019	Fernando	\N	López	Muñoz	CI	10167892	1979-06-30	46	masculino	03683740694	03986905558	fernando496@gmail.com	Calle 92, Caracas	Maturín	\N	Comerciante	soltero	{"nombre": "Gabriel Alonso", "relacion": "Padre/Madre", "telefono": "04129746562", "direccion": ""}	{"Ninguna conocida"}	\N	{"Ninguna conocida"}	\N	2025-09-23 15:22:44.895727+00	2025-09-23 15:22:44.895727+00	6214feee-9786-4d6d-8157-439b1d9e379a	t	\N
5a32b59a-084e-4896-8ad1-516ef7fc57ce	HC000020	Victoria	Valentina	Ruiz	Díaz	CI	17513645	1987-03-25	38	femenino	03175749225	03123179517	victoria951@gmail.com	Calle 50, Caracas	Ciudad Guayana	\N	Empleado	casado	{"nombre": "Isabel Rodríguez", "relacion": "Padre/Madre", "telefono": "03523031249", "direccion": ""}	{"Ninguna conocida"}	\N	{"Ninguna conocida"}	\N	2025-09-23 15:22:44.962597+00	2025-09-23 15:22:44.962597+00	6214feee-9786-4d6d-8157-439b1d9e379a	t	\N
dcc1c80b-e21f-4f76-b0b9-9c2f52635305	HC000021	wilmer	nicolas	aguirre	carrion	CI	28704741	\N	\N	masculino	04129482192	041294875632	wilmer@gmail.com	asas	plc	caaa	nada	casado	{}	\N	\N	\N	\N	2025-09-25 10:15:48.80519+00	2025-09-25 10:15:48.80519+00	25356728-1a6e-4cb4-b466-b2b9a31e11ca	t	\N
05f72d6b-db89-428f-87ae-41f4abffe460	HC000022	jesus	\N	cordova	\N	CI	78965412	2025-08-07	0	masculino	0412-4529874	0412-4529874	uiojhgt@odontomara.com	\N	ccs	\N	vvv	casado	{}	\N	\N	\N	\N	2025-10-01 18:53:17.338895+00	2025-10-01 18:53:17.338895+00	25356728-1a6e-4cb4-b466-b2b9a31e11ca	t	\N
\.


--
-- Name: condiciones_diente condiciones_diente_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.condiciones_diente
    ADD CONSTRAINT condiciones_diente_pkey PRIMARY KEY (id);


--
-- Name: odontograma odontograma_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.odontograma
    ADD CONSTRAINT odontograma_pkey PRIMARY KEY (id);


--
-- Name: pacientes pacientes_numero_documento_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pacientes
    ADD CONSTRAINT pacientes_numero_documento_key UNIQUE (numero_documento);


--
-- Name: pacientes pacientes_numero_historia_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pacientes
    ADD CONSTRAINT pacientes_numero_historia_key UNIQUE (numero_historia);


--
-- Name: pacientes pacientes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pacientes
    ADD CONSTRAINT pacientes_pkey PRIMARY KEY (id);


--
-- Name: idx_condiciones_diente; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_condiciones_diente ON public.condiciones_diente USING btree (diente_id);


--
-- Name: idx_condiciones_odontograma; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_condiciones_odontograma ON public.condiciones_diente USING btree (odontograma_id);


--
-- Name: idx_odontograma_actual; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_odontograma_actual ON public.odontograma USING btree (paciente_id, es_version_actual);


--
-- Name: idx_odontograma_paciente_version; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_odontograma_paciente_version ON public.odontograma USING btree (paciente_id, version);


--
-- Name: idx_pacientes_activo; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_pacientes_activo ON public.pacientes USING btree (activo);


--
-- Name: idx_pacientes_celular1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_pacientes_celular1 ON public.pacientes USING btree (celular_1);


--
-- Name: idx_pacientes_fecha_registro; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_pacientes_fecha_registro ON public.pacientes USING btree (fecha_registro);


--
-- Name: idx_pacientes_nombres_completo; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_pacientes_nombres_completo ON public.pacientes USING btree (primer_nombre, primer_apellido);


--
-- Name: idx_pacientes_numero_documento; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_pacientes_numero_documento ON public.pacientes USING btree (numero_documento);


--
-- Name: pacientes trigger_calcular_edad_paciente; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_calcular_edad_paciente BEFORE INSERT OR UPDATE ON public.pacientes FOR EACH ROW EXECUTE FUNCTION public.calcular_edad_paciente();


--
-- Name: pacientes trigger_generar_numero_historia; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_generar_numero_historia BEFORE INSERT ON public.pacientes FOR EACH ROW EXECUTE FUNCTION public.generar_numero_historia();


--
-- Name: odontograma trigger_manejar_version_odontograma; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_manejar_version_odontograma BEFORE INSERT OR UPDATE ON public.odontograma FOR EACH ROW EXECUTE FUNCTION public.manejar_version_odontograma();


--
-- Name: odontograma trigger_odontograma_fecha_actualizacion; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_odontograma_fecha_actualizacion BEFORE UPDATE ON public.odontograma FOR EACH ROW EXECUTE FUNCTION public.actualizar_fecha_modificacion();


--
-- Name: pacientes trigger_pacientes_fecha_actualizacion; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trigger_pacientes_fecha_actualizacion BEFORE UPDATE ON public.pacientes FOR EACH ROW EXECUTE FUNCTION public.actualizar_fecha_modificacion();


--
-- Name: condiciones_diente condiciones_diente_diente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.condiciones_diente
    ADD CONSTRAINT condiciones_diente_diente_id_fkey FOREIGN KEY (diente_id) REFERENCES public.dientes(id);


--
-- Name: condiciones_diente condiciones_diente_intervencion_origen_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.condiciones_diente
    ADD CONSTRAINT condiciones_diente_intervencion_origen_id_fkey FOREIGN KEY (intervencion_origen_id) REFERENCES public.intervenciones(id);


--
-- Name: condiciones_diente condiciones_diente_odontograma_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.condiciones_diente
    ADD CONSTRAINT condiciones_diente_odontograma_id_fkey FOREIGN KEY (odontograma_id) REFERENCES public.odontograma(id) ON DELETE CASCADE;


--
-- Name: condiciones_diente condiciones_diente_registrado_por_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.condiciones_diente
    ADD CONSTRAINT condiciones_diente_registrado_por_fkey FOREIGN KEY (registrado_por) REFERENCES public.usuarios(id);


--
-- Name: odontograma odontograma_odontologo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.odontograma
    ADD CONSTRAINT odontograma_odontologo_id_fkey FOREIGN KEY (odontologo_id) REFERENCES public.personal(id);


--
-- Name: odontograma odontograma_paciente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.odontograma
    ADD CONSTRAINT odontograma_paciente_id_fkey FOREIGN KEY (paciente_id) REFERENCES public.pacientes(id);


--
-- Name: odontograma odontograma_version_anterior_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.odontograma
    ADD CONSTRAINT odontograma_version_anterior_id_fkey FOREIGN KEY (version_anterior_id) REFERENCES public.odontograma(id);


--
-- Name: pacientes pacientes_registrado_por_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pacientes
    ADD CONSTRAINT pacientes_registrado_por_fkey FOREIGN KEY (registrado_por) REFERENCES public.usuarios(id);


--
-- Name: odontograma; Type: ROW SECURITY; Schema: public; Owner: postgres
--

ALTER TABLE public.odontograma ENABLE ROW LEVEL SECURITY;

--
-- Name: odontograma odontograma_policy; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY odontograma_policy ON public.odontograma USING (true);


--
-- Name: pacientes; Type: ROW SECURITY; Schema: public; Owner: postgres
--

ALTER TABLE public.pacientes ENABLE ROW LEVEL SECURITY;

--
-- Name: pacientes pacientes_policy; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY pacientes_policy ON public.pacientes USING (true);


--
-- Name: TABLE condiciones_diente; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.condiciones_diente TO anon;
GRANT ALL ON TABLE public.condiciones_diente TO authenticated;
GRANT ALL ON TABLE public.condiciones_diente TO service_role;


--
-- Name: TABLE odontograma; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.odontograma TO anon;
GRANT ALL ON TABLE public.odontograma TO authenticated;
GRANT ALL ON TABLE public.odontograma TO service_role;


--
-- Name: TABLE pacientes; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.pacientes TO anon;
GRANT ALL ON TABLE public.pacientes TO authenticated;
GRANT ALL ON TABLE public.pacientes TO service_role;


--
-- PostgreSQL database dump complete
--

\unrestrict wAikh5DCMGMzufow2VaWtLTA0pQdPcw36hepsRDH8POWVjtIBC5fcUZagFHdK7v

