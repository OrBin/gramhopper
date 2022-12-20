{{/*
Expand the name of the chart.
*/}}
{{- define "gramhopper.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "gramhopper.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "gramhopper.labels" -}}
helm.sh/chart: {{ include "gramhopper.chart" . }}
{{ include "gramhopper.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "gramhopper.selectorLabels" -}}
app.kubernetes.io/name: {{ include "gramhopper.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
