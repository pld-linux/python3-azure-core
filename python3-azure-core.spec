#
# Conditional build:
%bcond_without	tests	# unit tests

Summary:	Microsoft Azure Core Library for Python
Summary(pl.UTF-8):	Biblioteka Microsoft Azure Core dla Pythona
Name:		python3-azure-core
Version:	1.38.2
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/azure-core/
Source0:	https://files.pythonhosted.org/packages/source/a/azure-core/azure_core-%{version}.tar.gz
# Source0-md5:	25e95f482afd1f88515ec7c30906873e
URL:		https://pypi.org/project/azure-core/
BuildRequires:	python3-modules >= 1:3.9
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-aiohttp >= 3.0
BuildRequires:	python3-azure-storage-blob
BuildRequires:	python3-isodate >= 0.6.1
BuildRequires:	python3-opentelemetry-api >= 1.26
BuildRequires:	python3-opentelemetry-api < 2
BuildRequires:	python3-opentelemetry-instrumentation
BuildRequires:	python3-opentelemetry-instrumentation-requests
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-asyncio
BuildRequires:	python3-pytest-trio
BuildRequires:	python3-requests >= 2.21.0
BuildRequires:	python3-typing_extensions >= 4.6.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-modules >= 1:3.9
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Azure core provides shared exceptions and modules for Python SDK
client libraries.

%description -l pl.UTF-8
Pakiet Azure core udostępnia współdzielone wyjątki i moduły dla
bibliotek klienckich SDK dla Pythona.

%prep
%setup -q -n azure_core-%{version}

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_asyncio.plugin,pytest_trio.plugin \
PYTHONPATH=$(pwd):$(pwd)/tests/specs_sdk/modeltypes \
%{__python3} -m pytest tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

install -d $RPM_BUILD_ROOT%{_examplesdir}
cp -pr samples $RPM_BUILD_ROOT%{_examplesdir}/python3-azure-core-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md LICENSE README.md TROUBLESHOOTING.md
%dir %{py3_sitescriptdir}/azure
%{py3_sitescriptdir}/azure/core
%{py3_sitescriptdir}/azure_core-%{version}-py*.egg-info
%{_examplesdir}/%{name}-%{version}
