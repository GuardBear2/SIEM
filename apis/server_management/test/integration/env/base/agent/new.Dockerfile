FROM public.ecr.aws/o5x5t0j3/amd64/api_development:integration_test_guardbear-generic

ARG GUARDBEAR_BRANCH

## install GuardBear
RUN mkdir guardbear && curl -sL https://github.com/guardbear/guardbear/tarball/${GUARDBEAR_BRANCH} | tar zx --strip-components=1 -C guardbear
ADD base/agent/preloaded-vars.conf /guardbear/etc/preloaded-vars.conf
RUN /guardbear/install.sh

COPY base/agent/entrypoint.sh /scripts/entrypoint.sh

HEALTHCHECK --retries=900 --interval=1s --timeout=40s --start-period=30s CMD /usr/bin/python3 /tmp_volume/healthcheck/healthcheck.py || exit 1
