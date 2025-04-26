#include <gtest/gtest.h>

#include <base/utils/guardbearProtocol/guardbearResponse.hpp>

TEST(GuardBearResponse, constructor)
{
    const json::Json jdata {R"({"test": "data"})"};
    const int error {0};
    const std::string message {"test message"};
    const base::utils::guardbearProtocol::GuardBearResponse wresponse {jdata, error, message};
    EXPECT_EQ(wresponse.data(), jdata);
    EXPECT_EQ(wresponse.error(), error);
    EXPECT_EQ(wresponse.message(), message);
}

TEST(GuardBearResponse, toString)
{
    const json::Json jdata {R"({"test": "data"})"};
    const int error {0};
    const std::string message {"test message"};
    const base::utils::guardbearProtocol::GuardBearResponse wresponse {jdata, error, message};
    EXPECT_EQ(wresponse.toString(), R"({"data":{"test":"data"},"error":0,"message":"test message"})");
}

TEST(GuardBearResponse, toStringNoMessage)
{
    const json::Json jdata {R"({"test": "data"})"};
    const int error {0};
    const base::utils::guardbearProtocol::GuardBearResponse wresponse {jdata, error};
    EXPECT_EQ(wresponse.toString(), R"({"data":{"test":"data"},"error":0})");
}

TEST(GuardBearResponse, toStringEmptyMessage)
{
    const json::Json jdata {R"({"test": "data"})"};
    const int error {0};
    const std::string message {""};
    const base::utils::guardbearProtocol::GuardBearResponse wresponse {jdata, error, message};
    EXPECT_EQ(wresponse.toString(), R"({"data":{"test":"data"},"error":0})");
}

TEST(GuardBearResponse, toStringEmptyData)
{
    const json::Json jdata {R"({})"};
    const int error {0};
    const std::string message {"test message"};
    const base::utils::guardbearProtocol::GuardBearResponse wresponse {jdata, error, message};
    EXPECT_EQ(wresponse.toString(), R"({"data":{},"error":0,"message":"test message"})");
}

TEST(GuardBearResponse, toStringArrayData)
{
    const json::Json jdata {R"([{"test": "data"}])"};
    const int error {0};
    const std::string message {"test message"};
    const base::utils::guardbearProtocol::GuardBearResponse wresponse {jdata, error, message};
    EXPECT_EQ(wresponse.toString(), R"({"data":[{"test":"data"}],"error":0,"message":"test message"})");
}

TEST(GuardBearResponse, toStringEmptyDataEmptyMessage)
{
    const json::Json jdata {R"({})"};
    const int error {0};
    const std::string message {""};
    const base::utils::guardbearProtocol::GuardBearResponse wresponse {jdata, error, message};
    EXPECT_EQ(wresponse.toString(), R"({"data":{},"error":0})");
}

TEST(GuardBearResponse, validateOkObject)
{
    const json::Json jdata {R"({"test": "data"})"};
    const int error {0};
    const std::string message {"test message"};
    const base::utils::guardbearProtocol::GuardBearResponse wresponse {jdata, error, message};
    EXPECT_TRUE(wresponse.isValid());
}

TEST(GuardBearResponse, validateOkArray)
{
    const json::Json jdata {R"([{"test": "data"}])"};
    const int error {0};
    const std::string message {"test message"};
    const base::utils::guardbearProtocol::GuardBearResponse wresponse {jdata, error, message};
    EXPECT_TRUE(wresponse.isValid());
}

TEST(GuardBearResponse, validateOkEmptyObject)
{
    const json::Json jdata {R"({})"};
    const int error {0};
    const std::string message {"test message"};
    const base::utils::guardbearProtocol::GuardBearResponse wresponse {jdata, error, message};
    EXPECT_TRUE(wresponse.isValid());
}

TEST(GuardBearResponse, validateOkEmptyArray)
{
    const json::Json jdata {R"([])"};
    const int error {0};
    const std::string message {"test message"};
    const base::utils::guardbearProtocol::GuardBearResponse wresponse {jdata, error, message};
    EXPECT_TRUE(wresponse.isValid());
}

TEST(GuardBearResponse, validateOkEmptyMessage)
{
    const json::Json jdata {R"({"test": "data"})"};
    const int error {0};
    const std::string message {""};
    const base::utils::guardbearProtocol::GuardBearResponse wresponse {jdata, error, message};
    EXPECT_TRUE(wresponse.isValid());
}

TEST(GuardBearResponse, validateOkEmptyData)
{
    const json::Json jdata {R"({})"};
    const int error {0};
    const std::string message {"test message"};
    const base::utils::guardbearProtocol::GuardBearResponse wresponse {jdata, error, message};
    EXPECT_TRUE(wresponse.isValid());
}

TEST(GuardBearResponse, validateOkEmptyDataEmptyMessage)
{
    const json::Json jdata {R"({})"};
    const int error {0};
    const std::string message {""};
    const base::utils::guardbearProtocol::GuardBearResponse wresponse {jdata, error, message};
    EXPECT_TRUE(wresponse.isValid());
}

TEST(GuardBearResponse, validateErrorInvalidDataStr)
{
    const json::Json jdata {R"("test")"};
    const int error {0};
    const std::string message {"test message"};
    const base::utils::guardbearProtocol::GuardBearResponse wresponse {jdata, error, message};
    EXPECT_FALSE(wresponse.isValid());
}

TEST(GuardBearResponse, validateErrorInvalidDataInt)
{
    const json::Json jdata {R"(1)"};
    const int error {0};
    const std::string message {"test message"};
    const base::utils::guardbearProtocol::GuardBearResponse wresponse {jdata, error, message};
    EXPECT_FALSE(wresponse.isValid());
}

TEST(GuardBearResponse, validateErrorInvalidDataBool)
{
    const json::Json jdata {R"(true)"};
    const int error {0};
    const std::string message {"test message"};
    const base::utils::guardbearProtocol::GuardBearResponse wresponse {jdata, error, message};
    EXPECT_FALSE(wresponse.isValid());
}

TEST(GuardBearResponse, validateErrorInvalidDataNull)
{
    const json::Json jdata {R"(null)"};
    const int error {0};
    const std::string message {"test message"};
    const base::utils::guardbearProtocol::GuardBearResponse wresponse {jdata, error, message};
    EXPECT_FALSE(wresponse.isValid());
}
