// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from custom_interfaces:msg/Waypoint.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACES__MSG__DETAIL__WAYPOINT__STRUCT_H_
#define CUSTOM_INTERFACES__MSG__DETAIL__WAYPOINT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/Waypoint in the package custom_interfaces.
typedef struct custom_interfaces__msg__Waypoint
{
  int64_t x;
  int64_t y;
  int64_t z;
  int64_t radius;
} custom_interfaces__msg__Waypoint;

// Struct for a sequence of custom_interfaces__msg__Waypoint.
typedef struct custom_interfaces__msg__Waypoint__Sequence
{
  custom_interfaces__msg__Waypoint * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_interfaces__msg__Waypoint__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CUSTOM_INTERFACES__MSG__DETAIL__WAYPOINT__STRUCT_H_
