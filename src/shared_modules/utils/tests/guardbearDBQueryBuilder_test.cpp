/*
 * GuardBear shared modules utils
 * Copyright (C) 2015, GuardBear Inc.
 * Nov 1, 2023.
 *
 * This program is free software; you can redistribute it
 * and/or modify it under the terms of the GNU General Public
 * License (version 2) as published by the FSF - Free Software
 * Foundation.
 */

#include "guardbearDBQueryBuilder_test.hpp"
#include "guardbearDBQueryBuilder.hpp"
#include <string>

TEST_F(GuardBearDBQueryBuilderTest, GlobalTest)
{
    std::string message = GuardBearDBQueryBuilder::builder().global().selectAll().fromTable("agent").build();
    EXPECT_EQ(message, "global sql SELECT * FROM agent ");
}

TEST_F(GuardBearDBQueryBuilderTest, AgentTest)
{
    std::string message = GuardBearDBQueryBuilder::builder().agent("0").selectAll().fromTable("sys_programs").build();
    EXPECT_EQ(message, "agent 0 sql SELECT * FROM sys_programs ");
}

TEST_F(GuardBearDBQueryBuilderTest, WhereTest)
{
    std::string message = GuardBearDBQueryBuilder::builder()
                              .agent("0")
                              .selectAll()
                              .fromTable("sys_programs")
                              .whereColumn("name")
                              .equalsTo("bash")
                              .build();
    EXPECT_EQ(message, "agent 0 sql SELECT * FROM sys_programs WHERE name = 'bash' ");
}

TEST_F(GuardBearDBQueryBuilderTest, WhereAndTest)
{
    std::string message = GuardBearDBQueryBuilder::builder()
                              .agent("0")
                              .selectAll()
                              .fromTable("sys_programs")
                              .whereColumn("name")
                              .equalsTo("bash")
                              .andColumn("version")
                              .equalsTo("1")
                              .build();
    EXPECT_EQ(message, "agent 0 sql SELECT * FROM sys_programs WHERE name = 'bash' AND version = '1' ");
}

TEST_F(GuardBearDBQueryBuilderTest, WhereOrTest)
{
    std::string message = GuardBearDBQueryBuilder::builder()
                              .agent("0")
                              .selectAll()
                              .fromTable("sys_programs")
                              .whereColumn("name")
                              .equalsTo("bash")
                              .orColumn("version")
                              .equalsTo("1")
                              .build();
    EXPECT_EQ(message, "agent 0 sql SELECT * FROM sys_programs WHERE name = 'bash' OR version = '1' ");
}

TEST_F(GuardBearDBQueryBuilderTest, WhereIsNullTest)
{
    std::string message = GuardBearDBQueryBuilder::builder()
                              .agent("0")
                              .selectAll()
                              .fromTable("sys_programs")
                              .whereColumn("name")
                              .isNull()
                              .build();
    EXPECT_EQ(message, "agent 0 sql SELECT * FROM sys_programs WHERE name IS NULL ");
}

TEST_F(GuardBearDBQueryBuilderTest, WhereIsNotNullTest)
{
    std::string message = GuardBearDBQueryBuilder::builder()
                              .agent("0")
                              .selectAll()
                              .fromTable("sys_programs")
                              .whereColumn("name")
                              .isNotNull()
                              .build();
    EXPECT_EQ(message, "agent 0 sql SELECT * FROM sys_programs WHERE name IS NOT NULL ");
}

TEST_F(GuardBearDBQueryBuilderTest, InvalidValue)
{
    EXPECT_THROW(GuardBearDBQueryBuilder::builder()
                     .agent("0")
                     .selectAll()
                     .fromTable("sys_programs")
                     .whereColumn("name")
                     .equalsTo("bash'")
                     .build(),
                 std::runtime_error);
}

TEST_F(GuardBearDBQueryBuilderTest, InvalidColumn)
{
    EXPECT_THROW(GuardBearDBQueryBuilder::builder()
                     .agent("0")
                     .selectAll()
                     .fromTable("sys_programs")
                     .whereColumn("name'")
                     .equalsTo("bash")
                     .build(),
                 std::runtime_error);
}

TEST_F(GuardBearDBQueryBuilderTest, InvalidTable)
{
    EXPECT_THROW(GuardBearDBQueryBuilder::builder()
                     .agent("0")
                     .selectAll()
                     .fromTable("sys_programs'")
                     .whereColumn("name")
                     .equalsTo("bash")
                     .build(),
                 std::runtime_error);
}

TEST_F(GuardBearDBQueryBuilderTest, GlobalGetCommand)
{
    std::string message = GuardBearDBQueryBuilder::builder().globalGetCommand("agent-info 1").build();
    EXPECT_EQ(message, "global get-agent-info 1 ");
}

TEST_F(GuardBearDBQueryBuilderTest, GlobalFindCommand)
{
    std::string message = GuardBearDBQueryBuilder::builder().globalFindCommand("agent 1").build();
    EXPECT_EQ(message, "global find-agent 1 ");
}

TEST_F(GuardBearDBQueryBuilderTest, GlobalSelectCommand)
{
    std::string message = GuardBearDBQueryBuilder::builder().globalSelectCommand("agent-name 1").build();
    EXPECT_EQ(message, "global select-agent-name 1 ");
}

TEST_F(GuardBearDBQueryBuilderTest, AgentGetOsInfoCommand)
{
    std::string message = GuardBearDBQueryBuilder::builder().agentGetOsInfoCommand("1").build();
    EXPECT_EQ(message, "agent 1 osinfo get ");
}

TEST_F(GuardBearDBQueryBuilderTest, AgentGetHotfixesCommand)
{
    std::string message = GuardBearDBQueryBuilder::builder().agentGetHotfixesCommand("1").build();
    EXPECT_EQ(message, "agent 1 hotfix get ");
}

TEST_F(GuardBearDBQueryBuilderTest, AgentGetPackagesCommand)
{
    std::string message = GuardBearDBQueryBuilder::builder().agentGetPackagesCommand("1").build();
    EXPECT_EQ(message, "agent 1 package get ");
}
