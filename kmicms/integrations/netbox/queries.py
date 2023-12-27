GET_DEVICE_QUERY = """
query DeviceInfo($deviceId: Int!) {
  device(id: $deviceId) {
    name
    role {
      name
      color
    }
    description
    comments
    platform {
      name
    }
    interfaces {
      description
      name
      enabled
      ip_addresses {
        display
        dns_name
      }
    }
    device_type {
      model
      manufacturer {
        name
      }
      front_image
      rear_image
    }
    tags {
      name
      color
    }
    rack {
      name
    }
    location {
      name
    }
    position
    status
  }
}
"""

LIST_DEVICE_QUERY = """
query listDevices {
  device_list {
    id
    name
    role {
      name
      color
    }
    platform {
      name
    }
    device_type {
      model
      manufacturer {
        name
      }
    }
    rack {
      name
    }
    status
  }
}
"""

GET_VM_QUERY = """
query VMInfo($VMId: Int!) {
  virtual_machine(id: $VMId) {
    name
    cluster {
      name
    }
    role {
      name
      color
    }
    description
    comments
    platform {
      name
    }
    interfaces {
      description
      name
      enabled
      ip_addresses {
        display
        dns_name
      }
    }
    vcpus
    memory
    disk
    tags {
      name
      color
    }
    status
  }
}
"""

LIST_VM_QUERY = """
query listVMs {
  virtual_machine_list {
    id
    name
    role {
      name
      color
    }
    platform {
      name
    }
    cluster {
      name
    }
    status
  }
}
"""
