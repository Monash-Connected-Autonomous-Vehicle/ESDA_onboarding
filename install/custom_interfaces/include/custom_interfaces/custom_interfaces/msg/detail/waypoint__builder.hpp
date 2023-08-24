// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_interfaces:msg/Waypoint.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__MSG__DETAIL__WAYPOINT__BUILDER_HPP_
#define CUSTOM_INTERFACES__MSG__DETAIL__WAYPOINT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_interfaces/msg/detail/waypoint__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_interfaces
{

namespace msg
{

namespace builder
{

class Init_Waypoint_radius
{
public:
  explicit Init_Waypoint_radius(::custom_interfaces::msg::Waypoint & msg)
  : msg_(msg)
  {}
  ::custom_interfaces::msg::Waypoint radius(::custom_interfaces::msg::Waypoint::_radius_type arg)
  {
    msg_.radius = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interfaces::msg::Waypoint msg_;
};

class Init_Waypoint_z
{
public:
  explicit Init_Waypoint_z(::custom_interfaces::msg::Waypoint & msg)
  : msg_(msg)
  {}
  Init_Waypoint_radius z(::custom_interfaces::msg::Waypoint::_z_type arg)
  {
    msg_.z = std::move(arg);
    return Init_Waypoint_radius(msg_);
  }

private:
  ::custom_interfaces::msg::Waypoint msg_;
};

class Init_Waypoint_y
{
public:
  explicit Init_Waypoint_y(::custom_interfaces::msg::Waypoint & msg)
  : msg_(msg)
  {}
  Init_Waypoint_z y(::custom_interfaces::msg::Waypoint::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_Waypoint_z(msg_);
  }

private:
  ::custom_interfaces::msg::Waypoint msg_;
};

class Init_Waypoint_x
{
public:
  Init_Waypoint_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Waypoint_y x(::custom_interfaces::msg::Waypoint::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_Waypoint_y(msg_);
  }

private:
  ::custom_interfaces::msg::Waypoint msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interfaces::msg::Waypoint>()
{
  return custom_interfaces::msg::builder::Init_Waypoint_x();
}

}  // namespace custom_interfaces

#endif  // CUSTOM_INTERFACES__MSG__DETAIL__WAYPOINT__BUILDER_HPP_
