/*
 * GuardBear DB Query Builder
 * Copyright (C) 2015, GuardBear Inc.
 * October 31, 2023.
 *
 * This program is free software; you can redistribute it
 * and/or modify it under the terms of the GNU General Public
 * License (version 2) as published by the FSF - Free Software
 * Foundation.
 */

#ifndef _GUARDBEAR_DB_QUERY_BUILDER_HPP
#define _GUARDBEAR_DB_QUERY_BUILDER_HPP

#include "builder.hpp"
#include "stringHelper.h"
#include <string>

constexpr auto GUARDBEAR_DB_ALLOWED_CHARS {"-_ "};

class GuardBearDBQueryBuilder final : public Utils::Builder<GuardBearDBQueryBuilder>
{
private:
    std::string m_query;

public:
    GuardBearDBQueryBuilder& global()
    {
        m_query += "global sql ";
        return *this;
    }

    GuardBearDBQueryBuilder& agent(const std::string& id)
    {
        if (!Utils::isNumber(id))
        {
            throw std::runtime_error("Invalid agent id");
        }

        m_query += "agent " + id + " sql ";
        return *this;
    }

    GuardBearDBQueryBuilder& selectAll()
    {
        m_query += "SELECT * ";
        return *this;
    }

    GuardBearDBQueryBuilder& fromTable(const std::string& table)
    {
        if (!Utils::isAlphaNumericWithSpecialCharacters(table, GUARDBEAR_DB_ALLOWED_CHARS))
        {
            throw std::runtime_error("Invalid table name");
        }
        m_query += "FROM " + table + " ";
        return *this;
    }

    GuardBearDBQueryBuilder& whereColumn(const std::string& column)
    {
        if (!Utils::isAlphaNumericWithSpecialCharacters(column, GUARDBEAR_DB_ALLOWED_CHARS))
        {
            throw std::runtime_error("Invalid column name");
        }
        m_query += "WHERE " + column + " ";
        return *this;
    }

    GuardBearDBQueryBuilder& isNull()
    {
        m_query += "IS NULL ";
        return *this;
    }

    GuardBearDBQueryBuilder& isNotNull()
    {
        m_query += "IS NOT NULL ";
        return *this;
    }

    GuardBearDBQueryBuilder& equalsTo(const std::string& value)
    {
        if (!Utils::isAlphaNumericWithSpecialCharacters(value, GUARDBEAR_DB_ALLOWED_CHARS))
        {
            throw std::runtime_error("Invalid value");
        }
        m_query += "= '" + value + "' ";
        return *this;
    }

    GuardBearDBQueryBuilder& andColumn(const std::string& column)
    {
        if (!Utils::isAlphaNumericWithSpecialCharacters(column, GUARDBEAR_DB_ALLOWED_CHARS))
        {
            throw std::runtime_error("Invalid column name");
        }
        m_query += "AND " + column + " ";
        return *this;
    }

    GuardBearDBQueryBuilder& orColumn(const std::string& column)
    {
        if (!Utils::isAlphaNumericWithSpecialCharacters(column, GUARDBEAR_DB_ALLOWED_CHARS))
        {
            throw std::runtime_error("Invalid column name");
        }
        m_query += "OR " + column + " ";
        return *this;
    }

    GuardBearDBQueryBuilder& globalGetCommand(const std::string& command)
    {
        if (!Utils::isAlphaNumericWithSpecialCharacters(command, GUARDBEAR_DB_ALLOWED_CHARS))
        {
            throw std::runtime_error("Invalid command");
        }
        m_query += "global get-" + command + " ";
        return *this;
    }

    GuardBearDBQueryBuilder& globalFindCommand(const std::string& command)
    {
        if (!Utils::isAlphaNumericWithSpecialCharacters(command, GUARDBEAR_DB_ALLOWED_CHARS))
        {
            throw std::runtime_error("Invalid command");
        }
        m_query += "global find-" + command + " ";
        return *this;
    }

    GuardBearDBQueryBuilder& globalSelectCommand(const std::string& command)
    {
        if (!Utils::isAlphaNumericWithSpecialCharacters(command, GUARDBEAR_DB_ALLOWED_CHARS))
        {
            throw std::runtime_error("Invalid command");
        }
        m_query += "global select-" + command + " ";
        return *this;
    }

    GuardBearDBQueryBuilder& agentGetOsInfoCommand(const std::string& id)
    {
        if (!Utils::isNumber(id))
        {
            throw std::runtime_error("Invalid agent id");
        }
        m_query += "agent " + id + " osinfo get ";
        return *this;
    }

    GuardBearDBQueryBuilder& agentGetHotfixesCommand(const std::string& id)
    {
        if (!Utils::isNumber(id))
        {
            throw std::runtime_error("Invalid agent id");
        }
        m_query += "agent " + id + " hotfix get ";
        return *this;
    }

    GuardBearDBQueryBuilder& agentGetPackagesCommand(const std::string& id)
    {
        if (!Utils::isNumber(id))
        {
            throw std::runtime_error("Invalid agent id");
        }
        m_query += "agent " + id + " package get ";
        return *this;
    }

    std::string build()
    {
        return m_query;
    }
};

#endif /* _GUARDBEAR_DB_QUERY_BUILDER_HPP */
