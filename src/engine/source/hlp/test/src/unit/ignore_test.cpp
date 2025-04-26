#include <gtest/gtest.h>

#include "hlp_test.hpp"

auto constexpr NAME = "ignoreParser";

INSTANTIATE_TEST_SUITE_P(IgnoreBuild,
                         HlpBuildTest,
                         ::testing::Values(BuildT(FAILURE, getIgnoreParser, {NAME, "", {}, {}}),
                                           BuildT(SUCCESS, getIgnoreParser, {NAME, "", {}, {"ignore"}}),
                                           BuildT(FAILURE, getIgnoreParser, {NAME, "", {}, {"ignore", "unexpected"}}),
                                           BuildT(FAILURE, getIgnoreParser, {NAME, "not allow", {}, {"ignore"}})));

INSTANTIATE_TEST_SUITE_P(
    IgnoreParse,
    HlpParseTest,
    ::testing::Values(ParseT(SUCCESS, "guardbear", j("{}"), 5, getIgnoreParser, {NAME, "", {}, {"guardbear"}}),
                      ParseT(SUCCESS, "guardbear 123", j("{}"), 5, getIgnoreParser, {NAME, "", {}, {"guardbear"}}),
                      ParseT(SUCCESS, "guardbearguardbear", j("{}"), 10, getIgnoreParser, {NAME, "", {}, {"guardbear"}}),
                      ParseT(SUCCESS, "guardbearguardbearguardbearguardbear", j("{}"), 20, getIgnoreParser, {NAME, "", {}, {"guardbear"}}),
                      ParseT(SUCCESS, "guardbearwa", j("{}"), 5, getIgnoreParser, {NAME, "", {}, {"guardbear"}}),
                      ParseT(FAILURE, "GUARDBEAR", j("{}"), 0, getIgnoreParser, {NAME, "", {}, {"guardbear"}})));
